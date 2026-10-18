import json, zipfile, pathlib, textwrap, subprocess, sys, numpy as np
HERE = pathlib.Path(__file__).parent; WORK = HERE / "work"
SLUG = "knotted-protein-backbone-crossing-number"
PY = sys.executable
question = (HERE / "stem.txt").read_text().strip()
final_answer = "5"
variants = [r"$5$", "crossing number 5", "five"]
sd = json.load(open(WORK / "solution_data.json"))
seg = json.load(open(WORK / "segments.json"))
helices = [f"{g['first']}-{g['last']}" for g in seg["segments"] if g["kind"] == "helix"]
strands = [f"{g['first']}-{g['last']}" for g in seg["segments"] if g["kind"] == "strand"]
def colour(r):
    f = r / seg["n"]
    for lim, name in ((0.12, "dark blue"), (0.25, "blue"), (0.40, "cyan"), (0.55, "green"), (0.68, "yellow"), (0.82, "orange"), (1.01, "red")):
        if f <= lim: return name
cross_lines = []
for c in sd["crossings"]:
    ok_, uk_ = c["over_kind"], c["under_kind"]
    cross_lines.append(f"The {colour(c['over'])} {ok_[0]} around residue {c['over']} passes over the {colour(c['under'])} {uk_[0]} around residue {c['under']}, sign ${'+' if c['sign'] > 0 else '-'}1$.")
