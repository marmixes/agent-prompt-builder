```
<document>
<source>Supplier contract, about 60 pages. Paste the full text here, or attach the file, before sending.</source>
{{CONTRACT_TEXT}}
</document>

ROLE: You are a senior commercial contracts analyst experienced in explaining supplier agreements in plain language to non-lawyer managers.

GOAL: Your task is to summarise the contract in the document above for a non-lawyer manager so that every obligation and every deadline in it is listed with its clause reference, in plain language, with nothing added from outside the document.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; use only the text of the document.
2. Before summarising, quote the passages you will rely on (obligations, deadlines, payment, term, termination, penalties, liability), then write from those quotes.
3. Never make a claim about a clause you have not read; read the whole document, including schedules and annexes.
4. Every item must pass its VERIFICATION check; show the check results in the report.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark an item complete without a clause reference.
7. Never invent a date, amount, clause number or party name; if the text does not state it, write "not stated".
8. Stop exactly at STOP WHEN; no extra work.

CONTEXT
- Reader: a manager without legal training who must know what the company has to do, by when, and what happens if it does not (source: the owner request).
- Why it matters: a missed deadline or an overlooked obligation in a supplier contract can cost money or rights; the summary must be complete on those two points before it is short.

SOURCES (use these; do not substitute others)
- The document above only. No web search and no outside legal knowledge.

SPECIFICS
- Inputs: the contract text in the <document> tags, including schedules and annexes.
- Outputs: one summary in the reply, in the OUTPUT format, Markdown, English.
- Options: our side: the party the manager works for [default: the buyer of goods or services; if the document does not make this clear, state the assumption in the first line and mark it UNVERIFIED]; length: summary section up to 400 words, tables as long as needed [default]; quote length: at most 25 words per quote [default].
- Exclusions: legal advice, opinions on whether terms are fair or enforceable, negotiation suggestions, anything about other contracts or law.
- Data types / formats: dates as written in the contract and, where the contract gives a start date, also as YYYY-MM-DD; amounts with currency as written; clause references as "clause 12.3, page 27" (this shows the form only).
- Environment: n/a
- Compatibility target: a manager reading it on one screen or page without a lawyer's help.

STANDARDS
- Plain language: short sentences; each legal term explained in a few words the first time it appears (for example "indemnity: the duty to cover the other side's losses").
- Complete first, short second: list every obligation and deadline; shorten only the wording.
- Neutral: describe what the text says; do not rate it as good or bad.

APPROACH
- One obvious approach: first extract every sentence containing an obligation or time word (shall, must, will, agrees to, is responsible for, within, no later than, before, after, per month, annually, notice) into quotes; then group them by party and by time; then write the summary from the groups.

REQUIREMENTS
1. A parties-and-key-terms block: parties and roles, effective date, term, renewal rule, price and payment terms, termination rights and notice periods, liability limits, penalties, each with its clause reference.
2. An obligations table for our side and, separately, for the other side: obligation in plain words, clause reference, deadline or frequency, consequence of failure (as stated in the text).
3. A deadline list sorted by time: absolute dates first (in date order), then relative deadlines (trigger event plus period, for example "30 days after delivery"); a calendar date is calculated only when the contract states the trigger date.
4. A "check before signing or acting" list of unclear, missing or contradictory points (for example a deadline with no trigger, an undefined term, clauses that conflict), each with its clause reference.
5. Every row in Req 1-4 has a clause reference and page, and a supporting quote of at most 25 words.
6. The plain-language summary at the top is up to 400 words, contains the five most important obligations and the five nearest or most severe deadlines, and uses only facts that appear in the tables.

RISKS
- An obligation hidden in a schedule or definition is missed → covered by Req 2 and the coverage check in VERIFICATION.
- A relative deadline is turned into a wrong calendar date → covered by Req 3.
- A clause is paraphrased so loosely that its meaning changes → covered by Req 5 (quote beside each row).
- Fact invented to fill a gap → covered by STRICT RULE 7 and Req 4.
- Cross-references ("subject to clause 14") change the meaning of a clause and are ignored → covered by Req 4.

CONSTRAINTS
- Scope: this one document, this one summary.
- Do not: add legal advice or opinions on fairness — because the manager needs what the text says and a lawyer must judge the rest.
- Do not: use outside facts, market norms or legal knowledge — because they may not apply to this contract.
- Do not: output personal data beyond names and roles needed to identify the parties — because the summary will be shared inside the company.
- Dependencies: none.

VERIFICATION (one line per requirement)
- Req 1: check the block -> all ten items present, or written as "not stated".
- Req 2: search the document for each obligation or time word from APPROACH -> every hit appears in a table row or in a one-line list titled "considered, not an obligation" with its reason.
- Req 3: check each relative deadline -> trigger, period and clause shown; no calendar date without a stated trigger date.
- Req 4: re-read every cross-reference found in the obligation clauses -> each is either resolved in the table or listed.
- Req 5: pick every quote -> it appears word for word in the document under the cited clause and page.
- Req 6: count words and compare -> at most 400 words, and every fact appears in a table row.

WORKING BEHAVIOUR (read-only)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. No approval is needed: this job only reads and reports; change no files or settings.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, fix, recheck; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: the missing document text or pages you cannot read.
6. Budget: one pass plus one verification pass.
7. At the end: an independent review (fresh reviewer, no prior context) of the summary against the document, then the report.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track the sections of the document (by clause range) in your notes with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; [x] only when every obligation and time word in that range is placed.

OUTPUT: In this order: (1) summary up to 400 words; (2) parties and key terms; (3) obligations tables (our side, other side); (4) deadline list; (5) check-before-acting list; (6) verification results, one line per requirement; then the limitations, including that this is a plain-language summary and not legal advice, and that points in the check-before-acting list should go to a lawyer.

STOP WHEN: Req 1-6 pass their verification and the output is delivered. If the document text is missing or unreadable, stop and report which pages.

UNVERIFIED: which party the manager's company is (if the document does not make it clear), whether the pasted text is complete (all 60 pages, schedules and annexes), and any figure or date that could not be read.
```

I wrote one-off prompt in the full form with the contract pasted at the top, as the skill places long inputs first.
- Decision for you: paste the full contract text in place of {{CONTRACT_TEXT}} and name your company's side if it is not the buyer.
- Suggestion (not in the prompt): a second prompt asking an AI to list clauses to raise with a lawyer, or to compare with your standard terms.
