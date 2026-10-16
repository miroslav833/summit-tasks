"""Builds task.json, README.md, reference.txt and the Import .zip. Edit the texts here, never the JSON."""
import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "matroid-smallest-representing-field"

question = r"""The figure shows nine points, labelled $A$ to $I$, and eight lines drawn as straight segments. Let $M$ be the simple rank-$3$ matroid on $\{A, B, \dots, I\}$ whose dependent $3$-element sets are exactly the triples of points lying on a common drawn line (the line through $D$, $G$, $E$, $F$ contributes all four of its triples); every triple of points not on a common drawn line is independent.

A representation of $M$ over the finite field $\mathbb{F}_q$ is an injective map from the nine points to the projective plane $\mathrm{PG}(2, q)$ such that three points are collinear in $\mathrm{PG}(2, q)$ if and only if they lie on a common drawn line.

What is the smallest prime power $q$ for which $M$ has a representation over $\mathbb{F}_q$? Give a single integer."""

final_answer = "7"
variants = [r"$7$", "q = 7", r"$\mathbb{F}_7$", "GF(7)"]

solution = r"""Step 1: Read the incidences off the figure.
The eight lines are $ABE$, $ACD$, $AFI$, $BCG$, $CEI$, $CFH$, $DEFG$ and $GHI$. No drawn line contains two of the points $A, B, C, F$ together with a third of them, so these four points form a basis-like frame: every three of them are independent.

Step 2: Normalise a representation and construct the remaining points.
In any representation over any field, $A, B, C, F$ are four points of the projective plane with no three collinear, so after a projectivity we may assume $A = (1,0,0)$, $B = (0,1,0)$, $C = (0,0,1)$, $F = (1,1,1)$. The point $D$ lies on the line $AC$ and differs from $A$ and $C$, so $D = (1, 0, t)$ for some $t \neq 0$. Every other point is now forced as the meet of two lines through points already known:
$$E = AB \cap DF = (1-t,\, -t,\, 0), \qquad G = BC \cap DE = (0,\, 1,\, 1-t), \qquad I = AF \cap CE = (t-1,\, t,\, t), \qquad H = CF \cap GI = (t-1,\, t-1,\, 2t-1).$$
The eighth line and the four-point line are then automatic: $G$ was put on $DE$, so $D, E, F, G$ are collinear, and $H$ was put on $GI$. So the eight incidences impose no condition at all: for every $t$ (and every field) these nine vectors satisfy all the drawn collinearities. Conversely every representation arises this way for exactly one $t$.

Step 3: What can go wrong is degeneracy, not incidence.
A representation also needs the nine points to be distinct and every triple that is not on a drawn line to be non-collinear. Checking the $36$ pairs and the $76$ undrawn triples of the vectors above (each is a polynomial condition in $t$; the full list is in the verification notes) gives exactly five obstructions:
$$t = 0 \ (D = A), \qquad t = 1 \ (E = B), \qquad 2t = 1 \ (A, B, H \text{ collinear}), \qquad t = 2 \ (B, D, I \text{ collinear}), \qquad t^{2} - 3t + 1 = 0 \ (B, D, H \text{ collinear}).$$
For instance $\det(B, D, H) = \det\begin{pmatrix} 0 & 1 & t-1 \\ 1 & 0 & t-1 \\ 0 & t & 2t-1 \end{pmatrix} = t^{2} - 3t + 1$. So $M$ is representable over $\mathbb{F}_q$ exactly when $\mathbb{F}_q$ contains an element $t$ with $t \notin \{0, 1, 2, 1/2\}$ and $t^{2} - 3t + 1 \neq 0$.

Step 4: Go through the small fields.
$\mathbb{F}_2$ and $\mathbb{F}_3$: every element is $0$, $1$ or $2$. $\mathbb{F}_4 = \{0, 1, \omega, \omega^{2}\}$: here $2 = 0$ and $2t - 1 = 1$ never vanishes, but $t^{2} - 3t + 1 = t^{2} + t + 1$ vanishes at $\omega$ and $\omega^{2}$, so nothing is left. $\mathbb{F}_5$: $0, 1, 2$ and $1/2 = 3$ are excluded, and the last element $t = 4$ satisfies $16 - 12 + 1 = 5 \equiv 0$, so it is a root of $t^{2} - 3t + 1$ and $B, D, H$ become collinear. Hence no representation over $\mathbb{F}_5$. $\mathbb{F}_7$: $0, 1, 2$ and $1/2 = 4$ are excluded; the discriminant of $t^{2} - 3t + 1$ is $5$, which is not a square modulo $7$ (the squares are $1, 2, 4$), so the quadratic has no root and $t = 3, 5, 6$ are all admissible.

Step 5: The representation over $\mathbb{F}_7$.
With $t = 3$: $A = (1,0,0)$, $B = (0,1,0)$, $C = (0,0,1)$, $D = (1,0,3)$, $E = (5,4,0)$, $F = (1,1,1)$, $G = (0,3,1)$, $H = (1,1,6)$, $I = (2,3,3)$. These are nine distinct points of $\mathrm{PG}(2,7)$; the eight drawn lines hold by construction, and the determinants of the undrawn triples are all non-zero modulo $7$ (the verification notes list them). So the smallest field is $\mathbb{F}_7$.

Answer: $7$."""

