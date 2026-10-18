# Prompt patterns: use and avoid

Each pattern cites its source. Sources were checked on 2026-10-18; vendors update these guides, so re-check before relying on model-specific advice.

- [A] Anthropic, Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- [O] OpenAI, GPT-5 prompting guide (archived, Aug 2025): https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- [O2] OpenAI, Using GPT-6 (current-model guidance): https://developers.openai.com/api/docs/guides/latest-model
- [O3] OpenAI, Prompt engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- [O4] OpenAI, Structured Outputs: https://developers.openai.com/docs/guides/structured-outputs
- [S] Anthropic, claude-code-security-review (MIT): https://github.com/anthropics/claude-code-security-review

## Use

| Pattern | How to write it | Source |
|---|---|---|
| One role sentence | "You are a senior <domain> engineer experienced in <specific area>." Even one sentence focuses behaviour and tone. | [A] |
| Context and reason | Give the reason behind each constraint; the model generalises from it. | [A] |
| Explicit quality bar | Ask for it directly ("fully featured", "production-ready, PEP 8, docstrings") rather than hoping it is inferred, but pair it with scope limits to avoid over-engineering. | [A] |
| Scope limit | "Only make changes that are directly requested or clearly necessary." | [A] |
| Investigate before answering | "Read a file before making claims about it. Do not speculate about code you have not opened." | [A] |
| Verify at the end | "Before you finish, verify your result against <criteria>." Catches errors reliably in code and maths. | [A] |
| General thinking over scripted steps | "Think carefully about the approach" usually beats a hand-written chain of steps. Use numbered steps only when order or completeness matters. | [A] |
| Tests are not the spec | "Implement a solution that works for all valid inputs, not only the tests. Do not hard-code values. Do not edit or remove tests to make them pass; report tests you believe are wrong." | [A] |
| State in files | Long tasks: structured state in JSON (e.g. tests.json), notes in a text file, checkpoints in git; make incremental progress. | [A] |
| XML or labelled sections | Separate instructions, context, examples and inputs with consistent tags or headings. | [A], [O] |
| Stop criteria and escape hatch | Say when the task is done, when to hand back, and that it may proceed under stated uncertainty. Lower the "ask first" threshold for risky actions (deleting, paying, deploying). | [O] |
| No contradictions | Precise models spend effort reconciling conflicting instructions; review the prompt for conflicts. | [O] |
| Examples (few-shot) | 3–5 examples that mirror the real use, vary enough to cover edge cases, each in `<example>` tags inside `<examples>`. | [A], [O3] |
| Long input first, question last | Put long documents (20k+ tokens) at the top in `<document>` tags with `<source>`; instructions and the question after them ("up to 30 percent" better in Anthropic's tests). | [A] |
| Quote first | For long-document tasks, ask the model to quote the relevant passages first, then answer from them. | [A] |
| Positive format instructions | Say what the output should look like ("flowing prose paragraphs") instead of only what to avoid; the prompt's own style influences the output's. | [A] |
| Schema-constrained output | When the result is parsed by code, give a JSON Schema and use the API's structured-output option where available; it guarantees schema adherence, unlike plain JSON mode. Still validate business rules. | [O4] |
| State each instruction once | Repeating an instruction ("ask first" several times) makes models over-apply it. | [O2] |
| Stable content first | Reusable content (role, rules, reference text) at the beginning, variable input at the end; this also enables prompt caching. | [O3] |
| Match the model type | Reasoning models do better with high-level goals; non-reasoning models need precise, step-level instructions. | [O3] |
| Strict, checkable rules | A short STRICT RULES list, each rule firm, stated once and checkable (scope, proof, no guessing, stop). Firm wording for real limits, calm wording elsewhere. | [A], [O2] |
| Goal with its result | "Your task is to <action> <what> so that <result>": the result is what VERIFICATION checks. | — (template convention) |
| Baseline first | Record the current state (versions, config, test results) before changing anything, so nothing is assumed and there is a "before" to compare. | — (template convention) |
| Rollback before change | For infra and real devices, write how to undo each change before making it. | — (template convention) |
| Budget | A maximum time or number of attempts, so long tasks plan for limits instead of being cut off. | — (template convention) |
| Options with defaults | List owner-adjustable settings with defaults so the agent never has to guess. | — (template convention) |
| High-confidence findings only | For reviews: report only issues above a stated confidence, with a concrete scenario, and filter false positives in a separate step. | [S] |

## Avoid (and what to write instead)

| Avoid | Why | Write instead |
|---|---|---|
| "You are Claude, a large language model by Anthropic" / "You are GPT…" | The agent already knows its identity from its own system prompt, and the line is false when the agent runs another model (e.g. a local model in OpenCode). | One expertise role sentence; a role in the system prompt focuses behaviour [A]. |
| "World-leading expert", "flawless", "absolute best", "brilliant" | Hype carries no testable information. | A concrete STANDARDS list. |
| CRITICAL / MUST / NEVER in caps everywhere | Current models over-react to aggressive wording (over-triggering tools, over-searching). [A], [O] | Calm wording with a reason. Keep firm wording only for real hard limits. |
| "Be THOROUGH" | Made GPT-5 over-use search on small tasks in Cursor's testing. [O] | Say what thoroughness means for this task. |
| "Never include caveats" / "Never explain the problem" | Hides uncertainty and errors; breaks the UNVERIFIED rule. | "Report briefly what you could not verify." |
| "Mentally walk through 8 steps…", "consider three approaches" | Hand-written step rituals usually underperform general instructions; some newest models may decline prompts that ask them to write out their reasoning and rely on built-in thinking instead. [A] | "Think carefully about the approach, then verify against <criteria> before finishing." |
| "Test your changes" + "output only the final script" | Contradiction: testing needs running and reporting. | Allow running tests; specify the final deliverable and a short test report. |
| "If the result can be improved, you MUST improve it" | No stop condition; invites endless rework. | A STOP WHEN line with measurable criteria. |
| "If in doubt, use <tool>" | Causes over-triggering. [A] | State when the tool is appropriate. |
| Several tasks in one prompt ("fix everything") | Scope creep, partial results. | One task; chain prompts for more. |
| Prefilling the assistant's reply (partial last assistant message) on recent Claude models | Returns a 400 error from Claude 4.6 models onward. [A] | Format instructions, or schema-constrained output. |
| Examples that all look alike | The model copies unintended patterns (length, wording, one label). [A] | Vary inputs and outputs; include an edge case. |

## Small local models

- Short, concrete instructions and one example of the output format.
- No long reasoning rituals unless measured to help on that model.
- Compare old vs new prompt on a fixed test set before switching (promptfoo or the project's harness).
