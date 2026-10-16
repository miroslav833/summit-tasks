"""Builds task.json, README.md, reference.txt and the Import .zip for this task.
Edit the text fields here, never the JSON by hand."""
import json, zipfile, pathlib, textwrap, subprocess, sys

HERE = pathlib.Path(__file__).parent
SLUG = "plane-tree-shabat-vertex-position"

question = r"""The figure shows a plane tree $T$ with nine edges. Filled discs are black vertices, open circles are white vertices, and the cyclic order of the edges around each vertex, read counterclockwise, is the one drawn. The plane of the figure carries the usual orientation of $\mathbb{C}$. $T$ is not isomorphic to its mirror image, so the orientation matters.

A Shabat polynomial for $T$ is a polynomial $P \in \mathbb{C}[x]$ all of whose critical values lie in $\{0, 1\}$ and for which the set $P^{-1}([0,1]) \subset \mathbb{C}$, with the points of $P^{-1}(0)$ coloured black and the points of $P^{-1}(1)$ coloured white, is carried onto $T$ by an orientation-preserving homeomorphism of the plane. The valency of a vertex equals the multiplicity of the corresponding root of $P$ or of $P-1$. Such a polynomial is determined by $T$ up to an affine substitution $x \mapsto ax + b$ with $a \neq 0$. Fix it by requiring that the black vertex of valency $4$ sits at $x = 0$ and the white vertex of valency $1$ sits at $x = 1$.

Let $r$ be the position of the black vertex of valency $2$. Give $r$, with real and imaginary parts to four significant figures."""

final_answer = "0.1399 + 2.699i"
variants = [r"0.1399+2.699i", r"$0.1399 + 2.699\,i$", r"0.1399 + 2.699 i", r"0.13989 + 2.69870i", r"r = 0.1399 + 2.699i"]

