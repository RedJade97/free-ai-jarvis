# Set up your own basic AI second brain

You will need an assistant account, a text editor and, for voice, a microphone. Start with the free plan of an app that offers the features you need. Stop at any upgrade screen unless you want that paid service. No API key, server or reseller is needed for the workflow below.

## 1. Get the templates

On this repository's GitHub page, choose **Code → Download ZIP**, then extract it. Alternatively, open each file in `templates`, select its raw view and copy the text.

Create a private folder called `My Second Brain` outside your public repository. Put copies of `MEMORY.md` and `ASSISTANT.md` there. These are ordinary text files; edit them with any text editor. If you work inside a local clone instead, use its ignored `private/` folder. Ignoring a file does not protect anything you have already published.

## 2. Write a small memory file

Open your private copy of `MEMORY.md`. Replace the blanks with your preferred name, time zone, response preferences, current priorities and one active project. Delete sections you do not need. Keep the first version short enough to review easily.

For your first test, use fictional information:

```text
Preferred name: Alex
Time zone: Australia/Brisbane
Response preference: Three concise bullets
Current project: Garden plan
Next action: Compare three planter layouts
```

Do not include passwords or API keys. Only send information to an assistant provider that you intend that provider to process. Review its data controls before adding personal or business material.

## 3. Give the assistant its context

Open a new conversation in your chosen assistant. Paste the contents of `ASSISTANT.md`, then paste or attach your private `MEMORY.md`. Send:

```text
Use the attached or pasted MEMORY.md as my current reference for this chat.
Tell me my preferred response style and the next action for my active project.
If you cannot read the file, say so. Do not fill gaps by guessing.
```

Check the answer against the actual file. A file sitting on your computer is not automatically visible to the app: you must paste it, upload it, or explicitly connect it.

## 4. Choose your app's native features

### Claude: a starting route with a free plan

Open Claude on the web, desktop or mobile and complete step 3. For built-in memory, inspect **Settings → Your Claude → Memory from chats**; older layouts may use **Settings → Memory**. Review saved entries through the memory controls. Organisation settings can affect access. [Official memory documentation](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context).

In the same conversation, select the sound-wave voice control, allow microphone access if prompted, and speak the test in step 5. On mobile, choose a voice when asked. Voice is documented for the Free plan too, but consumes your normal usage allowance. [Official voice instructions](https://support.claude.com/en/articles/11101966-use-voice-mode).

### ChatGPT

Complete step 3 in a chat. For related conversations, use a ChatGPT project, add the memory file to its sources and the assistant instructions to its project instructions. Start subsequent chats within that project. [Projects documentation](https://learn.chatgpt.com/docs/projects).

Review ChatGPT memory in **Settings → Personalization**. Memory is a convenience; keep your own file as the reference you can inspect and move. [Memory documentation](https://learn.chatgpt.com/docs/customization/memories).

Where available, start voice in the same chat. The desktop instructions use **Start voice chat** or **Start new voice chat**, with microphone permission and voice selection on first use. Desktop voice availability depends on plan, rollout and workspace settings; do not assume this route is included free. [Voice documentation](https://learn.chatgpt.com/docs/features/voice).

### Grok

Open Grok on web or mobile and complete step 3. Use its voice interface to continue the conversation where supported by your account. Grok documents voice, file uploads and cross-chat memory, but availability and limits can vary. Keep a portable copy of your context instead of assuming every new conversation has it. [Grok features](https://x.ai/grok) and [official overview](https://docs.x.ai/grok/overview).

Grok Bot is a separate option to evaluate if you need persistent work, connected apps and routines. It is beyond this basic setup and is not needed to follow the guide. [Grok Bot overview](https://docs.x.ai/grok-bot/overview).

## 5. Speak to it

Say:

```text
Based only on the memory I gave you, what should I work on next?
Keep it in my preferred response style. Ask one useful follow-up question.
```

You should hear a reply based on your project and preferences. A dictation button only turns speech into typed text; full voice mode also speaks the response. If full voice is unavailable, finish the guide in text or use your device's dictation. That fallback is not a two-way voice call.

## 6. Save approved changes

Tell the assistant something new, then ask:

```text
Propose an updated MEMORY.md containing only confirmed durable facts,
current project state and agreed decisions. Show what changed separately.
Do not claim you saved a file unless you actually have file access and saved it.
```

Read the proposed changes. Correct mistakes. Save the approved replacement to your private file yourself. If you uploaded the old version to a project, replace that source with the new one so two contradictory versions are not present.

This manual loop works without automatic memory: **load context → talk → review changes → save → load next time**. Automatic provider memory is a separate feature and may not match your file exactly.

## 7. Test a fresh conversation

Open a new chat. First ask what it remembers about your project; do not assume the answer is correct. Then load your latest file and instructions and ask again.

| Test | A useful result |
| --- | --- |
| What is my next action? | Matches your saved file |
| What is my time zone? | Matches your saved file |
| Change my preferred style to one paragraph | A proposed update you can review and save |
| What is my budget? (when absent from the file) | Says it does not know |
| Did you put that in my calendar? (with no calendar access) | Says no; a suggestion is not a completed action |

If recall fails, confirm the latest file is available in that chat. If a native memory conflicts with it, correct or remove that entry using the app's controls. If limits stop the session, wait for the allowance to reset or continue later; paying a reseller does not remove provider limits.

## 8. Use it daily

Try the [daily prompts](PROMPTS.md). Once a week, remove stale project details and verify important facts against their original source. Keep dated private backups so you can recover an earlier version.

You now have the basic second-brain workflow: reusable context, a conversational assistant, optional native voice and a memory file you can take elsewhere. Phone calling, scheduled background actions and custom integrations are additional capabilities, not implied by this setup.
