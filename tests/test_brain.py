import copy
import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from brain import Brain, demo_payload, metric, utc

AS_OF = '2026-10-31T00:00:00+00:00'
ROOT = Path(__file__).resolve().parents[1]


class BrainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.brain = Brain(self.temp.name)
        self.data, self.dates = demo_payload(AS_OF)

    def tearDown(self):
        self.brain.close()
        self.temp.cleanup()

    def test_import_is_idempotent_and_conflicts_are_atomic(self):
        self.assertEqual(self.brain.ingest(self.data), 129)
        self.assertEqual(self.brain.ingest(self.data), 0)
        bad = copy.deepcopy(self.data)
        bad['experiments'].insert(0, dict(bad['experiments'][0], id='EXTRA'))
        bad['evidence'][0]['views'] = 99
        with self.assertRaises(ValueError):
            self.brain.ingest(bad)
        self.assertNotIn('EXTRA', self.brain.records('experiments'))

    def test_confirmation_then_refutation_and_no_rewrite(self):
        self.brain.ingest(self.data)
        lesson = self.data['lessons'][0]
        expected = ['hunch', 'likely', 'supported (provisional)', 'contradicted']
        for index, date in enumerate(self.dates):
            result = self.brain.retest(lesson['id'], f'run-{index}', date)
            self.assertEqual(len(result['with_feature']), 8)
            self.assertEqual(len(result['without_feature']), 8)
            self.assertEqual(self.brain.confidence(lesson, date), expected[index])
        self.assertEqual(self.brain.records('lessons')[lesson['id']]['claim'], lesson['claim'])

    def test_run_reruns_do_not_add_confirmations(self):
        self.brain.ingest(self.data)
        first = self.brain.retest('DEMO-lesson', 'same', self.dates[0])
        self.assertEqual(first, self.brain.retest('DEMO-lesson', 'same', self.dates[0]))
        self.assertEqual(len(self.brain.runs('DEMO-lesson')), 1)
        later = (utc(self.dates[0])+timedelta(hours=1)).isoformat()
        self.assertEqual(self.brain.retest('DEMO-lesson', 'new-name', later)['outcome'], 'insufficient')
        with self.assertRaises(ValueError):
            self.brain.retest('DEMO-lesson', 'same', later)

    def test_sibling_variants_are_not_independent_evidence(self):
        first = self.data['evidence'][0]
        sibling = dict(first, id='SIBLING', post_id='Z-SIBLING', variant='sibling')
        self.data['evidence'].append(sibling)
        self.brain.ingest(self.data)
        run = self.brain.retest('DEMO-lesson', 'one', self.dates[0])
        self.assertEqual(len(run['with_feature']), 8)
        self.assertTrue(any(x['id'] == 'SIBLING' for x in run['exclusions']))

    def test_missing_counts_and_zero_views_stay_unknown(self):
        self.assertIsNone(metric({'views': 1000, 'saves': None}, 'saves_per_1000'))
        self.assertIsNone(metric({'views': 0, 'saves': 1}, 'saves_per_1000'))
        self.assertIsNone(metric({'retention': [{'second': 9, 'fraction': .8}, {'second': 11, 'fraction': .7}]}, 'retention_10s'))
        self.data['evidence'][0]['saves'] = None
        self.brain.ingest(self.data)
        self.assertEqual(self.brain.retest('DEMO-lesson', 'one', self.dates[0])['outcome'], 'insufficient')

    def test_sample_gates_platform_cohort_age_and_views(self):
        for row, change in zip(self.data['evidence'][:4], [{'platform': 'other'}, {'cohort': 'paid'}, {'views': 10}, {'observed_at': self.dates[1]}]):
            row.update(change)
        self.brain.ingest(self.data)
        run = self.brain.retest('DEMO-lesson', 'one', self.dates[0])
        self.assertEqual(run['outcome'], 'insufficient')
        self.assertEqual(len(run['with_feature']), 4)

    def test_snapshot_uniqueness(self):
        self.data['evidence'].append(dict(self.data['evidence'][0], id='COPY'))
        with self.assertRaises(ValueError):
            self.brain.ingest(self.data)
        self.assertEqual(len(self.brain.records('evidence')), 0)

    def test_no_hindsight_label_or_nonfinite_number(self):
        self.data['evidence'][0]['labels_at'] = AS_OF
        with self.assertRaises(ValueError):
            self.brain.ingest(self.data)
        self.data, _ = demo_payload(AS_OF)
        self.data['lessons'][0]['instrument']['minimum_difference'] = float('nan')
        with self.assertRaises(ValueError):
            self.brain.ingest(self.data)

    def test_staleness_and_insufficient_runs_do_not_refresh_confidence(self):
        self.brain.ingest(self.data)
        lesson = self.data['lessons'][0]
        for index in range(3):
            self.brain.retest(lesson['id'], str(index), self.dates[index])
        last = utc(self.dates[2])
        self.assertEqual(self.brain.confidence(lesson, (last+timedelta(days=31)).isoformat()), 'needs retest')
        self.assertEqual(self.brain.confidence(lesson, (last+timedelta(days=91)).isoformat()), 'stale')

    def test_fragile_pattern_does_not_get_support(self):
        for row in self.data['evidence'][:8]:
            row['saves'] = 20
        self.data['evidence'][0]['saves'] = 100
        self.brain.ingest(self.data)
        run = self.brain.retest('DEMO-lesson', 'fragile', self.dates[0])
        self.assertEqual(run['difference'], 10)
        self.assertEqual(run['minimum_leave_one_out_difference'], 0)
        self.assertEqual(run['outcome'], 'inconclusive')

    def test_complete_media_includes_fractional_final_second(self):
        row = dict(self.data['evidence'][0], media_verified=True, segments=[{'start': 0, 'end': 12}])
        self.assertFalse(self.brain.complete_media(row))
        row['segments'][0]['end'] = 12.5
        self.assertTrue(self.brain.complete_media(row))
        row['segments'][0]['start'] = .5
        self.assertFalse(self.brain.complete_media(row))

    def test_practice_lifecycle_and_closed_history(self):
        self.brain.ingest(json.loads((ROOT/'examples/first-experiment.json').read_text()))
        self.brain.advance('EX-001', 'testing')
        with self.assertRaises(ValueError):
            self.brain.advance('EX-001', 'reviewed')
        self.brain.ingest(json.loads((ROOT/'examples/review.json').read_text()))
        self.brain.advance('EX-001', 'reviewed')
        with self.assertRaises(ValueError):
            self.brain.advance('EX-001', 'closed')
        self.brain.advance('EX-001', 'closed', 'Keep control; run another test')
        with self.assertRaises(ValueError):
            self.brain.advance('EX-001', 'testing')

    def test_report_is_local_and_escapes_html(self):
        self.data['lessons'][0]['claim'] = '<script>alert(1)</script>'
        self.brain.ingest(self.data)
        output = self.brain.report(AS_OF)
        page = (output/'dashboard.html').read_text(encoding='utf-8')
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)
        self.assertEqual(len(json.loads((output/'context.json').read_text())['evidence']), 64)


if __name__ == '__main__':
    unittest.main()