solution = r"""Step 1: Read the passport off the figure and set up the polynomial.
The black vertex at the centre has valency $4$; the black vertex inside the long chain has valency $2$; the other three black vertices are leaves. Four white vertices have valency $2$ and one, attached directly to the centre, is a leaf. So $\deg P = 9$ and, with the normalisation of the question,
$$P(x) = c\,x^{4}(x-r)^{2}g(x), \qquad P(x)-1 = c\,(x-1)\,Q(x)^{2},$$
where $g$ is a monic cubic (the three black leaves) and $Q$ is a monic quartic (the four white vertices of valency $2$), both with the same leading coefficient $c$.

Step 2: The derivative is fixed by the valencies.
$P'$ has degree $8$; it vanishes to order $3$ at $0$, to order $1$ at $r$ and to order $1$ at each root of $Q$, which accounts for all eight zeros. So $P'(x) = 9c\,x^{3}(x-r)\,Q(x)$. Differentiating $P - 1 = c(x-1)Q^{2}$ gives $P' = c\,Q\,\bigl(Q + 2(x-1)Q'\bigr)$, hence
$$Q(x) + 2(x-1)\,Q'(x) = 9x^{3}(x-r).$$
Write $Q(x) = x^{4} + t x^{3} + q_2 x^{2} + q_1 x + q_0$. Comparing coefficients: the $x^{3}$ terms give $7t - 8 = -9r$, so $r = (8 - 7t)/9$; the $x^{2}$, $x$ and constant terms give $5q_2 = 6t$, $3q_1 = 4q_2$ and $q_0 = 2q_1$, so $q_2 = \tfrac{6}{5}t$, $q_1 = \tfrac{8}{5}t$, $q_0 = \tfrac{16}{5}t$. Everything is expressed through the single parameter $t$.

Step 3: The two remaining conditions.
$P(0) = 0$ gives $c\,(-1)\,q_0^{2} + 1 = 0$, so $c = 1/q_0^{2} = 25/(256\,t^{2})$. The double root of $P$ at $r$ is only half imposed so far ($P'(r) = 0$ is built in), so the last condition is $P(r) = 0$, that is $c\,(r-1)\,Q(r)^{2} + 1 = 0$ with $r = (8-7t)/9$. Clearing denominators this factors as
$$(t-5)\,(7t-8)^{5}\,(1225\,t^{3} - 2310\,t^{2} + 15789\,t + 640) = 0 .$$
The factor $7t - 8$ means $r = 0$, where the vertex of valency $2$ would merge with the centre, so it is discarded. In terms of $r$ the condition reads
$$(r+3)\,(25r^{3} - 30r^{2} + 189r - 168) = 0,$$
with roots $r = -3$, $r = 0.9202$ and $r = 0.1399 \pm 2.699\,i$. These four roots are the four plane trees with this passport.

Step 4: Discard the real roots.
A real $r$ gives a real $t$, hence real $q_0, q_1, q_2$ and real $c$: the polynomial has real coefficients and its dessin is mapped onto itself by complex conjugation, so that tree is isomorphic to its mirror image. The tree in the figure is not: going counterclockwise round the centre one meets the white leaf, then the long chain, then the two short arms, and a reflection turns this into white leaf, arm, arm, chain, which is a different cyclic order. ($r = -3$ is the tree with the white leaf opposite the chain, $r = 0.9202$ the tree whose chain ends at the white leaf.) So $r$ is one of the conjugate pair $0.1399 \pm 2.699\,i$, and the two values describe the figure and its mirror image.

Step 5: Decide the orientation.
Take $r = 0.13989 + 2.69870\,i$. Then $t = (8-9r)/7 = 0.9630 - 3.4698\,i$, and the white vertices of valency $2$, the roots of $Q$, are $0.0527 + 1.7969\,i$, $0.1984 + 3.2550\,i$, $-1.4490 - 0.2694\,i$ and $0.2350 - 1.3128\,i$; the black leaves, the roots of $g = P/(c\,x^{4}(x-r)^{2})$, are $0.2188 + 3.4450\,i$, $-1.7196 - 0.3461\,i$ and $0.2951 - 1.5568\,i$. The edges of the dessin (the arcs on which $P$ is real and runs from $1$ to $0$) join: the centre to $1$, to $0.0527+1.7969\,i$, to $-1.4490-0.2694\,i$ and to $0.2350-1.3128\,i$; the chain continues $0.0527+1.7969\,i$ to $r$, $r$ to $0.1984+3.2550\,i$, and on to the leaf $0.2188+3.4450\,i$; the arms end at $-1.7196-0.3461\,i$ and $0.2951-1.5568\,i$. The arguments of the four edges at the centre are about $0^\circ$ (white leaf), $88^\circ$ (chain), $190^\circ$ (arm) and $280^\circ$ (arm), so counterclockwise the order is white leaf, chain, arm, arm, which is the figure. For the conjugate root every vertex is reflected in the real axis and the order becomes white leaf, arm, arm, chain, the mirror image. Hence
$$r = 0.1399 + 2.699\,i .$$"""

rubric = [
    dict(id="c1", description=r"Gives $r = 0.1399 + 2.699\,i$ (real and imaginary parts to four significant figures).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Derives the identity $Q + 2(x-1)Q' = 9x^{3}(x-r)$ (or an equivalent relation from $P' = 9c\,x^{3}(x-r)Q$) and reduces $Q$ to the one-parameter family $x^{4} + t\,(x^{3} + \tfrac{6}{5}x^{2} + \tfrac{8}{5}x + \tfrac{16}{5})$ with $r = (8-7t)/9$.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Obtains the equation $(r+3)(25r^{3} - 30r^{2} + 189r - 168) = 0$, or its equivalent in $t$, for the position of the valency-2 vertex.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Rules out the real roots because the drawn tree is not isomorphic to its mirror image, and chooses between the two conjugate roots by the counterclockwise order of the edges at the centre.", points=1, isFinalAnswer=False),
]
wrong = ["0.1399 - 2.699i", "-3", "0.9202"]

