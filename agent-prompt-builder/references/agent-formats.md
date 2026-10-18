# Agent formats

Pick the form that matches the target agent. All forms keep the hard rules from SKILL.md; the forms themselves are in [../templates/general-template.md](../templates/general-template.md).

| Target | Form | Why |
|---|---|---|
| Claude Code, Codex, other strong cloud agents | Full form | Strong models handle long structured prompts; every block is checked |
| OpenCode, Hermes, OpenClaw, agents on mid-size or local models | Medium form | Same rules in fewer words; local models follow short, strict prompts better |
| A small local model doing one step (llama.cpp, Ollama, vLLM) | Short form (below) | One task, one output format |
| A plan saved in a file | Start prompt | The plan file holds the full prompt; the message only points to it |
| Any chat LLM without skills support | Full or medium form, pasted as the first message with the files it needs | Facts the model cannot check are marked UNVERIFIED |

Big jobs on local models: split them into several medium prompts, one per step, rather than one long prompt.

## Short form (small local models, one step)

```
Task: <one sentence>.
Input: <what it receives>.
Output: <exact format, ideally with one example>.
Rules:
- <rule> (because <reason>)
- If unsure, answer "UNVERIFIED: <what is unknown>".
```

- No "think step by step" rituals unless measured to help on that model.
- Test old vs new prompt on a fixed set before switching (see SKILL.md).

## Add your own agent

Add a row to the table with your agent's name and the form it gets. Keep the hard rules.
