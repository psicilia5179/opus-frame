# opus-frame

Two [Claude Code](https://claude.com/claude-code) skills for working with Opus 5.5:

- **`/opus-frame`** turns a rough prompt into a brief that Opus 5.5 can run to the end without stalling.
- **`/opus-verify`** checks the claims in finished work against the code and marks each one confirmed, wrong or unconfirmed.

Most bad agent runs trace back to the prompt, not the model. If the prompt has no finish line, the model stops early or keeps going past the goal. When context is missing, it guesses. Telling it to "be thorough" changes little. Long runs lose detail when older turns get summarized. These skills target those failure modes, following Anthropic's [Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) and [Theo's breakdown of it](https://youtu.be/ejjBbaq9RmY).

## /opus-frame

```
/opus-frame [build|audit|review|design|doc] <rough prompt>
```

It shows a brief and stops. You run the brief yourself, in this session, a new one, or another tool. When you leave the mode out, the skill infers it from the prompt.

Each brief is a fenced block with fixed fields:

```
MODE:        audit (inferred)
GOAL:        Every Express route in src/routes is known to have, or lack, an auth check.
DONE MEANS:  All 40 route files listed · each route marked protected / unprotected / unclear · every finding cites file:line
SCOPE:       src/routes, src/middleware (read only)
DON'T:       Change code · fix what you find · sample instead of covering every file
EFFORT:      xhigh (start with `claude --effort xhigh`)
PERMISSIONS: Read any file, run grep and the test suite, spawn subagents
STOP & ASK:  A route whose auth depends on config you can't read
DELEGATE:    One subagent per route directory; check each one's evidence before accepting it
VERIFY:      Re-open every unprotected finding at its file:line. Mark anything you couldn't confirm and say where you looked.
DELIVER:     Table: route · method · status · evidence, unprotected routes first
```

(Shortened. The full template, and the rules for writing each field, are in [`opus-frame/SKILL.md`](opus-frame/SKILL.md).)

Some details:

- **DONE MEANS** holds pass/fail checks a stranger could verify. It is the field that tells the model where to stop.
- **PERMISSIONS** and **STOP & ASK** are separate fields. Permissions granted up front let a long run finish unattended. STOP & ASK is kept to real blockers.
- Filler like "think step by step" and "be careful" is removed and replaced with concrete checks.
- Effort is `high` by default, `xhigh` for large or risky work, and never Max.
- `review` mode writes a plain-text brief that also works in Codex or another model as a second reviewer.

## /opus-verify

```
/opus-verify [report | diff | review | doc]
```

With no target, it checks Claude's last answer. It lists every factual claim and checks each one by reading the file or running the command. Each claim is reported as **wrong**, **unconfirmed** or **confirmed**, with `file:line` or command output as evidence. It is read-only and never fixes anything.

## Optional CLAUDE.md block

`claude-md/opus-block.md` holds three standing instructions for `~/.claude/CLAUDE.md`:

- Keep going when a step doesn't need input.
- Treat an answered question as done.
- Keep a `TASKS.md` checklist on long runs.

The installer adds the block only when asked.

## Install

Requires Claude Code, bash and Python 3. On Windows, run it from Git Bash.

```bash
git clone https://github.com/psicilia5179/opus-frame.git
cd opus-frame
./install.sh               # links both skills into ~/.claude/skills/
./install.sh --claude-md   # same, and adds the CLAUDE.md block (backs the file up first)
```

The skills are linked, so `git pull` updates them. Where symlinks aren't available (Git Bash on Windows without Developer Mode), the installer copies them instead and says so; rerun it after `git pull`. Rerunning `--claude-md` replaces the block between its markers instead of adding a second copy.

## Evals

Each skill has test prompts in `evals/evals.json`. `/opus-verify` also has a small fixture repo with planted wrong claims, plus the ground truth for each one. `opus-frame/evals/grade.py <iteration-dir>` scores a set of `/opus-frame` outputs against per-prompt checks.

## Tips

- Opus 5.5 defaults to medium effort. Raise it for long runs: `claude --effort high`.
- Flagged messages can move a session to an older model mid-run. After a long run, check `/model`, or turn off automatic switching in settings.

## License

MIT
