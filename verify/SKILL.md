---
name: verify
description: Checks each claim or change in a piece of work against evidence (run the tests, grep the code, read file:line) and reports every claim as confirmed, wrong or unconfirmed. Use it whenever the user types /verify, or asks to double-check, fact-check, sanity-check or "make sure that's actually true" about a report, a summary of a long agent run, a migration status, a code review (including findings from Codex or another model), a README or doc, or Claude's own last answer, even if they don't say "verify". Report-only: it never fixes what it finds.
---

# /verify

Opus 5.5's findings hold up well when it checks claims against evidence. The failure it's prone to is a plausible guess that was never checked: "all tests pass" when nobody ran them, "the old client is gone" when one file still imports it, a review finding about a line that actually handles the case. `/verify` is a second pass that separates what's been shown from what's only been said.

## Input

`/verify [target]`

- **No target:** the claims in the most recent substantive answer or run summary in this conversation.
- **A file:** a report, a TASKS.md, a findings list, a README or doc. Verify it against the code or data it describes.
- **A diff or branch:** the claims in the PR description or commit messages, checked against the diff.
- **Pasted text:** such as review findings from Codex or another model.

If the target is ambiguous, pick the most likely one and name it on the first line of the output.

## Stance

Check the work as if someone else did it and you expect some of it to be wrong. That matters most when the claims are your own from earlier in this conversation, because the pull is to confirm them. A claim's own wording is never evidence for it. "Tests pass" is confirmed by running the tests now, not by the log line that said so.

## Steps

1. **List the claims.** Break the target into atomic, checkable statements and number them. Include implicit "done" claims ("migrated every endpoint" means each endpoint, and nothing still uses the old path). Include counts ("6 tests"), names, paths, line numbers, defaults and versions, because those are where guesses hide. Skip opinions and plans. They aren't true or false yet.
2. **Pick the decisive check for each.** Use the cheapest check that would actually catch the claim being wrong:
   - Behavior ("tests pass", "returns 404") → run it.
   - Absence ("no longer used", "deleted") → search the whole scope, not just the obvious file.
   - Presence at a location ("line 12 does X") → read that location, plus enough around it to see whether something else handles the case.
   - Numbers → count them yourself.
3. **Give a verdict.**
   - **confirmed:** you saw evidence that it's true.
   - **wrong:** you saw evidence that it's false. Say what's actually true.
   - **unconfirmed:** you couldn't settle it (no access, needs credentials, too costly to run). Say where you looked and what would settle it. Unconfirmed is an honest result. Don't round it to confirmed because it sounds right.
   - A claim that's partly true is **wrong**. Say which part holds.
4. **Split the work when it's big.** With more than about 15 claims or many independent areas, hand batches to subagents if you have them. A fresh context has no stake in the original answer. Check each subagent's evidence before accepting its verdicts.

## Rules

- **Read-only.** Don't edit files, fix bugs, commit or push, even when a fix is one line. The user decides what to do with the results, and a verify pass that changes things can't be trusted as a check. Running tests, builds and read-only commands is fine.
- **Evidence you can quote.** Command plus the relevant output lines, or `file:line` plus the code. "Looked fine" isn't evidence.
- Don't stop partway to report progress. Check every claim, then report once.

## Output

1. **One-line tally:** `Verified <target>: N claims, X wrong, Y unconfirmed, Z confirmed.`
2. **A table ordered wrong, then unconfirmed, then confirmed:**

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 3 | legacy_client.py deleted | wrong | still exists: `ls payments/` → `legacy_client.py`; imported at `payments/refunds.py:2` |

Keep each claim to a short paraphrase. Put the evidence in the table, not in prose afterward.

3. **What's actually true** (only if something was wrong): one line per wrong claim, stating the correction plainly.
4. **Also noticed** (optional): serious problems you ran into while checking that the target never claimed anything about, such as a security hole, data loss, or code that can't work as intended. Give one line each, with the same kind of evidence. Only report what you came across. Don't go hunting outside the target for more, and leave out style, nits and minor doc gaps. A verify pass that turns into a second review buries the verdicts the user asked for, but a serious problem you saw and didn't mention is worse.

Nothing else follows. Don't offer to fix; the user will ask.