rubric = [
    dict(id="c1", description=r"Gives $q = 7$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Normalises four points in general position (such as $A, B, C, F$) to the standard frame and expresses all remaining points in terms of a single parameter (such as $D = (1, 0, t)$), showing that the eight drawn incidences impose no equation on the parameter.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Finds the complete list of degenerate parameter values, $t \in \{0, 1, 2, 1/2\}$ and the roots of $t^{2} - 3t + 1$ (or the equivalent list for another normalisation), each coming from two points coinciding or from an undrawn triple becoming collinear.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Shows that every element of $\mathbb{F}_5$ is degenerate (in particular that $t = 4$ is a root of $t^{2} - 3t + 1$ over $\mathbb{F}_5$), and that over $\mathbb{F}_4$ the quadratic kills the two elements outside $\mathbb{F}_2$.", points=1, isFinalAnswer=False),
]
wrong = ["5", "3", "2", "4"]

references = r"""Representability of matroids over small finite fields and the role of degeneracy conditions in coordinatisations: G. Whittle, On matroids representable over GF(3) and other fields, Transactions of the American Mathematical Society 349 (1997), 579-603. Representability over fields of given characteristic as a question about solutions of polynomial systems: T. Lazarson, The representation problem for independence functions, Journal of the London Mathematical Society 33 (1958), 21-25. The uploaded file verification_notes.txt contains the symbolic coordinatisation (all points as vectors in the parameter $t$, with the incidences checked identically), the complete list of degeneracy conditions, the admissible parameters over $\mathbb{F}_q$ for $q \le 13$, an independent brute-force search for representations in $\mathrm{PG}(2,q)$ for $q \le 7$, and the explicit representation over $\mathbb{F}_7$ with every determinant; the program is embedded with its output."""

necessity = "The matroid is given only by the figure: which triples lie on a common line, including the four-point line, is not stated in the text, and the answer depends on the exact incidence structure (one incidence more or less changes the degeneracy set and the field)."

task = {
    "schema_version": "summit-task-package-v1",
    "task": {
        "domain": "mathematics",
        "subdomain": "Matroid theory: representability of rank-3 matroids (point-line configurations) over finite fields",
        "modality": "image_reference",
        "taskType": "image_multistep_discrete_reasoning",
        "imageCreationTool": "matplotlib (original straight-line drawing of the configuration from a real representation)",
        "imageNecessityExplanation": necessity,
        "questionText": question,
        "answerType": "exact_match",
        "finalAnswer": [final_answer],
        "acceptableAnswerVariants": variants,
        "multipleChoiceOptions": [],
        "answerPrecision": {"kind": "none"},
        "solution": solution,
        "references": references,
        "rubric": {"criteria": rubric, "commonWrongAnswers": wrong},
        "image": {"entry": "image.png"},
        "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"},
    },
}

