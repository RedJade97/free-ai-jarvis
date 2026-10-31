# Free setup: a second brain that revises its lessons

Build a local evidence archive, experiment tracker, lesson register and review dashboard. No paid app, API key or server is required. AI assistance is optional. The executable examples concern content creation; the [no-code method](docs/NO-CODE.md) also works for other projects.

## 1. Download and install

1. Choose **Code → Download ZIP** on this repository and extract the ZIP.
2. Install Python 3.10 or later from [python.org](https://www.python.org/downloads/). Windows users can follow the [official instructions](https://docs.python.org/3/using/windows.html).
3. Open a terminal in the extracted folder. On Windows, right-click the folder background and choose **Open in Terminal**. On macOS/Linux, open Terminal, type `cd `, drag the extracted folder into it and press Enter.
4. Run `python --version`. If Windows recognises `py` instead, use it in all commands below. On macOS/Linux the command may be `python3`.

No packages need installing. Standard Python includes SQLite and everything this tool uses.

## 2. Watch a lesson change its mind

```bash
python brain.py --workspace private/demo demo
```

Expected output includes:

```text
DEMO-run-1: supports -> hunch
DEMO-run-2: supports -> likely
DEMO-run-3: supports -> supported (provisional)
DEMO-run-4: contradicts -> contradicted
```

Open `private/demo/reports/dashboard.html` in your browser. Its evidence link opens the full JSON record. All demo data is fictional. These classifications are bookkeeping rules, not statistical proof.

The demo refuses to overwrite a populated workspace. To repeat from scratch, change its folder to `private/demo-2`. Keep demo and real work separate.

## 3. Complete a practice experiment

These records contain two fictional cuts of one idea:

```bash
python brain.py --workspace private/practice import examples/first-experiment.json
python brain.py --workspace private/practice advance EX-001 testing
python brain.py --workspace private/practice import examples/review.json
python brain.py --workspace private/practice advance EX-001 reviewed
python brain.py --workspace private/practice advance EX-001 closed --note "Fictional practice complete; test a new concept next."
python brain.py --workspace private/practice report
```

Open `private/practice/reports/dashboard.html`. The experiment should be **closed**. Its review links edits and conclusions to evidence IDs. The example's media verification is fictional too; never carry that flag into real records without checking them.

Reimport `examples/first-experiment.json`: it adds zero records. Moving the closed experiment back to testing is refused. A new test gets a new experiment ID, optionally linked through `parent_id`.

## 4. Create your real workspace

```bash
python brain.py init
```

This creates `private/brain/brain.sqlite3`. In your file manager, create these optional folders beside the database:

```text
private/brain/
  brain.sqlite3
  incoming/          JSON files you want to import
  originals/         original media or documents
  observations/      dated exports or screenshots
  reviews/           written reviews
  reports/           generated dashboard and assistant context
```

Copy [MEMORY.md](templates/MEMORY.md) into your private folder and fill in your objective, audience, constraints and preferences. It complements the evidence archive.

Git ignores `private/`, but it is not encrypted. Never upload it or an entire working-project ZIP publicly. Keep custom workspace paths private too.

## 5. Plan before looking at results

Copy `examples/first-experiment.json` to `private/brain/incoming/experiment-001.json`. Replace the fictional experiment with your own and start with an empty `evidence` array. Use the [data reference](docs/DATA-FORMAT.md).

Assign an ID such as `MY-001`, an objective and a success rule: metric, comparison age, minimum views, what changes and what should stay similar. Use timestamps with timezones, such as `2026-10-31T09:00:00+10:00`.

```bash
python brain.py import private/brain/incoming/experiment-001.json
```

An assistant can format JSON from your notes using the examples. Review its output; do not let it invent counts, dates or observations.

## 6. Collect and connect evidence

Keep the master recording and actual posted cuts. Label observable features before inspecting performance. Map original-media seconds to posted-cut seconds.

Open your own platform analytics and save an export or dated screenshot. In a new JSON file, record each post's ID, source reference, platform, distribution cohort, publication time, observation time and counts. Saves and views must come from the **same observation**. Use `null` for unknown counts, never zero. Follow the [content walkthrough](docs/CONTENT-WORKFLOW.md) for speech, screens and retention.

```bash
python brain.py import private/brain/incoming/observations-001.json
python brain.py advance MY-001 testing
```

Testing requires two distinct posts with two variant names. A later snapshot gets a new evidence ID and observation time. Identical imports are reused; conflicting changes are rejected. See [corrections](docs/DATA-FORMAT.md#corrections-and-backups) before repairing a mistaken record.

## 7. Review results and propose edits

```bash
python brain.py report
```

Read the dashboard and source evidence, or give selected records from `context.json`, actual media and [the review procedure](procedures/02-review.md) to your assistant. Only upload information you intend the provider to process; the export is not anonymised.

Copy `examples/review.json` into your private incoming folder. Replace it with your conclusion, limitations, evidence IDs, exact edit intervals, reasons, success metrics and next test. Preserve "cannot tell" when evidence is inadequate.

```bash
python brain.py import private/brain/incoming/review-001.json
python brain.py advance MY-001 reviewed
```

This requires a review covering both variants and complete, manually verified speech/screen/source timelines through the fractional final second. The tool checks the records' shape and coverage; it cannot verify that descriptions are truthful or reasoning is sound.

## 8. Make the next version and close the loop

Use your existing editor to apply reviewed changes or record new material. Preserve an unchanged control where practical. Watch complete exports and verify time maps. Publish yourself if appropriate.

Record the actual decision:

```bash
python brain.py advance MY-001 closed --note "Reviewed both cuts. Next test: opening property on a new concept; no causal conclusion yet."
```

Create a new experiment for the next comparison with `parent_id` set to `MY-001`. Repeat steps 5–8. Each comparison follows **planned → testing → reviewed → closed**. There is no separate Instagram Trial state; posting and distribution decisions go in evidence and outcome notes.

## 9. Register a testable lesson

Copy `examples/lesson.json` into your private incoming folder. Replace the ID, claim, creation time and instrument. Specify a feature, platform/cohort, metric, comparison age, minimum views, minimum independent concepts per group and meaningful difference. Keep **eight per group** as a starting gate; it is not proof of statistical reliability.

The tool compares mean saves, shares or follows per 1,000 views, or observed retention at exactly second 10, between content with and without a labelled feature. These are associations, not causal experiments.

```bash
python brain.py import private/brain/incoming/lesson-001.json
```

The original archive can suggest a hypothesis. Its executable test uses observations from the lesson's creation onward, so discovery evidence cannot automatically become a new confirmation.

## 10. Retest with later evidence

Collect new independent concepts under the same definitions and import their observations. Use a unique review ID and an actual cutoff with a timezone:

```bash
python brain.py retest LS-001 --run-id review-001 --as-of 2026-11-07T18:00:00+10:00
python brain.py report
```

Replace the example ID and date with yours. Inspect selected evidence, exclusions, group sizes and mean difference. With only one pair of sibling cuts, **insufficient** is correct: one concept is not an archive.

Reuse the same run ID and cutoff to inspect an existing run. New imports need a new run ID and later cutoff. Qualified runs consume their experiments; subsequent confirmations require new experiments observed after the last qualified run. See [the exact rules](docs/LEARNING-RULES.md).

## 11. Run a weekly learning session

Use [the learning procedure](procedures/03-learn.md). Review every active lesson, counterexamples and gaps. Choose at most three next tests and save a private note using [the weekly template](templates/WEEKLY-REVIEW.md).

Reports overwrite the previous rendered dashboard and context export; copy them to a dated private folder for weekly snapshots. The database retains original records and runs.

Audio is optional. Read the report aloud, use device text-to-speech or follow [the memory and voice guide](docs/MEMORY-AND-VOICE.md) within provider limits.

## 12. Back up and verify

After commands finish, copy the whole private workspace to a private backup location. Restore the folder and point `--workspace` to it. The JSON context export is useful for inspection but is not a complete database restore format.

Run the toolkit checks:

```bash
python -m unittest discover -s tests -v
```

Verify your own workflow: imports do not duplicate; unknown counts stay unknown; incomplete timelines block review; reused experiments cannot inflate confidence; contradicted claims remain visible; backups open with `report`.

## Troubleshooting

- **Python missing:** try `py` or `python3`, reopen the terminal after installing, or use the official instructions.
- **brain.py not found:** open the terminal in the extracted repository folder.
- **JSON error:** check commas, double quotes and `null`/`true`/`false`; save as UTF-8.
- **Existing ID differs:** follow the correction guide instead of repeatedly importing a conflict.
- **Insufficient evidence:** inspect exclusions and collect comparable data. Do not lower thresholds to force success.
- **Review blocked:** check both variants' verification flags and timeline coverage through the actual end.

This release has no automatic collector or scheduler. Set a personal reminder for collection and weekly review. No agent needs to stay open all day.