solution = rf"""Step 1: Reduce the drawing to the path of the chain.
The chain runs from the N terminus (blue) to the C terminus (red) through {len(helices)} helices and {len(strands)} strands joined by loops. Crossings between consecutive turns of one helix, and crossings of a loop with its own neighbouring residues, never change the knot type, because each helix is an unknotted coil that can be straightened to its axis without passing through any other part of the chain, because the chain never comes closer to another part than a helix diameter. So replace every helix by its axis and every strand and loop by a smooth line through it, and keep only the crossings between different parts of the chain. The dashed closure adds no crossing.

Step 2: Record the remaining crossings.
Following the chain from N to C in the drawing, {len(sd['crossings'])} crossings between different parts remain, with the part in front read from the gaps in the tube. {" ".join(cross_lines)} Numbering the crossings in the order of the first visit gives the Gauss word {sd['gauss']} (O over, U under), which is the diagram of a single closed curve with {len(sd['crossings'])} crossings.

Step 3: Compute an invariant from the diagram.
Label the {len(sd['crossings'])} arcs between consecutive undercrossings and write, for each crossing, the colouring relation $2a_{{\rm over}} = a_{{\rm in}} + a_{{\rm out}}$. Dropping one relation and one arc and taking the determinant gives the knot determinant $7$. The Alexander polynomial from the same crossing data (Fox calculus with the crossing signs listed above) is $\Delta(t) = 2t^2 - 3t + 2$.

Step 4: Identify the knot and its crossing number.
A knot with at most four crossings is the unknot, the trefoil or the figure-eight knot, with determinants $1$, $3$ and $5$. Determinant $7$ excludes all three, so the crossing number is at least $5$. The only knots with five crossings are $5_1$ (determinant $5$, $\Delta = t^4 - t^3 + t^2 - t + 1$) and $5_2$ (determinant $7$, $\Delta = 2t^2 - 3t + 2$), and the diagram of Step 2 reduces to the standard five-crossing diagram of $5_2$ (the Jones polynomial of the diagram, $t - t^2 + 2t^3 - t^4 + t^5 - t^6$, is that of $5_2$, and the Jones polynomial separates all knots with at most nine crossings). The backbone forms the knot $5_2$, the knot type of the ubiquitin hydrolase UCH-L3 family, and its minimal crossing number is $5$.

Answer: $5$."""
rubric = [
    dict(id="c1", description=r"Gives $5$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Reduces the drawing to a knot diagram by replacing helices by their axes and keeping only the crossings between different parts of the chain, and computes an invariant of that diagram (determinant $7$, Alexander polynomial $2t^2 - 3t + 2$, or an equivalent) that shows the knot is not the unknot, trefoil or figure-eight knot.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Identifies the knot as $5_2$ (not $5_1$, not a trefoil) and justifies the crossing number, at least $5$ because the determinant is not $1$, $3$ or $5$, and at most $5$ because the diagram reduces to, or the invariants match, the five-crossing knot $5_2$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States that crossings inside a single helix and the dashed closure do not affect the knot type.", points=1, isFinalAnswer=False),
]
wrong = ["3", "0", str(json.load(open(WORK / "image_view.json"))["fine_crossings"]), "6"]
references = r"""For knot types of proteins and the reduction of a backbone to a knot diagram see W. R. Taylor, A deeply knotted protein structure and how it might fold, Nature 406 (2000), 916-919, and M. Jamroz, W. Niemyska, E. J. Rawdon, A. Stasiak, K. C. Millett, P. Sulkowski and J. I. Sulkowska, KnotProt: a database of proteins with knots and slipknots, Nucleic Acids Research 43 (2015), D306-D314. The $5_2$ knot of the ubiquitin hydrolase UCH-L3 is PDB entry 1XD3. Knot tables with determinants, Alexander and Jones polynomials are in D. Rolfsen, Knots and Links, AMS Chelsea, 2003, Appendix C, and the KnotInfo table (knotinfo.math.indiana.edu). Fox colourings and the determinant are explained in R. H. Fox, A quick trip through knot theory, in Topology of 3-manifolds, Prentice-Hall, 1962. The uploaded file verification_notes.txt gives the construction of the backbone (axis curve, helices, strands and loops with coordinates), the coarse-grained diagram in the view of the figure with every crossing located on the chain, the determinant, Alexander and Jones polynomials computed from that diagram, and an independent check from the full 200-residue chain in the same projection (its Alexander polynomial agrees with the axis curve's). The programs are embedded with their output."""
necessity = "The structure exists only in the figure. The path of the chain, which parts pass in front of which, and the positions of the termini are not given in the text, and the knot type depends on them."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Low-dimensional topology: knot theory, identification of the knot type of a closed space curve (protein backbone)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib and numpy (own z-buffer tube renderer of a constructed C-alpha trace)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for c in rubric: assert len(c["description"]) <= 500, c["id"]
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_standalone():
    """verify_key_standalone.py: data as literals plus the diagram and invariant code, no local imports."""
    CA = np.load(WORK / "calpha.npy"); coarse = np.load(WORK / "coarse_open.npy"); view = json.load(open(WORK / "image_view.json"))["view"]
    kl = (WORK / "knotlib.py").read_text()
    src = f'''"""Standalone key check for the knotted protein backbone (generated by build_package.py).
Data: 200 C-alpha coordinates (A), the open axis curve (A) and the viewing rotation of the figure.
Checks: (1) the axis curve in the figure's view: crossings, Gauss word, determinant, Alexander and
Jones polynomials; (2) the full chain plus straight closure in the same view: Alexander polynomial
equal to the axis curve's up to a unit (exact integer evaluations), determinant 7, no crossing on
the closure; (3) the isotopy margin between chain and axis. Needs numpy, scipy, sympy. About 2 min."""
import numpy as np, itertools, sympy as sp
from scipy.interpolate import CubicSpline
CA = np.array({np.round(CA, 3).tolist()})
AXIS = np.array({np.round(coarse, 3).tolist()})
VIEW = {list(view)}
# ---- knot library (diagram extraction and invariants) ----
{kl.split('# ---------- invariants from a PD code ----------')[0].split('def build_braid_curve')[0]}
{'def ' + kl.split('def smooth')[1].split('def rotmat')[0] if False else ''}
{kl[kl.index('def rotmat'):]}
def gauss(D):
    ev = []
    for c in D["crossings"]:
        ev.append((c["pi"], c["id"], c["over_i"])); ev.append((c["pj"], c["id"], not c["over_i"]))
    ev.sort(); return [(cid, ov) for _, cid, ov in ev]
def arcs_of(pd):
    E = 2 * len(pd); starts = sorted(x[2] for x in pd); arc = {{}}
    for k, s in enumerate(starts):
        e = s
        while True:
            arc[e] = k; e = (e + 1) % E
            if e in starts: break
    return arc
def alex_eval(pd, signs, tv):
    arc = arcs_of(pd); m = len(pd); M = [[0] * m for _ in range(m)]
    for r, ((a, b, c, d), sg) in enumerate(zip(pd, signs)):
        if sg > 0: M[r][arc[b]] += 1 - tv; M[r][arc[a]] += tv; M[r][arc[c]] += -1
        else: M[r][arc[b]] += 1 - tv; M[r][arc[a]] += -1; M[r][arc[c]] += tv
    A_ = [row[1:] for row in M[1:]]; N = len(A_); sign = 1; prev = 1
    for k in range(N - 1):
        if A_[k][k] == 0:
            sw = next((i for i in range(k + 1, N) if A_[i][k] != 0), None)
            if sw is None: return 0
            A_[k], A_[sw] = A_[sw], A_[k]; sign = -sign
        for i in range(k + 1, N):
            for j in range(k + 1, N):
                A_[i][j] = (A_[i][j] * A_[k][k] - A_[i][k] * A_[k][j]) // prev
        prev = A_[k][k]
    return sign * A_[N - 1][N - 1]
def rotview(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]); return Rz @ Ry @ Rx
if __name__ == "__main__":
    R = rotview(*VIEW)
    print("== axis curve in the figure's view")
    Qa = (AXIS - AXIS.mean(0)) @ R.T; closa = np.linspace(Qa[-1], Qa[0], 30, endpoint=False)[1:]
    Da = diagram(np.vstack([Qa, closa])); sa = [c["sign"] for c in Da["crossings"]]
    print("crossings:", Da["n"], " Gauss word:", " ".join(f"{{c + 1}}{{'O' if o else 'U'}}" for c, o in gauss(Da)))
    print("determinant:", determinant(Da["pd"]), " Alexander:", alexander(Da["pd"], sa).as_expr(), " Jones:", jones_str(jones(Da["pd"], Da["writhe"])))
    print("== full chain with closure in the same view")
    Q = (CA - CA.mean(0)) @ R.T; n = len(Q)
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; cs = CubicSpline(t, Q)
    u = np.linspace(0, t[-1], 2600); F = cs(u); clos = np.linspace(Q[-1], Q[0], 40, endpoint=False)[1:]
    D = diagram(np.vstack([F, clos])); nf = len(F); s = [c["sign"] for c in D["crossings"]]
    onc = sum(1 for c in D["crossings"] if c["pi"] >= nf - 1 or c["pj"] >= nf - 1)
    print("crossings:", D["n"], " on the closure segment:", onc)
    ks = set(); ok = True
    for tv in (2, 3, 5, 7):
        af = abs(alex_eval(D["pd"], s, tv)); ac = abs(alex_eval(Da["pd"], sa, tv)); k = round(np.log(af / ac) / np.log(tv)); ks.add(k)
        ok &= (af == ac * tv ** k) if k >= 0 else (af * tv ** (-k) == ac)
        print(f"  t = {{tv}}: |Alexander(chain)| = {{af}}, |Alexander(axis)| = {{ac}}, ratio t^{{k}}")
    det = abs(alex_eval(D["pd"], s, -1))
    print("Alexander polynomials agree up to a unit:", ok and len(ks) == 1, " determinant of the chain diagram:", det)
    print("== isotopy margin")
    N = len(AXIS); d = np.linalg.norm(AXIS[:, None] - AXIS[None], axis=2)
    idx = np.abs(np.subtract.outer(np.arange(N), np.arange(N))); idx = np.minimum(idx, N - idx); reach = d[idx >= 40].min()
    # distance of every C-alpha from the axis polyline
    def dist_to_axis(p):
        a = AXIS[:-1]; b = AXIS[1:]; ab = b - a; tt = np.clip(((p - a) * ab).sum(1) / (ab * ab).sum(1), 0, 1)
        return np.linalg.norm(a + tt[:, None] * ab - p, axis=1).min()
    off = max(dist_to_axis(p) for p in CA)
    print("axis clearance %.1f A, largest C-alpha offset from the axis %.2f A, margin %.1f A" % (reach, off, reach - 2 * off))
    known = {{-6: -1, -5: 1, -4: -1, -3: 2, -2: -1, -1: 1}}; J = jones(Da["pd"], Da["writhe"])
    assert (J == known or J == {{-k: v for k, v in known.items()}}) and determinant(Da["pd"]) == 7 and onc == 0 and ok and det == 7 and reach - 2 * off > 0
    print("The backbone is the knot 5_2. Crossing number 5. KEY = 5")
'''
    (HERE / "verify_key_standalone.py").write_text(src)
    r = subprocess.run([PY, str(HERE / "verify_key_standalone.py")], capture_output=True, text=True, cwd=str(HERE))
    out = r.stdout + (("\nSTDERR:\n" + r.stderr) if r.returncode else "")
    (WORK / "verify_key_standalone_output.txt").write_text(out)
    assert r.returncode == 0, out[-2000:]
    print("standalone verify ok"); return src, out
