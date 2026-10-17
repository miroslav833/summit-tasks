import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "renewal-residual-life-log-logistic"
HINT = r", one of them $t = 6$"
question = r"""The figure shows, on logarithmic axes, the survival function $S(t) = P(X > t)$ of the inter-arrival time $X$ of a renewal process. $X$ has a log-logistic distribution, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$, with $\lambda > 0$ and $k > 0$ not given. The curve is drawn so that it passes exactly through gridline crossings at two of the $t$ values labelled on the axisHINT; reading those two crossings fixes $\lambda$ and $k$.

Let $m = E[X]$ and let $r(t)$ be the residual life at time $t$, the time from $t$ until the next arrival of the process. Using the $\lambda$ and $k$ fixed by the figure, find $\lim_{t \to \infty} E[r(t)]\,/\,m$ to two significant figures. Give only this number as the answer.""".replace("HINT", HINT)
final_answer = "0.80"
variants = ["0.8", "0.798", "0.7980", "80 percent of the mean"]
solution = r"""Step 1: The parameters from the figure.
The gridlines of the vertical axis sit at $1$, $2$ and $5$ in every decade. Checking the curve at each labelled $t$, it passes through a gridline crossing at exactly two of them, $(6, 0.02)$ and $(20, 0.0005)$; everywhere else it runs between lines (at $t = 4$ it is at about $0.066$, at $t = 8$ about $0.0083$, at $t = 10$ about $0.0042$, at $t = 15$ about $0.0012$). Since $(t/\lambda)^k = 1/S(t) - 1$, the two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, so $(10/3)^k = 1999/49 = 40.80$, $k = \ln 40.80/\ln(10/3) = 3.7087/1.2040 = 3.080$, and $\lambda = 6/49^{1/k} = 6/3.538 = 1.696$.

Step 2: The moments of $X$.
For the log-logistic distribution $E[X^r] = \lambda^r\,\Gamma(1 + r/k)\,\Gamma(1 - r/k) = \lambda^r\,\dfrac{\pi r/k}{\sin(\pi r/k)}$, finite for $r < k$. Here $k = 3.080 > 2$, so the second moment exists (the first integer moment that diverges is the fourth, since $4 > k$). With $\pi/k = 1.0200$: $E[X] = 1.696 \times 1.0200/\sin 1.0200 = 1.696 \times 1.0200/0.85221 = 2.030$; with $2\pi/k = 2.0400$: $E[X^2] = 1.696^2 \times 2.0400/\sin 2.0400 = 2.8766 \times 2.0400/0.89212 = 6.578$.

Step 3: The limiting residual life.
For a renewal process whose inter-arrival time has a finite second moment and a non-lattice distribution, the residual life $r(t)$ converges in distribution to the equilibrium distribution with density $S(t)/m$, and $E[r(t)] \to \int_0^\infty t\,S(t)\,dt/m = E[X^2]/(2m)$. This is the inspection paradox: the limit is not $m/2$, and for a heavy-tailed $X$ it can be close to or above $m$. Hence $\lim E[r(t)]/m = E[X^2]/(2m^2) = 6.578/(2 \times 2.030^2) = 6.578/8.243 = 0.798$. In closed form, $\dfrac{E[X^2]}{2E[X]^2} = \dfrac{(2\pi/k)\sin^2(\pi/k)}{2(\pi/k)^2 \sin(2\pi/k)} = \dfrac{k}{2\pi}\tan\dfrac{\pi}{k} = 0.49024 \times 1.6278 = 0.798$, independent of $\lambda$.

Step 4: Result.
$\lim_{t\to\infty} E[r(t)]/m = 0.798$, so to two significant figures $0.80$.

Taking the curve through near misses instead of the true crossings gives other answers: $(4, 0.05)$ with $(10, 0.005)$ gives $k = 2.56$ and $1.1$; $(4, 0.05)$ with $(20, 0.0005)$ gives $k = 2.89$ and $0.87$; $(3, 0.2)$ with $(8, 0.01)$ gives $k = 3.27$ and $0.74$; $(3, 0.2)$ with $(15, 0.001)$ gives $k = 3.43$ and $0.71$; $(8, 0.01)$ with $(20, 0.0005)$ gives $k = 3.27$ and $0.74$; $(6, 0.02)$ with $(10, 0.005)$ gives $k = 2.75$ and $0.96$. The naive answers $1/2$ (half the mean) and $1$ ignore the inspection paradox; $E[X^2]/(2E[X]) = 1.62$ is the limit itself, not its ratio to the mean. None of these is the answer.

Answer: $0.80$."""
rubric = [
    dict(id="c1", description=r"Gives $0.80$ as the final answer (any value that rounds to $0.80$ at two significant figures, such as $0.798$).", points=4, isFinalAnswer=True),
    dict(id="c2", description=r"Identifies the crossings $(6, 0.02)$ and $(20, 0.0005)$ as the two the curve passes through and obtains the intermediate values $k = 3.08$ and $\lambda = 1.70$ from $(t/\lambda)^k = 1/S - 1$ (not a near miss such as $(4, 0.05)$, $(8, 0.01)$, $(10, 0.005)$ or $(15, 0.001)$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Uses the limit $E[r(t)] \to E[X^2]/(2E[X])$ (equilibrium residual-life distribution with density $S(t)/m$), not $m/2$ or $m$, and notes that it requires $k > 2$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Computes the log-logistic moments through $\Gamma(1 + r/k)\Gamma(1 - r/k) = (\pi r/k)/\sin(\pi r/k)$ or the equivalent Beta integral, reaching $E[X] = 2.03$ and $E[X^2] = 6.58$ (or the closed form $(k/2\pi)\tan(\pi/k)$).", points=2, isFinalAnswer=False),
]
wrong = ["0.5", "1", "1.1", "0.87", "0.74"]
references = r"""Limiting residual life of a renewal process (key renewal theorem, equilibrium distribution with density $S(t)/m$): W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI; S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, section 3.4. Moments of the log-logistic distribution through the Beta function: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). The uploaded file verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa, solves $\lambda$ and $k$, and gives four computations of the answer (closed form, quadrature of the survival function, the Beta function, and quadrature of the equilibrium residual-life density), the values obtained from every pair of near-miss readings and from each wrong route, and the program with its output."""
necessity = "The parameters lambda and k exist only in the figure: the curve passes through gridline crossings at exactly two of the sixteen labelled abscissae (6 and 20) and runs between gridlines at every other one, by at least 16 percent of a step. The text gives the family and the question but neither parameter; the answer depends on k alone through (k/2pi) tan(pi/k), and every pair of near-miss readings changes it."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Probability: renewal theory (limiting residual life, inspection paradox) with heavy-tailed inter-arrival times",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot of the survival function with a 1-2-5 grid)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 2}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: limiting mean residual life over the mean, log-logistic renewal process

