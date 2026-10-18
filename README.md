# agent-prompt-builder

A skill that turns your goal into one strict, precise, verified prompt for an AI agent or any LLM: Claude Code, OpenCode, Hermes, OpenClaw, Codex, a local model. It covers agent tasks (build, debug, research, ML, infra, real devices, security, big projects) and general prompts (chatbot system prompts, JSON extraction, summaries, classification, writing). Every fact in the prompt is verified or marked `UNVERIFIED`, so the agent never works from guesses.

It comes with a **command-line tool** (`apb`) that works without any agent, a **lint script** that checks any prompt against the rules, and **behaviour evals** you can rerun on your own agent and model.

## Why

Agents fail most often because the prompt was vague, invented a path or flag, left out the exact inputs and outputs, mixed several tasks, or never said how to prove the result or when to stop. This skill fixes that with a fixed procedure, 7 hard rules, one strict template, an approval rule per job type, and a lint that enforces all of it.

## What is inside

```
agent-prompt-builder/              ← the skill folder (copy this)
├── SKILL.md                       ← instructions the agent follows
├── lab-profile.template.md        ← blank profile for your own setup
├── scripts/
│   ├── apb.py                     ← command line: goal → plan → one approval → linted prompt
│   └── lint_prompt.py             ← checks a prompt against the rules (Python 3.8+, no dependencies)
├── templates/
│   └── general-template.md        ← THE template: full form, medium form (local models), start prompt
└── references/
    ├── agent-formats.md           ← which form each agent gets
    ├── task-types.md              ← 13 presets: build, debug, refactor, research, ML/data, docs, infra,
    │                                 security, app system prompt, JSON extraction, summarise/classify,
    │                                 writing, big project / new product (phased)
    ├── working-behaviour.md       ← approval rule per job type: read-only, code, infra, real devices,
    │                                 security, publish
    ├── security-prompts.md        ← code security review, AI agent audit, authorised pentest, secrets scan
    └── prompt-patterns.md         ← what to use and avoid in prompts, with sources
evals/                             ← 14 behaviour tests, grader and published results
tests/                             ← unit tests for the lint script and apb
```

## Prompt structure

Every agent prompt uses the same blocks, in this order (full template: [general-template.md](agent-prompt-builder/templates/general-template.md)). A small job keeps every block with one or two lines each; a big job uses more lines.

| Block | Purpose |
|---|---|
| ROLE | One sentence naming the expertise the task needs |
| GOAL | "Your task is to <action> <what> so that <result>" |
| STRICT RULES | 8 mandatory, checkable rules: scope, baseline first, research first, proof, no guessing, no done without proof, no secrets, stop |
| CONTEXT | Verified facts, each with its source |
| SOURCES | Repos, docs or pages the agent must use |
| SPECIFICS | Inputs, outputs, options with defaults, exclusions, data types, environment, compatibility target |
| STANDARDS | Quality bar (style guide, docstrings, KISS, production-ready, dependencies) |
| APPROACH | Options compared against criteria; one chosen with a reason |
| REQUIREMENTS | Numbered, each one testable |
| RISKS | Weaknesses and edge cases, each covered by a test |
| CONSTRAINTS | Allowed scope and forbidden actions, each with a reason |
| VERIFICATION | One proof per requirement (command → pass condition) |
| WORKING BEHAVIOUR | Approval rule for the job type, debug-and-retest, suggestions, budget, independent review |
| ROLLBACK | How to undo each change (infra and real devices only) |
| PHASES + FIRST DELIVERABLE | Research and design first, one approval, then build (big projects only) |
| BEFORE YOU FINISH | Self-criticism against VERIFICATION and STANDARDS; fix every flaw |
| PROGRESS | Ticks in a file, done only with proof |
| OUTPUT | Exact deliverable, report and limitations |
| STOP WHEN | The done condition |
| UNVERIFIED | Assumptions the agent checks first |