def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch, label in (("—", "em dash"), ("–", "en dash"), ("’", "curly quote"), ("“", "curly dquote"), ("​", "zero-width space")):
            assert ch not in text, f"{label} in {name}"
    print("package checks passed")

def build_reference():
    verify_src = (HERE / "verify_key.py").read_text(); verify_out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: smallest field over which the matroid of the figure is representable

Answer key: q = 7.

1. Coordinatisation
   Lines (from the figure): ABE, ACD, AFI, BCG, CEI, CFH, DEFG, GHI. A, B, C, F are in general
   position; normalise A = (1,0,0), B = (0,1,0), C = (0,0,1), F = (1,1,1), D = (1,0,t). Then
   E = AB meet DF = (1-t, -t, 0), G = BC meet DE = (0, 1, 1-t), I = AF meet CE = (t-1, t, t),
   H = CF meet GI = (t-1, t-1, 2t-1). All eight drawn collinearities hold identically in t.
   Every representation is projectively equivalent to one of these, for exactly one t.

2. Degeneracies
   Two points coincide or an undrawn triple is collinear exactly when t = 0 (D = A), t = 1 (E = B),
   2t = 1 (A, B, H collinear), t = 2 (B, D, I collinear) or t^2 - 3t + 1 = 0 (B, D, H collinear).
   The program checks all 36 pairs and all 76 undrawn triples and prints which pair or triple each
   factor comes from.

3. Fields
   Admissible t in GF(q): none for q = 2, 3, 4, 5; {{3, 5, 6}} for q = 7 (and non-empty for every
   larger q tested). Over GF(5) the fifth element t = 4 is a root of t^2 - 3t + 1; over GF(4) the
   two elements outside GF(2) are the roots of t^2 + t + 1.

4. Independent check
   A backtracking search for injective maps into PG(2,q) preserving exactly the drawn
   collinearities (frame fixed, the other five points over all points of the plane) finds no
   representation for q = 2, 3, 4, 5 and one for q = 7, without using the coordinatisation.

5. Program verify_key.py (run with {pyver}, sympy 1.14, numpy 2.5; command: python3 verify_key.py)

{textwrap.indent(verify_src, "   ")}

   Output:

{textwrap.indent(verify_out, "   ")}

6. The figure
   image.png is a straight-line drawing of the real representation with t = 3 after a projective
   change of coordinates; the drawing coordinates are in the program (dictionary POS) and the
   program checks that they are collinear exactly on the eight lines.
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written,", len(txt), "bytes")

def build_readme():
    lines = ["# task03: smallest field over which the matroid of a drawn configuration is representable", "",
             "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "Modality: image. Pattern: multi-step discrete reasoning over image content.", "",
             "## Image", "", "image.png (300 dpi, matplotlib, source work/make_figure.py). Necessity: " + necessity, "",
             "## Question", "", question, "", "## Answer", "", final_answer + "   (also accepted: " + ", ".join(variants) + ")", "",
             "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field (paste into 'Please explain where to find or verify the answer')", "",
              "Sections 1 to 3 of verification_notes.txt give the coordinatisation, the five degeneracy conditions and the admissible parameters over each small field; section 4 is an independent brute-force search in PG(2,q) for q up to 7; section 5 embeds the program verify_key.py with its output, including the explicit representation over GF(7) with all determinants.", "",
              "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")

def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(HERE / "task.json", "task.json"); z.write(HERE / "image.png", "image.png"); z.write(HERE / "reference.txt", "reference.txt")
    print("zip written:", f"{SLUG}.zip")

if __name__ == "__main__":
    check()
    (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); print("task.json written")
    build_reference(); build_readme(); build_zip()
