# Sources, provenance and scope

Reviewed 31 October 2026. These links support the feature comparisons; they do not establish that any particular seller is dishonest. The value judgement in the README is the author's opinion about the described sales pitch.

## Second-brain workflow

The conceptual reference was Angus Sewell's *Your AI Content Coach*, a nine-page PDF supplied by the repository maintainer. It describes evidence collection, content timelines, experiment tracking, reusable procedures and lessons revisited with later evidence. Its examples distinguish a local test with mocked external steps from a fully demonstrated end-to-end integration.

This repository's code, examples and procedure wording are original. The PDF, its embedded TikTok collector and its paid skills are not redistributed or covered by this repository's MIT licence. This implementation uses manual imports and a local Python/SQLite tracker instead of that guide's proposed collection, editing and audio integrations. There is no affiliation or endorsement.

The guide informed the workflow, not proof that a particular tool works or that a particular seller is dishonest. Confidence labels, minimum sample gates and confirmation counts are transparent operational conventions; they are not validated statistical guarantees. See [the implemented rules](docs/LEARNING-RULES.md).

## Local runtime

- [Python downloads](https://www.python.org/downloads/) and [Windows setup](https://docs.python.org/3/using/windows.html).
- [Python SQLite support](https://docs.python.org/3/library/sqlite3.html): the tracker stores evidence and audit history locally using the standard library.
- [Python statistics](https://docs.python.org/3/library/statistics.html): the fixed instruments compare arithmetic means, with a leave-one-experiment-out sensitivity check for apparent support.

## Optional native assistant features

| Claim | Official source | Scope |
| --- | --- | --- |
| ChatGPT has memory controls | [Memories](https://learn.chatgpt.com/docs/customization/memories) | ChatGPT memory and local Codex memory are separate systems |
| ChatGPT projects share context | [Projects and chats](https://learn.chatgpt.com/docs/projects) | Files must be uploaded or connected; a local file is not automatically visible |
| ChatGPT offers native voice | [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) | Desktop access depends on plan, rollout and workspace settings |
| Claude has memory | [Chat search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context) | Includes controls to review and change remembered information |
| Claude offers native voice | [Voice mode](https://support.claude.com/en/articles/11101966-use-voice-mode) | Documented across plans, including Free; usage limits apply |
| Grok advertises voice and cross-chat memory | [Grok product page](https://x.ai/grok) | Product descriptions are not a guarantee of recall in every session |
| Grok supports files and voice | [Grok overview](https://docs.x.ai/grok/overview) | Account availability and usage limits matter |
| Grok Bot supports persistent work | [Grok Bot overview](https://docs.x.ai/grok-bot/overview) and [FAQ](https://docs.x.ai/grok-bot/faq) | A separate product with persistent context and connected work capabilities |
| Production voice agents can include more infrastructure | [Voice Agent Builder](https://x.ai/news/grok-voice-agent-builder) | Telephony, retrieval, tools and operational controls go beyond a prompt and memory file |

## What this repo does not establish

- That every "Jarvis" or "second brain" product has the same architecture.
- That this kit exactly reproduces an unspecified seller's implementation.
- That all three providers have identical memory, voice, automation or plan access.
- That commercial model usage, voice or hosting is unlimited and free.
- That a memory file provides the security, reliability or integrations of an enterprise deployment.

The practical claim is to try a transparent, self-owned workflow before paying for an implementation. Native memory and voice alone do not reproduce the richer evidence-and-retest workflow. Additional engineering and reliable integrations can have value.

The local tool is tested with synthetic evidence, including contradiction, insufficient samples, duplicate protection, timeline coverage and experiment transitions. The documented local demo and practice workflow are exercised separately from provider products. No live TikTok, Instagram, Descript or audio integration has been tested or included. Optional native-app instructions have not been exercised in every account or plan. Report broken steps without including private records.
