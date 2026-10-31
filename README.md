# Build your own AI second brain. Keep your money and your knowledge.

**Free software, a step-by-step guide and reusable procedures. By Red Jade.**

A useful second brain keeps evidence, tracks work, tests ideas and revises what it thinks it knows. This repo helps you build that loop yourself:

**Capture → organise → analyse → test → save lessons → retest.**

## My take

If somebody sells you a revolutionary "AI Jarvis" and delivers a prompt, a memory file and a voice interface while hiding the ordinary tools underneath, I think you are getting rorted. Selling that as a secret invention is, in my view, a scammy sales pitch.

But a serious second brain can involve more: reliable collection, connected tools, a searchable archive, experiment tracking and lessons checked against new evidence. That work has substance. Judge the implementation, ownership, reliability and support rather than the branding.

**Before paying for an implementation, try building it with this repo. The guide and software are FREE.** No course, sales call, mandatory subscription or API key. The core works offline once Python is installed. An AI assistant can help interpret the evidence, but is optional and does not secretly power the calculations.

## Start here

- **[Step-by-step setup](SETUP.md)** — run a learning demo, complete a practice experiment, then use your own evidence.
- **[No-code workflow](docs/NO-CODE.md)** — follow the same process with folders, text files and your existing assistant.
- **[Content-coaching workflow](docs/CONTENT-WORKFLOW.md)** — connect videos, speech, screen content, retention, edits and later results.
- **[How learning works](docs/LEARNING-RULES.md)** — formulas, exclusions, confidence rules and limitations.
- **[Optional memory and voice](docs/MEMORY-AND-VOICE.md)** — add conversational personalisation after the evidence workflow is in place.

## What is included

| Layer | Included here |
| --- | --- |
| Evidence | Local database of sources, dated observations, labelled features, speech/screens and original-media time maps |
| Experiments | Objectives and success rules, linked follow-up experiments, guarded progress from planned to closed |
| Procedures | Three [reusable procedure files](procedures/README.md) for capture, review and learning |
| Lessons | Original claims, executable comparison rules, retest history, exclusions and changing confidence |
| Review | Local HTML dashboard, readable review and complete context export for an assistant |
| Learning demo | Fictional results that strengthen a lesson, then contradict it |

The Python tool uses only the standard library and makes **no network calls**. Your data defaults to `private/brain`, which Git ignores. The database is local and unencrypted; keep it private and back it up.

## Try the learning loop

Download this repo using **Code → Download ZIP**, extract it, open a terminal in that folder, and run:

```bash
python brain.py --workspace private/demo demo
```

Open `private/demo/reports/dashboard.html`. The demo uses 64 fictional concepts across four batches. A lesson moves from **hunch → likely → supported (provisional) → contradicted**. The original claim and each result remain available. Use a separate empty folder for each fresh demo.

Need help with Python or terminals? Follow [the full setup guide](SETUP.md).

## What the free version does

It imports observations you provide, calculates comparable metrics, checks evidence coverage, tracks experiments, executes a fixed set of lesson tests and exports reports. You manually gather your own analytics, inspect your media, make edits and publish if you choose. An optional assistant helps organise and interpret supplied records.

It does **not** automatically scrape TikTok, transcribe or inspect video, edit in Descript, post to Instagram, run in the background or generate audio. Those integrations would be additional work. Native assistant memory and voice alone do not reproduce this workflow.

## Cost and ownership

- **Repo, local tracker, calculations and reports:** no software fee or model tokens.
- **AI help:** optional; use an existing free allowance where available. Paid models and API usage may cost money.
- **Voice, cloud storage, transcription and editing services:** optional, with their own pricing and limits.
- **Your time, computer and storage:** still needed, especially for collection and media review.

Your evidence, experiment history, instructions and lessons stay in readable exports you control. Original material in this repository is available under the [MIT licence](LICENSE).

## Before you pay a seller

Ask them to demonstrate the complete loop on your use case, show how errors and missing data are handled, identify ongoing costs and export your knowledge in an ordinary format. Ask what happens when a lesson is contradicted. A confident voice is not evidence that a system learns reliably.

This is an original reference implementation informed by a supplied content-coaching guide. It does not redistribute that PDF, its embedded collector or paid skills, and is not an exact clone of a commercial product. See [sources and scope](SOURCES.md).

**Share the toolkit. Keep your real evidence and personal memory private.**
