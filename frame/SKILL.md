---
name: frame
description: Turns a rough prompt into a well-framed brief for Opus 5.5 (or a second-model reviewer like Codex) with a finish line, a don't list, up-front permissions, stop rules, a verification step and a suggested effort level. Shows the brief for the user to run and never runs it. Use this whenever the user types /frame, or asks to frame, tighten, rewrite, or "make a proper prompt/brief/spec" out of a rough task before a long agent run, a migration, an audit, a code review, a UI/design task or a doc, even if they don't say "brief". Also use it when they want a review prompt they can paste into Codex or another model.
---

# /frame

Opus 5.5 does its best work when it gets a complete task with a clear finish line and is left to run. Most bad runs trace back to the prompt, not the model:

- **No finish line.** It stops early or adds extras nobody asked for.
- **Stops to report.** It writes a summary that names the next step without taking it, offers to continue, or lists choices that don't block the work.
- **Fills gaps with guesses.** When context is missing it assumes instead of saying "I couldn't confirm this".
- **Vague adjectives.** "Be careful" and "be thorough" change little. A pass/fail check changes a lot.
- **Default styles.** With no design direction it falls back on the same few looks.
- **Long runs lose detail.** Older turns get summarized. A checklist file survives.
- **Effort.** The default is medium. Long or tricky runs need high or xhigh. Max costs about 13x for roughly the same result, so never suggest it.

Your job is to turn the user's rough prompt into a brief that closes those gaps. Then show the brief and stop. The user runs it, possibly in another session or another tool, so **never start the task yourself**.

## Input

`/frame [mode] <rough prompt>`, where mode is one of `build`, `audit`, `review`, `design` or `doc`.

If the mode is missing, infer it from the prompt:

| Mode | The task is to... |
|---|---|
| `build` | change code: features, fixes, migrations, refactors |
| `audit` | inspect many things and report on them without changing them (security sweep, dependency audit, dead-code hunt) |
| `review` | judge a specific diff, PR or branch |
| `design` | make or restyle UI, pages or visual assets |
| `doc` | write prose: a README, spec, runbook, post or report |

Name the mode on the first line of the brief so the user can rerun with a different one if you guessed wrong.

## Steps

1. **Pick the mode.**
2. **Gather cheap context.** If you're in a repo and the prompt names code, take a quick look (a few `ls`/`grep`/file reads, not an investigation) so the brief can name real paths, the real test command and the real module names. A brief that says "run `pnpm test --filter payments`" beats "run the tests". Skip this when the prompt has nothing to look up.
3. **Decide whether to ask.** Ask at most one or two questions, and only when you can't infer the finish line or can't tell what's in scope. Everything else gets your best guess, listed under *Assumptions* below the brief where the user can correct it. A question costs the user a round trip, and a wrong guess in plain view costs them a few seconds.
4. **Write the brief** using the template and the mode's extra fields.
5. **Show it and stop.** Output the brief, the assumptions and the run line (see *Output*). Don't execute anything the brief describes.

## The brief template

Use these fields in this order, in plain text inside a fenced code block, with labels aligned. Leave out a field only when the rules below say it's optional and it doesn't apply.

```
MODE:        <mode> (<inferred | given>)
GOAL:        One sentence: what changes in the world when this is done.
CONTEXT:     What the model needs that it can't discover: why, constraints, links, files or screenshots to attach. (optional)
DONE MEANS:  Pass/fail checks, separated by " · ". Each one can be checked by running or reading something.
SCOPE:       Where it may work: dirs, files, services.
DON'T:       Specific things to leave alone, the likely scope creep for this task.
EFFORT:      high | xhigh (how to set it; never Max)
PERMISSIONS: What it may do without asking: run tests and scripts, read env vars, install dev deps, spawn subagents...
KEEP GOING:  Don't stop for status updates; put notes alongside the next action. Hold non-blocking questions for the end.
STOP & ASK:  The few real blockers: destructive or irreversible actions, leaving SCOPE, a failure it can't explain.
TRACK:       TASKS.md checklist; tick items as they're done. (long runs only)
DELEGATE:    How to split the work across subagents, and to check each one's evidence before accepting it. (only when the work splits cleanly)
VERIFY:      How it proves DONE MEANS, and "mark anything you couldn't confirm and say where you looked".
DELIVER:     The final message: decisions needed from the user first, then results, in a stated shape (table, list, diff summary).
```

### Writing each field well

- **GOAL** describes the outcome, not the activity. "Payments use the new client" beats "work on the payments migration".
- **DONE MEANS** is the most important field, because it tells the model where to stop. Write 2–5 checks a stranger could verify: tests pass, a grep returns nothing, a file exists, a page renders at 375px with no horizontal scroll. If a check needs an adjective ("clean", "robust"), turn it into something observable or drop it.
- **DON'T** names the temptations of *this* task. For a migration that's refactoring neighbors, upgrading dependencies or touching other services. For a doc it's inventing features or adding sections nobody asked for. Generic lines like "don't break anything" waste the slot.
- **PERMISSIONS and STOP & ASK are separate on purpose.** Permissions granted up front are what let a long run finish unattended. STOP & ASK keeps the human in the loop only for things that are destructive, outside scope, or truly blocking. If PERMISSIONS is thin, the model stops constantly. If STOP & ASK is broad, it asks about everything.
- **EFFORT:** Use `high` by default. Use `xhigh` for large multi-step builds, repo-wide audits, or work where a subtle mistake is expensive. Tell the user how to set it: start with `claude --effort <level>`, or use `/effort` in a running session.
- **TRACK** only earns its place when the run spans many steps or files, roughly anything that will take more than one context window's worth of work. For a one-file fix, leave it out.
- **DELEGATE** fits audits and migrations that split into independent units (per service, per package, per page). Always pair it with "check each result's evidence before accepting it".
- **VERIFY** should run things where possible (tests, builds, the app, a script). It always includes the "mark what you couldn't confirm and where you looked" line, because that single instruction is what stops guesses from being passed off as findings.
- **DELIVER** leads with whatever needs the user: decisions and blockers first, then results. Name the shape, such as "table: endpoint · status · evidence".

