"""Build task.json, reference.txt and the zip for the text-only knotted-backbone task (key 11, knot 11a246)."""
import json, zipfile, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent; WORK = HERE / "work"
SLUG = "backbone-crossing-table-crossing-number"
PY = sys.executable

question = (HERE / "stem.txt").read_text().strip()

solution = r"""Step 1: Read the diagram off the table.
Order the 26 residues of the table along the chain. Each residue is one passage through a crossing, over (O) or under (U), and the straight closure from residue $184$ back to residue $1$ adds nothing. In that order the passages are the following.
8:1U, 14:2O, 19:3U, 26:4O, 35:5U, 39:6O, 43:7U, 53:8O, 61:9U, 65:10U, 71:11O, 79:1O, 83:12U, 91:11U, 96:13U, 100:9O, 104:8U, 111:7O, 118:6U, 122:3O, 127:4U, 131:5O, 139:2U, 146:13O, 150:10O, 160:12O,
This is the Gauss word 1U 2O 3U 4O 5U 6O 7U 8O 9U 10U 11O 1O 12U 11U 13U 9O 8U 7O 6U 3O 4U 5O 2U 13O 10O 12O with the signs of the table ($+1$ at crossings $1$ to $12$, $-1$ at crossing $13$, writhe $11$). A signed Gauss code determines the diagram on the sphere, and with it the knot. The diagram is planar (13 crossings, 26 edges, 15 regions by face tracing, $13 - 26 + 15 = 2$), it is not alternating (for example 10U is followed by 11O and then 1O), and no Reidemeister move of type I or II is visible, because no crossing is met twice in a row and no two crossings are met consecutively on both of their strands.

Step 2: The classical invariants point at $9_{18}$.
Label the thirteen arcs between consecutive undercrossings and write at each crossing the Fox relation $(1 - t)\,a_{\rm over} + t\,a_{\rm in} - a_{\rm out} = 0$ (with in and out swapped at the negative crossing $13$). Deleting one relation and one arc, the determinant is, up to a unit, $\Delta(t) = 4t^4 - 10t^3 + 13t^2 - 10t + 4$, equivalently the Conway polynomial $\nabla(z) = 1 + 6z^2 + 4z^4$, with knot determinant $|\Delta(-1)| = 41$. The signature follows from the Goeritz matrix of the checkerboard colouring (Gordon and Litherland). The colour class with six regions $W_0, \dots, W_5$, where $W_0$ is bounded by crossings $1, 2, 5, 6, 7, 8, 9, 10, 12$, $W_1$ by $1, 12, 11$, $W_2$ by $2, 13, 9, 8, 7, 6, 3$, $W_3$ by $3, 4$, $W_4$ by $4, 5$ and $W_5$ by $10, 13, 11$, has $\eta(c) = -1$ at crossings $10$ and $11$ and $\eta(c) = +1$ elsewhere ($\eta(c) = +1$ when a small counterclockwise rotation of the over strand sweeps it into the two regions of the class). With $g_{ij} = -\sum \eta(c)$ over the crossings between $W_i$ and $W_j$ and zero row sums, deleting $W_0$ leaves
$G = \begin{pmatrix} 1 & 0 & 0 & 0 & 1 \\ 0 & 7 & -1 & 0 & -1 \\ 0 & -1 & 2 & -1 & 0 \\ 0 & 0 & -1 & 2 & 0 \\ 1 & -1 & 0 & 0 & -1 \end{pmatrix},$
$\det G = -41$, four positive and one negative eigenvalue, $\operatorname{sign} G = 3$. The crossings of type II (where the smoothing consistent with the orientation of the chain does not merge the two regions of the class) are $10, 11, 13$ with $\eta = -1, -1, +1$, so $\mu = -1$ and $\sigma = 3 - (-1) = 4$. The alternating knot $9_{18}$ has exactly this Alexander polynomial, determinant $41$ and signature $-4$, so its mirror image has $\Delta$, determinant and signature equal to those found here, and no other knot with at most ten crossings has this Alexander polynomial. The diagram, with twelve positive crossings and one negative, even looks like a positive 9-crossing knot drawn with two kinks and one cancelling pair. The conclusion "$9_{18}$, crossing number $9$" is the natural one, and it is wrong. The Alexander polynomial and the signature do not identify a knot, and the diagram has not been shown to reduce to nine crossings.

Step 3: The hidden simplification.
The region bounded by crossings $10$, $11$ and $12$ is a triangle whose three sides are the chain segments $65$ to $71$ (under at $10$, then over at $11$), $83$ to $91$ (under at $12$, then under at $11$) and $150$ to $160$ (over at $10$, then over at $12$). The segment $150$ to $160$ passes over both other sides, so it can be slid across crossing $11$, which is a Reidemeister move of type III. On each of the three sides the two passages exchange their order, and the Gauss word becomes 1U 2O 3U 4O 5U 6O 7U 8O 9U 11O 10U 1O 11U 12U 13U 9O 8U 7O 6U 3O 4U 5O 2U 13O 12O 10O. Now crossings $12$ and $13$ are met consecutively under (12U 13U) and consecutively over (13O 12O), with opposite signs, and a Reidemeister move of type II removes both. The remaining diagram has $11$ crossings and the Gauss word
1U 2O 3U 4O 5U 6O 7U 8O 9U 11O 10U 1O 11U 9O 8U 7O 6U 3O 4U 5O 2U 10O,
all eleven crossings positive. Over and under alternate along the whole word, so the diagram is alternating, and no crossing is nugatory, since for no crossing do its two passages cut the word into two halves each containing complete pairs only. The diagram is therefore a reduced alternating diagram.

Step 4: Crossing number.
By the theorem of Kauffman, Murasugi and Thistlethwaite (the first Tait conjecture), a reduced alternating diagram has the minimal number of crossings of its knot type. The crossing number is therefore $11$, and the knot is the alternating knot $11a_{246}$, whose Alexander polynomial and signature coincide with those of the mirror image of $9_{18}$. As a check without the theorem, the Kauffman bracket state sum of either diagram gives the Jones polynomial $V(t) = t^2 - t^3 + 3t^4 - 4t^5 + 5t^6 - 6t^7 + 6t^8 - 5t^9 + 4t^{10} - 3t^{11} + 2t^{12} - t^{13}$, of span $11$. The span of the Jones polynomial is at most the crossing number for every knot, so the crossing number is at least $11$ (and the Jones polynomial of $9_{18}$, of span $9$, differs). The eleven-crossing diagram shows it is at most $11$.

Answer: $11$."""

