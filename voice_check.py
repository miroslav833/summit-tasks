# Voice check against Humanize.md sections 8.3, 9 and 10.
# The em-dash detector in section 3 passes text that still reads as AI, so this
# checks sentence SHAPE, which is what the Summit AI Authorship gate reacts to.
import json, re, sys

SHAPE = [
    (r"(?<!FINAL):\s*[a-z]",          "colon introducing an explanation or list (section 9 rule 6, 8.3)"),
    (r';',                              "semicolon list (not in Miroslav's writing)"),
    (r'\b(?:is|are|was|were) not [a-z ]{2,30},\s*(?:it|they|but)\b', "antithesis 'is not X, it is Y' (8.3)"),
    (r'\brather than\b',                "'rather than' antithesis (8.3)"),
    (r'\b(?:Any one of these|Either of these|One of the following)\b', "scaffold lead-in"),
    (r'\bdoes not count\b|\bearns nothing here\b|\bfails here\b', "punchy verdict closer (8.3)"),
    (r'^(?:Step|Setting|Context|Background|Objective) \d*:?', "scaffold label (section 2)"),
]
REGISTER = r'\b(comprehensive|robust|leverage|delve|crucial|seamless|holistic|furthermore|moreover|ensure that|it is important|utilize|notably|essentially|ultimately|straightforward|nuanced|thus|hence|subsequently|approximately|numerous|prior to|in order to|demonstrate|facilitate|underscore|encompass|constitute)\b'
TELLS = {"em dash": "—", "en dash": "–", "curly quote": "’",
         "curly dquote": "“", "zero width space": "​"}

def check(name, text):
    bad = []
    for k, v in TELLS.items():
        if v in text: bad.append(f"{k} x{text.count(v)}")
    for w in re.findall(REGISTER, text, re.I): bad.append(f"register word '{w}'")
    for pat, why in SHAPE:
        for m in re.findall(pat, text, re.M):
            bad.append(f"{why}: ...{m if isinstance(m,str) else m}...")
    # section 10: sentences must join related facts, not one fact each
    sents = [x for x in re.split(r'(?<=[.!?])\s+', text) if len(x.split()) > 3]
    if sents:
        mean = sum(len(x.split()) for x in sents) / len(sents)
        joiners = len(re.findall(r'\b(and|because|while|where|which|so|then)\b', text, re.I))
        if mean < 20 and len(sents) > 2:
            bad.append(f"sentences too short, mean {mean:.1f} words (section 10 says this still reads as AI)")
        if joiners < len(sents):
            bad.append(f"too few joining words, {joiners} for {len(sents)} sentences (section 10)")
    return bad

t = json.load(sys.stdin if sys.argv[1] == "-" else open(sys.argv[1]))["task"]
fields = {"questionText": t["questionText"], "solution": t["solution"],
          "references": t["references"], "imageNecessity": t.get("imageNecessityExplanation", "")}
for c in t["rubric"]["criteria"]: fields[f"rubric {c['id']}"] = c["description"]
fail = False
for n, v in fields.items():
    bad = check(n, v)
    print(f"{n:18s} {'CLEAN' if not bad else ''}")
    for b in bad:
        print(f"    {b}"); fail = True
sys.exit(1 if fail else 0)