def build_reference(src, out):
    pyver = subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip()
    cl = "\n".join(f"   crossing {c['id']:2d}: residue {c['over']} ({c['over_kind'][0]} {c['over_kind'][1]}-{c['over_kind'][2]}) over residue {c['under']} ({c['under_kind'][0]} {c['under_kind'][1]}-{c['under_kind'][2]}), sign {'+' if c['sign'] > 0 else '-'}1" for c in sd["crossings"])
    txt = f"""VERIFICATION NOTES: knot type of the protein backbone in the figure

Answer key: 5 (the closed backbone is the knot 5_2).

1. Construction. The backbone follows an axis curve that is the closure of the 3-strand braid
   s1^3 s2 s1^-1 s2 (the knot 5_2), relaxed to a compact curve whose distinct parts stay 9.2 A apart.
   200 C-alpha atoms are laid along the axis: helices (axis radius 2.3 A, rise 1.5 A, 100 degrees per
   residue) at residues {", ".join(helices)}; strands at residues {", ".join(strands)}; loops elsewhere.
   Every C-alpha lies within 2.3 A of the axis, so the chain is isotopic to the axis curve and has its
   knot type. The figure is the orthographic projection of the chain along the viewing direction
   stored as VIEW in the program; the straight segment between the termini carries no crossing.

2. Coarse-grained diagram in the view of the figure ({len(sd['crossings'])} crossings between different parts of the chain;
   crossings within one helix are not part of the knot diagram):
{cl}
   Gauss word (order of first visit, O over, U under): {sd['gauss']}
   Determinant 7; Alexander polynomial {sd['alexander']}; Jones polynomial {sd['jones']}.
   Knots with at most four crossings have determinants 1, 3, 5, so the crossing number is at least 5;
   5_1 has determinant 5 and 5_2 has determinant 7 and Alexander polynomial 2t^2 - 3t + 2, and the
   Jones polynomial above is that of 5_2 (the Jones polynomial separates all knots up to nine
   crossings). Crossing number 5 (Rolfsen table, KnotInfo).

3. Independent check from the drawn chain itself: the 200-residue chain with its closure, projected
   along the same direction, has a diagram with the same Alexander polynomial as the axis curve up
   to a unit (exact integer evaluations at t = 2, 3, 5, 7) and determinant 7; no crossing lies on
   the closure segment. Program and output below.

4. Program verify_key_standalone.py (run with {pyver}; command: python3 verify_key_standalone.py;
   needs numpy, scipy, sympy; the coordinates are embedded)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False))
    src, out = build_standalone(); build_reference(src, out); build_zip()
