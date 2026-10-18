import json, re, sys, pathlib
TELLS = {"em dash": "—", "en dash": "–", "curly quote": "’", "curly dquote": "“", "zero width space": "​"}
SCAFFOLD = r"(Setting|Context|Background|What just happened|What you're accountable for|One thing to watch|What's around you|Your task|Objective):"
REGISTER = r"\b(comprehensive|robust|leverage|delve|crucial|seamless|holistic|furthermore|moreover|ensure that|it is important|note that|notably)\b"
root = pathlib.Path(sys.argv[1])
for name in ("task.json", "README.md", "reference.txt"):
    f = root / name
    if not f.exists(): print(name, "missing"); continue
    raw = f.read_text(encoding="utf-8")
    text = json.dumps(json.loads(raw), ensure_ascii=False, indent=1) if name.endswith(".json") else raw
    counts = {k: text.count(v) for k, v in TELLS.items()}
    counts["scaffold label"] = len(re.findall(SCAFFOLD, text))
    counts["register word"] = len(re.findall(REGISTER, text, re.I))
    bad = {k: v for k, v in counts.items() if v}
    print(f"{name}: {'CLEAN' if not bad else bad}")
    for line_no, line in enumerate(text.splitlines(), 1):
        if any(t in line for t in TELLS.values()) or re.search(REGISTER, line, re.I) or re.search(SCAFFOLD, line):
            print(f"   line {line_no}: {line.strip()[:120]}")
