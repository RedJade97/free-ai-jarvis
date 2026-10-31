# Worked workflow: a content coach that learns from your archive

This is a free manual collection and editing route with automated local bookkeeping and lesson tests. It does not depend on Descript, a social-platform scraper or an audio service. No live platform connection is included or claimed as tested.

## Capture what actually happened

Keep three separate assets: the master recording, the control cut actually posted, and the test cut actually posted. Record the real platform post IDs and URLs. Filenames and matching durations are not enough to identify sibling cuts.

Download analytics through your own account where available, or record them manually from the platform's interface. Keep a dated screenshot/export as the source. Do not enter passwords, cookies or login sessions into this repository.

Each observation should state platform, organic/paid or other distribution cohort, publication time, collection time, views, saves, shares and follows. Unknown fields stay null. Revisit on your chosen schedule and append a new observation instead of changing an old one.

## Build the content timeline

Watch each full cut. Manually transcribe speech, including important silence, and describe meaningful on-screen content. Split the timeline at useful edit boundaries. Map each segment to the original recording.

| Posted-cut interval | Original interval | Speech | Screen |
| --- | --- | --- | --- |
| 0–3 seconds | 5–8 seconds | The exact opening words | What the viewer sees |
| 3–8 seconds | 14–19 seconds | The explanation | Demonstration |
| 8–12.5 seconds | 23–27.5 seconds | The closing words | Final result |

These are illustrative intervals, not measurements of a real video. In your records, cover the actual final fraction of a second. Set `media_verified` to true only after personally checking that cut, transcript, screen notes and time map. If a tool transcribes for you, still check it against the media.

Import observed retention points as fractions between 0 and 1, preserving their timestamps. The tracker never invents missing seconds. Its complete-timeline check does not imply a complete retention curve.

## Compare fairly

Compare posts at a preselected age, with a minimum reach and similar distribution. Keep retention, saves, shares and follows as separate measures. Use paired saves/views from a single observation.

For a three-second interval with both endpoints observed, relative retention loss is:

`1 − retained(t + 3) / retained(t)`, provided `retained(t) > 0`.

This interval calculation is a manual review step, not an automated feature in the tracker. Missing endpoints mean unknown. A dip shows where viewers left; it does not establish why.

Inspect a comparable archive, including weak examples and counterexamples. Label features without looking at their performance. Match platform, distribution cohort and post age. Avoid treating repeated cuts of a successful concept as many independent examples. The executable retest conservatively selects one post per experiment.

## Turn a review into an edit plan

Use the actual words and posted-cut timestamps. For each change record KEEP, CHANGE or CUT, whether editing or re-recording is needed, the reason, the test hypothesis and the metric it should affect. Keep working passages instead of rewriting everything.

Use an editor you already have, or make a simple new recording. Review both complete exports. An editor or AI tool is useful only if you verify what it produced.

Publish manually when you choose. Organic posts or platform trials are not automatically randomised A/B tests. Record changes in audience, reach, timing or promotion. The tool stores your written success rule but does not decide if the difference proves an effect or automatically publish a winner.

## Learn across experiments

A first pair can generate a hypothesis such as "direct openings are associated with a higher save rate in this cohort." Register the claim before collecting the next evidence. Test it on new concepts with and without the feature; see [learning rules](LEARNING-RULES.md).

Review exclusions, individual examples and sensitivity to a strong outlier. A result that fails a harder check becomes uncertain. A later contradiction remains attached to the original claim rather than disappearing from the history.

Your weekly output should explain what was observed, what remains uncertain, which lessons changed and what to test next. Audio can narrate that report, but does not make it more reliable.

## Extending this later

Automated collectors, transcription, editor integrations, reminders and spoken reports can reduce manual effort. Add one at a time and require a real source record, a correct saved result and a visible failure state before relying on it. This repo intentionally includes no credentials or copied third-party collector source.
