```
ROLE: You are a senior Python engineer experienced in web scraping and HTML parsing.

GOAL: Your task is to build a scraper that collects data from every product page on mysite.com so that it outputs one structured record per product, with no duplicates and no crash on malformed pages.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; change nothing outside SCOPE.
2. Before changing anything, record the current state (versions, config, test results) and report it.
3. Research before deciding: read the files and the SOURCES first; never make a claim about a file you have not read.
4. Every requirement must pass its VERIFICATION check; show the command, exit code and key output line.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark a step done without proof.
7. Never read or print secrets; never touch other projects, services or settings outside SCOPE.
8. Stop exactly at STOP WHEN; no extra work and no unrequested changes.

CONTEXT
- "mysite.com" is a placeholder domain (source: owner's request) — replace with the real site before running.
- Why it matters: the scraper must target the actual site and respect its own robots.txt and terms.

SOURCES (use these; do not substitute others)
- https://docs.python-requests.org/ — HTTP requests
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/ — HTML parsing (or Scrapy's docs if that is chosen in APPROACH)
- <real-domain>/robots.txt — crawl rules; read before writing any request logic

SPECIFICS
- Inputs: the site's sitemap.xml and/or category/listing pages (starting URL(s) to be set to the real domain)
- Outputs: one record per product in JSON (default) or CSV: name, price, URL, SKU/ID [exact field list to be confirmed by owner]
- Options: output format: json|csv [default: json]; request delay: seconds between requests [default: 1]; max pages [default: unlimited, follow sitemap/pagination to the end]
- Exclusions: non-product pages (blog, account, cart, search); any path disallowed by robots.txt
- Data types / formats: price as a decimal string with currency symbol kept as shown on the page; URLs absolute
- Environment: Python 3.x, local machine
- Compatibility target: n/a

STANDARDS
- PEP 8, type hints, docstrings; respect robots.txt and a rate limit; retry with backoff on transient (5xx/timeout) errors; no new dependencies outside requests / BeautifulSoup4 / Scrapy without asking first.

APPROACH
- Compare requests+BeautifulSoup (simpler, fine for a few hundred pages) against Scrapy (built-in concurrency, retry, pagination) against the real site's size and structure; pick one and state why in one line before starting.

REQUIREMENTS
1. Discover all product URLs (sitemap.xml if present, else category/pagination crawl).
2. Parse each product page into the defined fields; skip pages that don't match the product template instead of crashing.
3. De-duplicate output by product URL/ID.
4. Follow pagination (or infinite-scroll's underlying API/next-page links) to the end of each category.
5. Respect robots.txt and the configured request delay.
6. Write the output file in the chosen format; log every skipped/failed page with its reason.

RISKS
- Page structure varies across categories → Req 2 skips non-matching pages without crashing.
- Anti-bot blocking or rate limiting → Req 5's delay and backoff; test: a full run produces no cascading 429/503 failures.
- Pagination missed → Req 4; test: total scraped count matches the sitemap/category count.
- robots.txt disallows some paths → Req 5; test: disallowed paths are absent from the output and appear in the skip log.

CONSTRAINTS
- Scope: this scraper script, its config and its output/log files only.
- Do not: ignore robots.txt or the site's terms of service — because that risks legal or access problems.
- Do not: send concurrent requests beyond the configured limit — because it can look like a denial-of-service and get the IP blocked.
- Dependencies: requests, beautifulsoup4 (or scrapy, whichever APPROACH picks) — approved; anything else needs a yes.

VERIFICATION (one line per requirement)
- Req 1: run the discovery step against the real sitemap/category pages → discovered URL count reported and > 0.
- Req 2: run on a sample of 10 product pages → 10 valid records, 0 crashes.
- Req 3: check the output file for duplicate URLs → none found.
- Req 4: run on one multi-page category → every page's products appear, not only page 1.
- Req 5: compare output URLs against robots.txt disallow rules → no disallowed path present; log shows the delay was applied.
- Req 6: open the output file → it parses as valid JSON/CSV; the skip log lists every page skipped with a reason.

WORKING BEHAVIOUR (code changes in one project)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. This approval covers the whole plan in this prompt; work without asking again, touching only this script and its output.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: a new dependency outside the approved list, anything outside SCOPE, deleting files.
6. Budget: one working session.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track steps in progress.md with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; mark [x] only with command, exit code and key output line.

OUTPUT: the scraper script, how to run it, a sample of the first 3 output records, and the test report (command, exit code, key line), then the limitations.

STOP WHEN: every discoverable product page has been attempted once, the output file is written, and the skip log accounts for every page not scraped.

UNVERIFIED: the real domain to use in place of "mysite.com"; the exact product fields wanted; whether that domain's robots.txt allows this; target agent/model to run this prompt (assumed a capable coding agent — full form).
```

Changes from your draft: removed the model-identity line ("You are GPT-4") and hype ("best coder in the world") for one plain role sentence; removed the open-ended "NEVER stop until it is perfect" (no stop condition, invites endless rework) for a concrete STOP WHEN; removed "Don't explain anything" (hides failures) for a short required OUTPUT report; added the missing SPECIFICS, STANDARDS, RISKS, CONSTRAINTS (robots.txt/rate-limit) and VERIFICATION blocks.

UNVERIFIED: real target domain, exact fields, robots.txt rules, intended agent. Owner decision needed: confirm these before running. No unapproved suggestions beyond what's listed above.
