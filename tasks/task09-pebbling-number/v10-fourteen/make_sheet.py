import build_package as b
t = b.task["task"]
lines = ["# Edit sheet: revision of SUM-MVBG0GO3 (task09 v10, rooted pebbling number, 14 vertices)", "",
 "Edit the returned task09 entry field by field (Category stays Mathematics). Every field below replaces the old one.", "",
 "## Subdomain", t["subdomain"], "", "## Modality / image reasoning pattern", "Multimodal (image). Multi-step discrete reasoning on a drawn structure.", "",
 "## Image", "Upload image.png from this folder (replaces the 10-vertex figure).", "", "## Image source", t["imageCreationTool"], "",
 "## Why the image is necessary", t["imageNecessityExplanation"], "", "## Question text", b.question, "",
 "## Answer format / precision", "Exact match. No precision stated (integer).", "", "## Correct answer", b.final_answer, "",
 "## Also accepted (one per line)"] + b.variants + ["", "## Solution", b.solution, "", "## Rubric (points 5/2/2/1; c1 is the final-answer criterion)"]
for c in b.rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
lines += ["", "## Common wrong answers (one per line)"] + b.wrong + ["", "## Reference file", "Upload reference.txt from this folder; it appears as verification_notes.txt (replaces the old file).", "",
 "## References box", b.references, "", "## Where to verify (the box the import leaves empty)", b.VERIFY_FIELD, ""]
open("paste-for-edit.md", "w").write("\n".join(lines)); print("sheet written")