references = r"""Uniqueness of the Shabat polynomial of a plane tree up to affine substitution and the correspondence between plane trees and Shabat polynomials: G. B. Shabat and A. Zvonkin, Plane trees and algebraic numbers, Contemporary Mathematics 178 (1994), 233-275. The method of Step 2 (the derivative of a Shabat polynomial is determined by the valencies, which turns the computation into a small algebraic system): J. Betrema and A. Zvonkin, Plane trees and Shabat polynomials, Discrete Mathematics 153 (1996), 47-58. The uploaded file verification_notes.txt contains the symbolic derivation of the quartic for $r$, a numerical tracing of the dessin $P^{-1}([0,1])$ for each of its four roots compared with the figure (only $r = 0.1399 + 2.699\,i$ reproduces the drawn orientation; the conjugate root gives the mirror image), the enumeration of the four plane trees with this passport, and an independent solution of the full Shabat system from random starting points. The complete programs are embedded with their output."""

necessity = "The tree, its planar embedding and its orientation are given only by the figure. The text states neither the valencies nor the shape, and the answer is one of two complex-conjugate numbers: which one is decided solely by the counterclockwise order of the edges at the vertex of valency 4 as drawn."

task = {
    "schema_version": "summit-task-package-v1",
    "task": {
        "domain": "mathematics",
        "subdomain": "Dessins d'enfants: Shabat polynomials of plane trees (Belyi maps on the sphere)",
        "modality": "image_reference",
        "taskType": "image_quantitative_derivation",
        "imageCreationTool": "matplotlib (original drawing of the plane tree from hand-placed coordinates)",
        "imageNecessityExplanation": necessity,
        "questionText": question,
        "answerType": "exact_match",
        "finalAnswer": [final_answer],
        "acceptableAnswerVariants": variants,
        "multipleChoiceOptions": [],
        "answerPrecision": {"kind": "significant_figures", "digits": 4},
        "solution": solution,
        "references": references,
        "rubric": {"criteria": rubric, "commonWrongAnswers": wrong},
        "image": {"entry": "image.png"},
        "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"},
    },
}

def check():
    pts = sum(c["points"] for c in rubric); assert pts == 10, pts
    assert sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer.replace(" ", "") in rubric[0]["description"].replace("\\,", "").replace(" ", "")
    assert final_answer not in wrong and all(w != final_answer for w in wrong)
    assert len(question) <= 20000 and len(solution) <= 30000
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch, label in (("—", "em dash"), ("–", "en dash"), ("’", "curly quote"), ("“", "curly dquote"), ("​", "zero-width space")):
            assert ch not in text, f"{label} in {name}"
    print("package checks passed")

def build_reference():
    verify_src = (HERE / "verify_key.py").read_text()
    verify_out = (HERE / "work" / "verify_key_output.txt").read_text()
    numeric = (HERE / "work" / "confirm_v2.txt").read_text() if (HERE / "work" / "confirm_v2.txt").exists() else "(not yet run)"
    numeric_src = (HERE / "work" / "confirm_numeric_standalone.py").read_text() if (HERE / "work" / "confirm_numeric_standalone.py").exists() else "(see work folder)"
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: position of the black vertex of valency 2 for the plane tree in the figure

Answer key: r = 0.1399 + 2.699 i  (r = 0.139886460896... + 2.698699160646... i).

1. The derivation

   With the black vertex of valency 4 at 0 and the white leaf at 1, P = c x^4 (x-r)^2 g(x) and
   P - 1 = c (x-1) Q(x)^2 with g a monic cubic and Q a monic quartic. The derivative is fixed by the
   valencies, P' = 9c x^3 (x-r) Q, and differentiating P - 1 = c(x-1)Q^2 gives
   Q + 2(x-1)Q' = 9x^3 (x-r). Hence Q = x^4 + t(x^3 + 6x^2/5 + 8x/5 + 16/5) and r = (8-7t)/9.
   P(0) = 0 gives c = 25/(256 t^2); P(r) = 0 gives
   (t-5)(7t-8)^5 (1225 t^3 - 2310 t^2 + 15789 t + 640) = 0, i.e. (r+3)(25r^3 - 30r^2 + 189r - 168) = 0
   after discarding 7t = 8 (r = 0, the two black vertices would coincide).
   Roots: r = -3, r = 0.920227..., r = 0.139886... +/- 2.698699... i.

