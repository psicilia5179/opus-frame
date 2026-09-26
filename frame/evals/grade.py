"""Grade /frame outputs: python frame/evals/grade.py <iteration-dir>"""
import json, re, sys, pathlib

def brief_of(text):
    m = re.search(r"```[^\n]*\n(.*?)```", text, re.S)
    return m.group(1) if m else ""

def has(p, s): return re.search(p, s, re.I | re.S | re.M) is not None

COMMON = [
    ("Brief is in a fenced code block", lambda t, b: bool(b.strip())),
    ("Brief has a pass/fail DONE MEANS field", lambda t, b: has(r"^\s*DONE MEANS:", b.replace("\r", "")) if b else False),
    ("Brief has an explicit DON'T list", lambda t, b: has(r"^\s*DON'?T:", b)),
    ("PERMISSIONS and STOP & ASK are separate fields", lambda t, b: has(r"^\s*PERMISSIONS:", b) and has(r"^\s*STOP (&|AND) ASK:", b)),
    ("Brief asks to mark unconfirmed items and say where it looked", lambda t, b: has(r"(couldn'?t|could not|can'?t|unable to) confirm", b) and has(r"where (you|it) looked", b)),
    ("Filler stripped from the brief (no 'think step by step' / 'be careful' / 'be thorough')", lambda t, b: bool(b) and not has(r"think step by step|be careful|be thorough", b)),
    ("Never recommends Max effort", lambda t, b: not has(r"(effort|use|set)[^\n]{0,20}\bmax\b(?![^\n]{0,15}(never|not|no))", t) or has(r"never max", t)),
    ("Reply doesn't offer to run the brief itself", lambda t, b: not has(r"(want|shall|should) me to (run|start|execute|kick)", t)),
]

SPECIFIC = {
    "eval-1-audit-auth-routes": [
        ("Mode is audit", lambda t, b: has(r"MODE:\s*audit", b)),
        ("Tells the model not to change code", lambda t, b: has(r"(don'?t|do not|no)\b[^\n]{0,40}(change|modify|edit|fix)", b)),
        ("Coverage is every route file, not a sample", lambda t, b: has(r"(every|all)[^\n]{0,40}(route|file)", b)),
        ("Each finding needs file:line evidence", lambda t, b: has(r"file:line|file\s*:\s*line", b) and has(r"evidence", b)),
        ("Suggests xhigh effort", lambda t, b: has(r"xhigh", t)),
    ],
    "eval-2-review-for-codex": [
        ("Mode is review", lambda t, b: has(r"MODE:\s*review", b)),
        ("Brief is tool-neutral (no subagents, TASKS.md or --effort in it)", lambda t, b: bool(b) and not has(r"subagent|TASKS\.md|--effort|/effort", b)),
        ("Only merge-blocking problems are reported", lambda t, b: has(r"block[^\n]{0,20}merge|merge[- ]block", b)),
        ("Names the diff target against main", lambda t, b: has(r"main\.\.\.?feature/stripe-webhooks|feature/stripe-webhooks", b)),
        ("Says the brief works in Codex", lambda t, b: has(r"codex", t)),
    ],
    "eval-3-design-landing-page": [
        ("Mode is design", lambda t, b: has(r"MODE:\s*design", b)),
        ("Has an avoid list of default styles", lambda t, b: has(r"AVOID:", b) and has(r"pill|cream|monospace|01 / 02", b)),
        ("Asks for screenshots or images to be attached", lambda t, b: has(r"(attach|screenshot)", b)),
        ("Done checks are visual and concrete (named widths)", lambda t, b: has(r"\d{3,4}\s*px", b)),
        ("Keeps the hero, schedule and contact form in scope", lambda t, b: has(r"hero", b) and has(r"schedule", b) and has(r"contact", b)),
    ],
}

root = pathlib.Path(sys.argv[1])
for ev in sorted(p for p in root.iterdir() if p.is_dir()):
    for cfg in ("with_skill", "without_skill"):
        run = ev / cfg / "run-1"; f = run / "outputs" / "response.md"
        if not f.exists(): continue
        t = f.read_text(); b = brief_of(t)
        checks = COMMON + SPECIFIC.get(ev.name, [])
        exp = [{"text": n, "passed": bool(fn(t, b)), "evidence": "regex check on response.md" + ("" if b else " (no fenced brief found)")} for n, fn in checks]
        p = sum(e["passed"] for e in exp)
        (run / "grading.json").write_text(json.dumps({"expectations": exp, "summary": {"passed": p, "failed": len(exp) - p, "total": len(exp), "pass_rate": round(p / len(exp), 3)}}, indent=2))
        print(f"{ev.name:22} {cfg:14} {p}/{len(exp)}")
