# Changelog

## 3.3.1 — 2026-10-18
- Self-check: options only when the owner asked; overwrite/delete actions off by default with a risk and test; "with tests" means a passing-tests requirement (found by the first Hermes test on a local model).

## 3.3.0 — 2026-10-18
- One strict template for every agent job (`templates/general-template.md`): GOAL as "Your task is to … so that …", 8 STRICT RULES (scope, baseline first, research first, proof, no guessing, no secrets, stop), SPECIFICS (inputs, outputs, options with defaults, exclusions, data types, environment, compatibility target), APPROACH, RISKS, WORKING BEHAVIOUR, BEFORE YOU FINISH; ROLLBACK for infra and real devices; PHASES and FIRST DELIVERABLE for big projects. Every block is always present; small jobs use fewer lines per block.
- Medium form for OpenCode, Hermes, OpenClaw and local models: the same rules in fewer words.
- `references/working-behaviour.md`: approval rule per job type (read-only, code changes, infra, real devices, security testing, publish).
- Preset 13: big project / new product, phased, with one approval after research and design.
- Independent judgement: improvements go to the owner as SUGGESTIONS and enter the prompt only after a yes (hard rule 2); spelling and grammar mistakes are read for meaning.
- Lint: enforces every block, `Req N:` per requirement, ROLLBACK for infra/devices, no unfilled placeholders (`--template` for templates), GOAL "so that", SPECIFICS lines, phase criteria and length.
- `apb`: plan screen with SUGGESTIONS and job type; writes with the template.
- Security presets rebuilt in the template.
- Specific example files removed; the template and the presets are the reference.
- Evals: 2 new cases (big project, suggestions); 14 in total, new published run.

## 3.2.0 — 2026-10-18
- General prompts: new presets for app/chatbot system prompts, JSON extraction, summarise/classify and writing (task-types.md 9–12), with a system-prompt example and test set.
- New patterns with sources: few-shot examples, long input first, quote first, positive format instructions, schema-constrained output, state each instruction once, stable content first; avoid prefill on recent Claude models.
- `scripts/apb.py`: command-line builder for any OpenAI-compatible API (local or cloud): shows what it understood, the plan, questions with defaults and UNVERIFIED items; one approval; writes, lints and self-fixes the prompt; saves it. `evals/run_apb.py` runs the 12 evals through it.
- `scripts/lint_prompt.py`: checks any prompt for missing structure and known bad patterns (Python standard library), with unit tests.
- `evals/`: 12 behaviour tests, a grader and two published runs (9/12, then 12/12 after the fixes they found; see evals/README.md).
- Security presets now include VERIFICATION and STOP WHEN (found by the lint).
- Worked example now has its ROLE line, matching the template.
- README: OpenClaw install and use.

## 3.1.0 — 2026-10-18
- Template: new ROLE, SOURCES, OPTIONS, STANDARDS and BEFORE YOU FINISH blocks.
- New references: prompt-patterns.md (use/avoid, with sources), task-types.md (8 presets), security-prompts.md (code review, AI agent audit, authorised pentest, secrets scan).
- "Improve an existing prompt" mode and a before/after example.
- Writing rules updated to current Anthropic and OpenAI guidance.

## 3.0.0 — 2026-10-18
- First public release.
- Universal core: procedure, template, writing rules, self-check.
- 7 hard rules.
- Delivery rules (plan file, single follow-up message, wait during test runs).
- Environment details moved to an optional, private `lab-profile.md` (template included).
- Prompt formats per agent type in `references/agent-formats.md`.
- Worked example; README in English.