answer = "11"
variants = ["$11$", "crossing number 11", "eleven"]
wrong = ["9", "13", "12", "10"]
rubric = [
    {"id": "c1", "description": "Gives $11$ as the final answer.", "points": 5, "isFinalAnswer": True},
    {"id": "c2", "description": "Builds the diagram from the table (passages in residue order, signed Gauss code) and finds the hidden simplification, a Reidemeister III move on the triangle of crossings 10, 11, 12 followed by the Reidemeister II removal of crossings 12 and 13, giving an 11-crossing diagram (or an equivalent explicit sequence of moves to 11 crossings).", "points": 2, "isFinalAnswer": False},
    {"id": "c3", "description": "Proves the lower bound, either because the 11-crossing diagram is alternating and reduced and so minimal by the Kauffman-Murasugi-Thistlethwaite theorem, or because the Jones polynomial has span 11, which bounds the crossing number from below.", "points": 2, "isFinalAnswer": False},
    {"id": "c4", "description": "Notes that the Alexander polynomial $4t^4 - 10t^3 + 13t^2 - 10t + 4$ (determinant 41) and the signature $\\pm 4$ coincide with those of $9_{18}$ and explains why this does not identify the knot or its crossing number.", "points": 1, "isFinalAnswer": False},
]
references = (r"The minimality of reduced alternating diagrams was proved in L. H. Kauffman, State models and the Jones polynomial, Topology 26 (1987), 395-407, in K. Murasugi, Jones polynomials and classical conjectures in knot theory, Topology 26 (1987), 187-194, and in M. B. Thistlethwaite, A spanning tree expansion of the Jones polynomial, Topology 26 (1987), 297-309. "
    r"The signature formula from the Goeritz matrix is C. McA. Gordon and R. A. Litherland, On the signature of a link, Inventiones Mathematicae 47 (1978), 53-69. "
    r"The Alexander polynomial from Fox calculus is in R. H. Fox, A quick trip through knot theory, in Topology of 3-manifolds, Prentice-Hall, 1962. "
    r"Knot tables with Alexander and Jones polynomials and signatures are D. Rolfsen, Knots and Links, AMS Chelsea, 2003, Appendix C, and the KnotInfo table (knotinfo.math.indiana.edu), entries 9_18 and 11a_246. "
    r"For knots in protein backbones and the closure of the chain see W. R. Taylor, A deeply knotted protein structure and how it might fold, Nature 406 (2000), 916-919. "
    r"The uploaded file verification_notes.txt contains the signed Gauss code built from the table, the planarity check, the Alexander polynomial by exact integer evaluation, the Goeritz matrix with the correction term and the signature, the Reidemeister III and II moves with the Gauss words after each, the alternation and nugatory checks on the 11-crossing diagram, the Jones polynomials of both diagrams by the state sum, the table facts (9_18 is the only knot with at most ten crossings having this Alexander polynomial, checked over the Rolfsen table), and an independent identification of the knot as 11a_246 by its hyperbolic structure (SnapPy census). The programs are embedded with their output.")