The patterns follow [Anthropic's prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and OpenAI's guides ([prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [current model](https://developers.openai.com/api/docs/guides/latest-model)). Strict means checkable: firm rules stated once, every requirement proven, hidden "mentally walk through…" steps replaced by written APPROACH, RISKS and BEFORE YOU FINISH checks, and uncertainty reported as UNVERIFIED instead of "never include caveats".

## Security prompts

`references/security-prompts.md` has four defensive presets:

1. **Code security review**: modelled on Anthropic's MIT-licensed [claude-code-security-review](https://github.com/anthropics/claude-code-security-review). High-confidence findings only, an exploit scenario per finding, and a false-positive filter.
2. **AI agent / LLM app audit**: mapped to the [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) (prompt injection, excessive agency, system prompt leakage, and more).
3. **Authorised penetration test or infrastructure audit**: requires written authorisation and an explicit scope; read-only and non-destructive by default.
4. **Secrets and dependency check**: reports where secrets are, never their values.

The skill asks you to confirm authorisation and scope before writing presets 2–4.

## Install

First get the files (Mac, Linux or Windows, with git installed):

```
git clone https://github.com/marmixes/agent-prompt-builder.git
```

Then copy the inner `agent-prompt-builder` folder to your agent's skills folder. The folder name must stay `agent-prompt-builder` (OpenCode requires it to match the skill name).

| Agent | Personal (all projects) | One project only | Source |
|---|---|---|---|
| Claude Code | `~/.claude/skills/agent-prompt-builder/` | `.claude/skills/agent-prompt-builder/` | [docs](https://code.claude.com/docs/en/skills) |
| OpenCode | `~/.config/opencode/skills/agent-prompt-builder/` (also reads `~/.claude/skills/` and `~/.agents/skills/`) | `.opencode/skills/agent-prompt-builder/` | [docs](https://opencode.ai/docs/skills) |
| Hermes Agent | `~/.hermes/skills/agent-prompt-builder/` | — | [docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| OpenClaw | `~/.agents/skills/agent-prompt-builder/` (shared with OpenCode) | `<workspace>/skills/agent-prompt-builder/` | [docs](https://docs.openclaw.ai/tools/skills.md) |
| Any chat LLM | paste `SKILL.md` as the first message (or system prompt) | — | — |

`~` is your home folder: `/Users/<you>` on Mac, `/home/<you>` on Linux, `C:\Users\<you>` on Windows.

**Mac / Linux** (Claude Code example):
```
mkdir -p ~/.claude/skills
cp -r agent-prompt-builder/agent-prompt-builder ~/.claude/skills/
```

**Windows PowerShell** (Claude Code example):
```
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Copy-Item -Recurse agent-prompt-builder\agent-prompt-builder "$HOME\.claude\skills\"
```

**One copy for all three agents:** install once in `~/.claude/skills/`. OpenCode reads it automatically. For Hermes, add it to `~/.hermes/config.yaml`:
```yaml
skills:
  external_dirs:
    - ~/.claude/skills
```

Restart the agent after installing.

## Use

| Agent | How to call it |
|---|---|
| Claude Code | `/agent-prompt-builder <your goal>`, or just ask "write a prompt for Claude Code to …" (it loads automatically) |
| OpenCode | `/agent-prompt-builder <your goal>`, or ask in plain words (the agent loads it with its `skill` tool) |
| Hermes | `/agent-prompt-builder <your goal>` |
| OpenClaw | `/agent-prompt-builder <your goal>` or `$agent-prompt-builder` (picked up on the next turn; no restart) |

Example request:
> Write a prompt for Claude Code: add a /health endpoint to my FastAPI app so Docker can restart it when it hangs.

To improve a prompt you already have, paste it and ask "improve this prompt". You get the rewritten prompt and a one-line reason for each change; every specific in your prompt (sources, options, data types, targets) is kept.

When you can answer, the agent first shows one plan screen (what it understood, the plan, its suggestions, questions with defaults, what is UNVERIFIED) and you approve once. The answer is then the finished prompt in one code block, plus up to 4 lines: how to deliver it, what is UNVERIFIED, what you must decide, and suggestions you have not approved yet.

## How the agent works when it runs this skill

1. **Reads your setup** (if present): `lab-profile.md`, then the project's `AGENTS.md`, `CLAUDE.md`, `LESSONS.md`, plan and `PROGRESS.md`.
2. **Understands your goal**: spelling and grammar mistakes are read for their meaning, never changed; the goal is restated in one sentence. If it could mean two things, it asks you one question and stops.
3. **Picks the target agent's form** (`agent-formats.md`), the **task-type preset** (`task-types.md` or `security-prompts.md`) and the **job type** (`working-behaviour.md`).
4. **Collects facts**: from your files, from official docs (with the URL), or marks them `UNVERIFIED` and adds a step for the target agent to check them.
5. **Collects the specifics**: inputs, outputs, options with defaults, exclusions, data types, environment, compatibility target.
6. **Judges independently**: weak points, conflicts with your rules (reported, never resolved silently), better approaches, which go to you as SUGGESTIONS.
7. **Shows you one plan screen** and takes one approval (skipped when you cannot answer now).
8. **Fills the template** with every block and the approval rule for the job type.
9. **Runs the self-check and the lint**, and fixes every error.
10. **Saves** the prompt if your profile names a prompts folder, then shows it to you.

The agent that receives the prompt then knows exactly: what "done" means, which files it may touch, how to prove each requirement, how to track progress, and when to stop or ask you.

## The 7 hard rules

1. No invented facts: verified or `UNVERIFIED`.
2. The prompt contains only what you approved; its own ideas go to you as suggestions.
3. Every requirement is testable.
4. No secrets requested, read, printed or logged.
5. Conflicts with your rules are reported, never resolved silently.
6. Scope and forbidden actions are explicit, each with its reason.
7. Clear stop condition; after 3 failed attempts at a step, record and move on.

## Customise

Nothing in `SKILL.md` needs editing.

1. **Your environment:** copy `lab-profile.template.md` to `lab-profile.md` in the same folder and fill it in (agents, start commands, machines and paths, secret files to never read, prompts folder). It stays private: `.gitignore` excludes it.
2. **Per project:** put standing rules in the project's `AGENTS.md` / `CLAUDE.md` / `LESSONS.md`. The skill reads and follows them.
3. **Your own agent:** add a row to `references/agent-formats.md` with the form it gets.

## Command line: `apb` (no agent needed)

Type what you need in your own words; spelling mistakes are fine. `apb` shows one screen with what it understood, the best plan, its suggestions, questions with default answers, and what is UNVERIFIED. You approve **once**: press `y`, or type all corrections and answers in one line. It then writes the prompt, lints it, fixes lint errors itself (up to 2 rounds) and saves it to `prompts/`.

```
python3 agent-prompt-builder/scripts/apb.py "make my fastapi app fastr, /search is slow"
```

It works with any OpenAI-compatible API: llama.cpp, vLLM, Ollama, LM Studio, OpenAI, OpenRouter. Python 3.8+, no installs.

| Setting | Flag | Environment variable | Default |
|---|---|---|---|
| API address | `--base-url` | `APB_BASE_URL` | `http://127.0.0.1:8080/v1` |
| Model name | `--model` | `APB_MODEL` | `local` |
| API key | — | `APB_API_KEY` or `OPENAI_API_KEY` | none (read from the environment, never printed or saved) |
| Output folder | `--out` | `APB_OUT` | `prompts` |

Other options: `--file goal.txt`, `-` (goal from stdin), `--yes` (approve automatically; it stops instead if a question has no safe default), `--fix-rounds`, `--timeout`, `--temperature`. Exit codes: 0 saved, 1 error or lint still failing, 3 needs your answer, 4 cancelled.

The result is only as good as the model behind it: a strong model gives better plans than a small local one. Measure yours with `evals/run_apb.py` (below).

## Check a prompt (lint)

Works on any prompt, written by this skill or not:

```
python3 agent-prompt-builder/scripts/lint_prompt.py my-prompt.md
```

It finds the prompt form (full, phased, medium, short, start prompt, system or runtime prompt), checks each ``` block in a Markdown file separately, and reports:

- **Errors** (exit code 1): any missing template block, requirements without a `Req N:` verification line, infra or real-device jobs without ROLLBACK, unfilled `<placeholders>`, a request to print or send a secret, model-identity lines ("You are GPT…"), "never include caveats", open-ended "improve until perfect".
- **Warnings**: a GOAL without "so that", SPECIFICS without inputs, outputs or environment, phases without verification criteria, prompts too long for their form, CAPS shouting, hype words, "Do not" without a reason, scripted "think step by step" rituals, "be thorough", "if in doubt use <tool>", context facts without a source, repeated instructions, and for system prompts a missing "I don't know" fallback or prompt-injection rule.

Options: `--strict` (warnings also fail), `--template` (allow placeholders, for templates), `--json`, `--form`, `-` to read from stdin. The skill runs it on every prompt it writes when the agent can run code.

The lint checks structure and known bad patterns; it cannot tell whether a fact in the prompt is true. That is what the `UNVERIFIED` rule is for.

## Behaviour evals

[evals/](evals/README.md) has 14 fixed requests (clear task, ambiguous goal, secret request, pentest without authorisation, rule conflict, too many tasks, system prompt, extraction, big project, suggestions and more) and a grader:

```
python3 evals/check_evals.py evals/results/<run-name>
```

Run them on your own agent and model and compare with the published results. To test `apb` with your model in one go: `python3 evals/run_apb.py <run-name>`, then grade that folder. Unit tests for the lint and `apb`: `python3 -m unittest discover -s tests`.

## Testing prompts for local models

Before switching a prompt that runs on a local model, compare old and new on a fixed test set, for example with [promptfoo](https://github.com/promptfoo/promptfoo) (MIT, runs locally, works with any OpenAI-compatible API). Keep the change only if it is not worse.

## Contributing

Issues and pull requests are welcome. Keep changes short, testable and consistent with the hard rules.

## Credits

Security preset 1 adapts the review approach of Anthropic's [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) (MIT licence). Prompt patterns cite Anthropic's and OpenAI's public prompting guides; see [prompt-patterns.md](agent-prompt-builder/references/prompt-patterns.md).

## Licence

[MIT](LICENSE)