Answer key: 0.80 (0.7980 before rounding).

1. The figure. The vertical axis carries gridlines at 1, 2 and 5 of every decade (1e-4 to 1); the horizontal axis is
   labelled at 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100. The curve S(t) = 1/(1 + (t/lambda)^k) is
   drawn exactly through the gridline crossings (6, 0.02) and (20, 0.0005). At every other labelled abscissa it runs
   between gridlines; the program prints S(t) and the distance to the nearest line at each of them (the closest are
   t = 1 and t = 10, 16 percent off, and t = 8, 17 percent off).
2. Parameters: (t/lambda)^k = 1/S - 1 at the two crossings gives (10/3)^k = 1999/49, k = 3.0803, lambda = 1.6960.
3. The answer, four ways: closed form (k/2pi) tan(pi/k) = 0.79800; quadrature of the survival function for
   E[X] = int S and E[X^2] = 2 int t S, ratio 0.79800; the Beta function E[X^r] = lambda^r B(1 + r/k, 1 - r/k),
   ratio 0.79800; quadrature of the equilibrium residual-life density S(t)/m, limit 1.62007, over m 0.79800.
   The limit exists because k > 2 (finite second moment) and the distribution is non-lattice. For the record the
   program also prints E[X^1], E[X^2] and E[X^3], all finite since r < k, the first divergent integer moment of X
   being the fourth; and the equilibrium residual life has E[r] = 1.62007, E[r^2] = 29.96567 and variance 27.34105,
   finite because the equilibrium density S(t)/m has tail index k - 1 = 2.0803 > 2.
4. Near-miss readings and wrong routes: the program lists every pair of labelled abscissae read at the nearest
   gridline (43 pairs) with the k and the ratio each pair gives; none of them rounds to 0.80. Among them
   (4, 0.05)+(10, 0.005) 1.13, (4, 0.05)+(20, 0.0005) 0.87, (3, 0.2)+(8, 0.01) 0.74, (3, 0.2)+(15, 0.001) 0.71,
   (8, 0.01)+(20, 0.0005) 0.74, (6, 0.02)+(10, 0.005) 0.96. Half the mean gives 0.5, the mean gives 1, the limit
   itself not divided by the mean gives 1.62.
5. The figure (image.png) was drawn by work/draw.py from the survival function with the parameters above; there
   are no data markers.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["task11 renewal residual life", "", "SUBMIT AS A NEW SUBMISSION (Import .zip on the Submit page), not as a revision of SUM-MVB7DTW7: the revision editor keeps the old bandwidth references text, which was the first blocking problem on the v4 consistency check.", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda and k; section 3 gives four computations of the answer (closed form, quadrature of the survival function, the Beta function, quadrature of the equilibrium residual-life density); section 4 lists the value from every pair of near-miss readings and from each wrong route; section 6 embeds the program verify_key.py with its full output.", "", "## Screen", "", "Final wording (one crossing named, t = 6): Opus 1/3 (one run found (6, 0.02) and (20, 0.0005) and gave 0.80; two runs paired the named crossing with an invented gridline at (10, 4e-3), which is not drawn, and gave 0.77), Sonnet see note.md. Same figure without the hint: Opus 0/3 and Sonnet 0/1, every miss an invented gridline. Earlier figures: v1 (9 labels) Opus 3/3 with or without hint; v2 (16 labels, crossings at 5 and 30) Opus 2/3 and Sonnet 1/1 but only through a lucky decade-line pair that rounded to the key, now excluded by the scan. Details in the task11 row of note.md."]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
