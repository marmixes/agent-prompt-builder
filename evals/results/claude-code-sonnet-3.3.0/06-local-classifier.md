```
Task: Classify a support ticket into exactly one category: billing, bug, feature, or other.
Input: ticket text (subject + body) at {{TICKET}}.
Output: exactly one word — billing, bug, feature, or other — lowercase, nothing else.
Rules:
- billing: payment, invoice, subscription, refund, or pricing problems. Example: "I was charged twice this month."
- bug: something in the product is broken or behaves incorrectly. Example: "The app crashes when I upload a photo."
- feature: a request for new or changed functionality. Example: "Can you add dark mode?"
- other: anything that does not clearly match the three above — use this rather than forcing a wrong label. Example: "How do I contact sales?"
- Output the label only, no explanation (the caller parses this value directly).
```

VERIFICATION: label at least 20 real tickets by hand first, run them through the model, and report per-label accuracy; keep this prompt only if it's not worse than any earlier version.
UNVERIFIED: whether this 7B model reliably outputs only the bare label (no punctuation/extra words) — check on a handful of real examples.
SUGGESTIONS (not yet approved): if tickets run long, truncate or summarise before {{TICKET}} — small models have limited context.