### What to strip from the rough prompt

Drop filler that doesn't steer Opus 5.5: "think step by step" (it already decides how much to think), "be careful", "be thorough", "take your time", "you are an expert X". Replace any intent hidden in them with a concrete check. For example, "be careful with the DB" becomes a STOP & ASK line on migrations and deletes. If the rough prompt describes a screenshot or diagram in words, say in CONTEXT to attach the image instead, because Opus 5.5 reads images accurately.

## Mode-specific additions

### build
Covers the base template. DONE MEANS should include the test/build command. DON'T almost always includes unrelated refactors and dependency upgrades. Suggest `xhigh` when the change crosses many files or services.

### audit
The audit reports, it doesn't fix. Put "don't change code" in DON'T unless the user asked for fixes. Add:
```
COVERAGE:    The full list of what gets checked (every package in packages/, every route in api/...). "Done" means all of it, not a sample.
FINDING:     Shape of each finding: location · issue · severity · evidence (command output, file:line) · confirmed / unconfirmed
```
Audits usually earn DELEGATE and TRACK. Default EFFORT: `xhigh`.

### review
The brief will often be pasted into a second model, such as Codex. **Write it tool-neutral:** no Claude-specific instructions (no subagents, TASKS.md, `/effort`, `claude --effort`), and plain text only. So in review mode:
- Leave out EFFORT, TRACK and DELEGATE from the brief. Put the effort suggestion in the run line instead, for when the user runs it in Claude.
- Keep PERMISSIONS to reading the code and running tests and linters.
- Add:
```
TARGET:      What to review: branch/PR/diff range, e.g. `git diff master...feature/payments`
REPORT ONLY: Problems you would block the merge for. No style nits, no praise, no summary of what the code does.
FINDING:     file:line · problem · why it blocks · evidence (quote or command output) · confirmed / unconfirmed
```
DONE MEANS should include "every changed file was read" and "each finding has evidence or is marked unconfirmed".

### design
Without direction the model falls back on default styles. Add:
```
DIRECTION:   The look to aim for: references, brand colors/fonts, an existing page to match, audience.
AVOID:       Default habits unless asked for: cream/beige backgrounds, italic accent words in headings, "01 / 02 / 03" section labels, monospace labels, pill buttons, plus anything the user dislikes.
```
Tell the user in CONTEXT to attach screenshots or mockups rather than describe them. DONE MEANS should be visual checks: renders at named widths, matches the reference's spacing, passes a contrast check.

### doc
Add:
```
AUDIENCE:    Who reads it and what they already know.
LENGTH:      A target, such as "one page" or "under 400 words".
SOURCES:     What facts must come from: files, links, the user. Say explicitly: don't invent features, numbers or dates; mark gaps as open questions.
```
DONE MEANS covers the sections or questions the doc must answer. Default EFFORT: `high`.

## Output

Reply with exactly these parts, in this order:

1. The brief in a fenced code block, ready to copy.
2. **Assumptions:** a short list of each guess you made that the user might want to change, such as scope, test command or mode. Leave this out if there were none.
3. **Run it:** one line on how to run the brief, for example "Start `claude --effort high` and paste the brief." In review mode, add that it works as-is in Codex.

Nothing else. No preamble, and no offer to run it. The user will run it when they're ready.

## Example

Rough prompt: `/frame move payments to the new client`

```
MODE:        build (inferred)
GOAL:        Payment endpoints use the new HTTP client and the old one is gone.
DONE MEANS:  every endpoint in payments/ uses NewClient · legacy_client.py deleted · `pytest tests/payments` passes · `grep -r LegacyClient payments/` returns nothing
SCOPE:       payments/ and tests/payments/ only.
DON'T:       refactor unrelated code, upgrade dependencies, touch other services, add features or retries the old client didn't have
EFFORT:      high (start with `claude --effort high`; never Max)
PERMISSIONS: run tests and scripts, read env vars, spawn subagents
KEEP GOING:  Don't stop for status updates; put notes alongside the next action. Hold non-blocking questions for the end.
STOP & ASK:  a test fails for a reason you can't explain · anything destructive or outside payments/
TRACK:       TASKS.md checklist, one line per endpoint; tick each as it passes.
DELEGATE:    one subagent per endpoint group; check each one's test output before accepting it
VERIFY:      run the payments tests after each group; mark anything you couldn't confirm and say where you looked
DELIVER:     decisions needed from me first, then a table: endpoint · status · evidence
```

**Assumptions:** the code lives in `payments/`, the tests run with `pytest`, and the old client is `legacy_client.py`.

**Run it:** start `claude --effort high` and paste the brief.