2. Which root is the figure (program verify_key.py, section 4)

   For each root the polynomial is formed, the dessin P^{{-1}}([0,1]) is traced numerically (from
   every white vertex the arcs on which P is real and decreasing to 0 are followed to the black
   vertex where they end) and the two edge permutations are compared, up to relabelling, with the
   permutations read off the coordinates of image.png. Result: r = -3 and r = 0.9202 give the two
   mirror-symmetric trees of the passport; r = 0.1399 - 2.699 i gives the mirror image of the
   figure; r = 0.1399 + 2.699 i gives the figure. The figure's tree is not isomorphic to its mirror
   image. Vertex positions and the traced edges for the key are printed in the output.

3. Independent numerical route

   The Shabat system for the passport (unknown vertex positions and leading coefficient, nine
   coefficient equations) was solved by Newton's method from random complex starting points, with
   no use of the derivation above. Every converged solution was traced as in section 2; the
   solutions whose dessin is the figure's tree were renormalised (black vertex of valency 4 at 0,
   white leaf at 1) and their valency-2 vertex compared with the key. Output:

{textwrap.indent(numeric, "   ")}

   Program (confirm_numeric_standalone.py):

{textwrap.indent(numeric_src, "   ")}

4. Program verify_key.py (run with {pyver}, sympy 1.14, mpmath 1.3, numpy 2.5; command: python3 verify_key.py)

{textwrap.indent(verify_src, "   ")}

   Output:

{textwrap.indent(verify_out, "   ")}

5. The figure

   image.png was drawn with matplotlib from the coordinates listed in verify_key.py (dictionary V,
   edge list E), with the plane oriented as usual (x to the right, y upwards). The cyclic order at the
   centre, read counterclockwise, is: white leaf, long chain, short arm, short arm. The enumeration
   in verify_key.py lists the four plane trees with this passport: this tree, its mirror image, and
   two mirror-symmetric trees (white leaf opposite the chain; chain ending at the white leaf).
"""
    (HERE / "reference.txt").write_text(txt)
    print("reference.txt written,", len(txt), "bytes")

def build_readme():
    lines = ["# task01: position of a vertex of the Shabat polynomial of a chiral plane tree", "",
             "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "Modality: image. Pattern: quantitative derivation from image-sourced data.", "",
             "## Image", "", "image.png (300 dpi, matplotlib, source work/draw_figure.py). Necessity: " + necessity, "",
             "## Question", "", question, "", "## Answer", "", final_answer + "   (also accepted: " + ", ".join(variants) + ")", "",
             "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric:
        lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field (paste into 'Please explain where to find or verify the answer')", "",
              "Section 1 of verification_notes.txt gives the derivation down to the quartic for r; section 4 embeds the program verify_key.py, which redoes the derivation symbolically, traces the dessin for each of the four roots and compares it with the figure (only r = 0.1399 + 2.699i reproduces the drawn orientation), and enumerates the four plane trees of the passport; section 3 solves the full Shabat system numerically from random starts and recovers the same vertex.", "",
              "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines))
    print("README.md written")

def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(HERE / "task.json", "task.json"); z.write(HERE / "image.png", "image.png"); z.write(HERE / "reference.txt", "reference.txt")
    print("zip written:", f"{SLUG}.zip", [i.filename for i in zipfile.ZipFile(HERE / f'{SLUG}.zip').infolist()])

if __name__ == "__main__":
    check()
    (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False))
    print("task.json written")
    build_reference(); build_readme(); build_zip()
