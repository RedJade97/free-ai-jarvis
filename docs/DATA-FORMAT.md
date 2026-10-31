# Data format and commands

Files are UTF-8 JSON objects with `schema_version: 1` and any of the arrays `experiments`, `evidence`, `lessons`, `reviews`. Omit unused arrays. Import is transactional: an invalid record rejects the whole file. Identical records are reused. Changed content under an existing ID is rejected.

Use [first-experiment.json](../examples/first-experiment.json), [review.json](../examples/review.json) and [lesson.json](../examples/lesson.json) as complete fictional examples. JSON uses double quotes, lowercase `true`/`false` and `null`. The IDs are references, not filenames. Use letters, numbers, underscores and hyphens.

## Experiments

Required: `id`, `title`, `objective`, `success_rule`, `created_at`. Optional `parent_id` links to an existing experiment. Cyclic parents are rejected. Dates need an explicit timezone. The textual success rule is your predeclared decision rule; the tracker does not automatically evaluate arbitrary prose.

State starts at planned. `advance` permits only:

- **testing:** at least two distinct platform/post IDs and two variant names exist.
- **reviewed:** the latest dated review cites both variants, and all cited media are marked verified with timeline coverage from zero through duration.
- **closed:** an actual outcome/decision is recorded with `--note`. Closed experiments cannot reopen; use a new linked experiment.

Transitions do not certify statistical adequacy, platform publication or the quality of a review. A source reference can be an offline file or fictional source; actual publication must be checked by you.

## Evidence observations

Required fields:

| Field | Meaning |
| --- | --- |
| `id`, `experiment_id`, `variant` | Unique observation ID, concept/experiment, control/test or archive label |
| `post_id`, `source_ref` | Stable post identifier plus original URL or private evidence reference |
| `platform`, `cohort` | Keep platforms and distribution conditions separate |
| `published_at`, `observed_at`, `labels_at` | Timezone-aware dates; labels must precede or equal the observation |
| `features` | Boolean feature labels, e.g. `{"direct_open": true}` |
| `views`, `saves`, `shares`, `follows` | Nonnegative integers or `null`; all four keys must be present |
| `duration_seconds`, `media_verified` | Positive clip duration and your manual verification flag |

Optional `retention` is a list of `{"second": 10, "fraction": 0.6}`. Timestamps must be unique and within the clip; fractions are between 0 and 1. Sparse curves are allowed and never interpolated.

Optional `segments` is a list of `start`, `end`, `source_start`, `source_end`, `speech`, `screen`. All times are seconds. Use explicit descriptions for silence or a blank screen. Gaps are allowed while collecting; they block the reviewed transition. These time maps are recorded, not automatically checked against video.

A platform/post/observation-time tuple can appear only once, even under different IDs. Multiple snapshots of a post must retain experiment, variant, publication timestamp, cohort and feature labels. Counts must refer to the same source observation; the software cannot verify the screenshot for you.

## Lessons

Required: `id`, `claim`, `created_at`, `instrument`.

The instrument has `feature`, `metric`, `platform`, `cohort`, `min_per_group`, `min_views`, `target_age_hours`, `age_tolerance_hours`, `minimum_difference`, `direction`. Supported metrics and exact selection are in [learning rules](LEARNING-RULES.md). `min_per_group` must be at least two; eight is the documented starting gate. The example uses eight.

These are predefined calculations, not arbitrary executable code. Imports cannot ask the tracker to run a shell command or connect to a service.

## Reviews

Required: `id`, `experiment_id`, `evidence_ids`, `conclusion`, `limitations`, `next_test`, `created_at`, `edits`.

Reference at least two distinct evidence IDs from the experiment. Each edit has `evidence_id`, `start`, `end`, `action` (KEEP/CHANGE/CUT), `method` (EDIT/RECORD/NONE), `reason`, `success_metric`. An edit must stay within the cited clip. Record uncertainty in the reason; metrics are proposed tests, not automatic proof that an edit worked.

## Commands

Place `--workspace` before the command. Default: `private/brain`.

```bash
python brain.py init
python brain.py import private/brain/incoming/batch.json
python brain.py advance MY-001 testing
python brain.py advance MY-001 reviewed
python brain.py advance MY-001 closed --note "Actual outcome and decision"
python brain.py retest LS-001 --run-id weekly-001 --as-of 2026-11-07T18:00:00+10:00
python brain.py report
python brain.py --workspace private/demo demo
```

`report` creates `reports/dashboard.html`, `reports/review.md` and `reports/context.json`. They are overwritten on each run, while records, transitions and retests remain in the database. Context exports may contain sensitive source references and notes.

## Corrections and backups

New measurements get new observation IDs and dates. A correction to the same measurement must **not** be disguised as a new independent observation or post. This release has no in-place correction or exclusion editor.

For a factual mistake, preserve a dated backup of the affected workspace. Correct your original import files, record an explanation of the correction, then rebuild a separate workspace from those files and rerun the affected transitions and tests in chronological order. Keep the prior workspace as an audit record. The original mistaken records must not remain eligible in the corrected workspace. Do not directly edit SQLite to bypass validation.

For a revised claim or instrument, create a new lesson ID, explain its relationship to the old one in your notes, and gather prospective evidence. Old claims and results remain readable.

Back up the entire workspace after commands have exited. To restore, copy the folder to a private location and use `--workspace`. The context export includes records and run history for portability; it is not directly accepted by `import` and does not restore transition/audit history. Keep original import files and the SQLite backup.