task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Low-dimensional topology: knot theory, crossing number of a knot given by a crossing table (Reidemeister moves, alternating diagrams, Alexander polynomial and signature)",
    "modality": "text_only", "taskType": "not_applicable",
    "questionText": question, "answerType": "exact_match", "finalAnswer": [answer], "acceptableAnswerVariants": variants,
    "multipleChoiceOptions": [], "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}

def check():
    blob = json.dumps(task, ensure_ascii=False)
    for ch, name in (("—", "em dash"), ("–", "en dash")):
        assert ch not in blob, name
    for c in rubric: assert len(c["description"]) <= 500, (c["id"], len(c["description"]))
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert answer not in wrong and len(question) < 20000 and len(solution) < 30000
    print("check ok")

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "tkinter" not in l and "warnings.warn" not in l)
    assert r.returncode == 0, out
    return out

def build_reference():
    vk = (HERE / "verify_key.py").read_text(); out_vk = run([PY, "verify_key.py"], HERE)
    (WORK / "verify_key_output.txt").write_text(out_vk)
    sn = (WORK / "verify_snappy.py").read_text(); out_sn = run([PY, "verify_snappy.py"], WORK)
    (WORK / "verify_snappy_output.txt").write_text(out_sn)
    scan = (WORK / "scan11b.py").read_text()
    out_scan = "\n".join(l for l in (WORK / "scan11b_out.txt").read_text().splitlines() if "9_18" in l or l.startswith("done"))
    txt = f"""Verification notes: minimal crossing number of the closed backbone given by the crossing table (key 11)

1. Data to diagram
The 26 residues of the table are ordered along the chain; each is a passage through a crossing, over or under, and the
closure from residue 184 to residue 1 carries no crossing. The signed Gauss code is
  8:1U 14:2O 19:3U 26:4O 35:5U 39:6O 43:7U 53:8O 61:9U 65:10U 71:11O 79:1O 83:12U 91:11U 96:13U 100:9O 104:8U 111:7O
  118:6U 122:3O 127:4U 131:5O 139:2U 146:13O 150:10O 160:12O
with the signs of the table (+1 at crossings 1 to 12, -1 at 13). A signed Gauss code determines the diagram on the
sphere. The PD code is built directly: edge k ends at passage k and starts at passage k - 1; at a crossing the under
strand enters on edge a and leaves on edge a + 1, the over strand enters on its own edge and leaves on the next; for a
positive crossing (under direction = over direction rotated counterclockwise) the over strand runs from the west
position to the east position of the crossing. Face tracing gives 15 regions for 13 crossings and 26 edges, Euler
characteristic 2: the data are planar. No Reidemeister I or II move is visible in the Gauss code.

2. Classical invariants (the trap)
Alexander polynomial from the Fox-calculus matrix, evaluated exactly at t = 2, 3, 5, 7 and compared with
4t^4 - 10t^3 + 13t^2 - 10t + 4 (values 20, 145, 1525, 7045): equal up to a unit. Determinant 41. Signature by
Gordon and Litherland from the Goeritz matrix of the six-region colour class: sign 3, correction mu = -1, sigma = 4
(the nine-region class gives sign -6, mu -10, sigma 4; the Seifert-matrix signature computed by spherogram is 4).
9_18 has the same Alexander polynomial and determinant and signature -4, so its mirror image matches all three.
Table fact (program scan11b.py, over the Rolfsen table in spherogram): 9_18 is the only knot with at most ten
crossings whose Alexander polynomial is 4t^4 - 10t^3 + 13t^2 - 10t + 4, and 11a246 is one of the 11-crossing knots
sharing an Alexander polynomial with a smaller knot. The signature routine was validated against the
Seifert-matrix signatures of all 84 prime knots with at most nine crossings (84 of 84, both colourings).

3. Hidden simplification
The region bounded by crossings 10, 11, 12 is a triangle whose side 150-160 passes over both other sides (over at
10 and at 12). Reidemeister III across crossing 11 swaps the two passages on each side; the Gauss word becomes
  1U 2O 3U 4O 5U 6O 7U 8O 9U 11O 10U 1O 11U 12U 13U 9O 8U 7O 6U 3O 4U 5O 2U 13O 12O 10O (planar),
in which crossings 12 and 13 form a Reidemeister II pair (12U 13U and 13O 12O, signs +1 and -1). Removing them:
  1U 2O 3U 4O 5U 6O 7U 8O 9U 11O 10U 1O 11U 9O 8U 7O 6U 3O 4U 5O 2U 10O, 11 crossings, all positive,
alternating, with no nugatory crossing. By Kauffman, Murasugi and Thistlethwaite the crossing number is 11.

4. Jones polynomial and identification
Kauffman bracket state sum (8192 states for the table diagram, 2048 for the reduced one): both give
V(t) = t^2 - t^3 + 3t^4 - 4t^5 + 5t^6 - 6t^7 + 6t^8 - 5t^9 + 4t^10 - 3t^11 + 2t^12 - t^13, span 11, so the crossing
number is at least 11 by the span bound alone; 9_18 has a Jones polynomial of span 9. Independent identification:
SnapPy finds the complement of the table diagram hyperbolic with volume 8.500584 and identifies it as K11a246
(census names in section 7); the complement of 9_18 has a different volume. Key: 11.

5. Program verify_key.py (python3 with numpy; reads the table embedded in the file and, if present, stem.txt)
{vk}

6. Output of verify_key.py
{out_vk}

7. Program verify_snappy.py (needs snappy and spherogram) and its output
{sn}

{out_sn}

8. Table scan scan11b.py (11-crossing knots sharing an Alexander polynomial with a knot of at most ten crossings) and the lines of its output for this polynomial
{scan}

{out_scan}
"""
    assert "—" not in txt and "–" not in txt
    (HERE / "reference.txt").write_text(txt); print("reference.txt", len(txt), "chars")

def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "reference.txt"): z.write(HERE / f, f)
    print("zip", HERE / f"{SLUG}.zip")

if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); print("task.json written")
    build_reference(); build_zip()
