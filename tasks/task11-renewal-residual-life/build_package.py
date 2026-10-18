import json, zipfile, pathlib, textwrap, subprocess, sys, re
HERE = pathlib.Path(__file__).parent
SLUG = "renewal-residual-life-log-logistic"
HINT = r", at $t = 6$ and $t = 20$"
question = r"""Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ valuesHINT, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $\mathrm{Var}[N(3)]$, variance of number of renewals by time $3$, with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them to 3 significant figures already moves third decimal of answer, so carry both to at least 4 significant figures through whole calculation.

No usable closed form is known for this quantity, so say which method you used and show your working, and give your final answer as value rounded to 3 decimal places.""".replace("HINT", HINT)
final_answer = "0.520"
variants = ["0.520", "0.5200"]
solution = r"""Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

Since $(t/\lambda)^k = 1/S(t) - 1$, two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other leaves $(10/3)^k = 1999/49 = 40.80$, from which $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Since $P(N(3) \ge n) = F_n(3)$, where $F_n$ is distribution function of $n$th arrival time $S_n$, mean is $E[N(3)] = \sum_n F_n(3)$ and second moment is $E[N(3)^2] = \sum_n (2n - 1) F_n(3)$, because $n^2$ is sum of first $n$ odd numbers, and variance is second moment less square of mean. Same thing in renewal form reads $E[N(t)^2] = M(t) + 2\int_0^t M(t-x)\,dM(x)$ with $M(t) = E[N(t)]$, and for log-logistic law no usable closed form is known for either one, so both must come from numerical work.

For key I took step $h$ on $[0, 3]$ and solved $M(t) = F(t) + \int_0^t M(t-u) f(u)\,du$ by product integration on density with trapezoidal weights, where $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$, and then took $2\int_0^3 M(3-x)\,dM(x)$ on same grid. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(3) = 1.201419$ and $\mathrm{Var}[N(3)] = 0.520129$ every time, and to 3 decimals that is $0.520$.

Convolution series gives same number term by term, with $F_1(3) = 0.852799$, $F_2(3) = 0.317143$, $F_3(3) = 0.030527$, $F_4(3) = 0.000938$ and $F_5(3) = 0.000012$, which sum to $E[N(3)] = 1.201419$, while $\sum_n (2n - 1) F_n(3) = 1.963537$, so that variance is $1.963537 - 1.201419^2 = 0.520129$. Simulation of one million paths gives $0.5195 \pm 0.0007$, which agrees within one standard error, though it is too rough to fix third decimal by itself.

Third decimal is what makes this question hard, because key sits only $0.00037$ below edge of its rounding bin, and coarse schemes miss it. Coupled trapezoid scheme on $dF$, which runs $M = F + M * dF$ alongside $A = M + A * dF$ and takes variance as $2A - M - M^2$, gives $0.5501$ at $h = 0.5$, $0.5274$ at $h = 0.25$, $0.5220$ at $h = 0.125$ and $0.5206$ at $h = 0.0625$, which last still rounds to $0.521$, and only second order Richardson from $(0.25, 0.125)$, which gives $0.52012$, comes to $0.520$. Midpoint lattice convolution, which puts each cell mass at its centre, comes down from above and comes slowly, with $0.5730$, $0.5456$ and $0.5326$ at steps $0.5$, $0.25$ and $0.125$, not one of them right.

Parameters must be carried to 4 figures, as question says, since $k = 3.080$ with $\lambda = 1.696$ gives $0.520202$ and third decimal is safe, whereas $k = 3.08$ with $\lambda = 1.70$ gives $0.518861$ and it has already moved to $0.519$. Rounding $k$ all way to $3$, with $\lambda = 4^{1/3}$, is tempting, but that law has $S(6) = 0.0182$ against drawn $0.0200$, a gap of nine per cent which can be seen on log axis, and it returns $0.5771$.

Shortcuts all fail here, for treating $N(3)$ as Poisson, so that variance equals mean, gives $1.201$, asymptotic formula $\sigma^2 t/\mu^3$ gives $0.881$ because $t = 3$ is only about one and a half mean gaps, and forgetting to subtract square of mean leaves $1.964$. Writing $E[N^2] = M + 2(M * dF)$, with $dF$ where $dM$ belongs, gives $0.455$, which is another thing altogether.

Answer: $0.520$."""
rubric = [
    dict(id="c1", description=r"Final answer is $0.520$, which is $\mathrm{Var}[N(3)] = 0.520129$ rounded to 3 decimals as question asks, and it is reached through $E[N(3)]$ and $E[N(3)^2]$ computed numerically with working shown, as stem demands, so bare number gets nothing here. Values which come of coarse grids or wrong formulas are wrong, these being $0.521$, $0.522$, $0.519$, $0.546$, $0.881$, $1.201$, $1.964$ and $0.455$.", points=4, isFinalAnswer=True),
    dict(id="c2", description=r"Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to at least 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which cuts them to $k = 3.08$ and $\lambda = 1.70$ loses this point, since that gives $0.519$.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Response uses correct second moment identity, either $E[N^2] = \sum_n (2n - 1) F_n(3)$ or $E[N^2] = M + 2\int_0^t M(t-x)\,dM(x)$, and then subtracts $M(3)^2$, so that taking $N(3)$ as Poisson, using asymptotic $\sigma^2 t/\mu^3$, or putting $dF$ where $dM$ belongs loses this point, because none of these is variance at finite time.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Working earns this when it shows third decimal has settled, by any one of four tests. It halves step at least twice and each change in value is at most half the one before and under $0.0002$, or it gives Richardson value from two steps of stated order which agrees with a third finer run within $0.0002$, or two different schemes agree within $0.0002$, or it states error bound or 95 per cent band which lies wholly in $0.5195$ to $0.5205$. Anything weaker earns nothing.", points=3, isFinalAnswer=False),
]
wrong = ["0.521", "0.522", "0.519", "0.546", "0.881", "1.201", "1.964", "0.455"]
references = r"""Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that no usable closed form is known for these quantities under this law, then they verify $\mathrm{Var}[N(3)] = 0.520129$ three times and every route is numerical, where first route is renewal equation by product integration with $E[N^2] = M + 2 M * dM$ at four step sizes, second is convolution series $\sum_n (2n - 1) F_n(3)$ with convolutions done numerically, and third is simulation of one million paths. After that notes table two discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each wrong formula would give, then program and its full output come at the end."""
necessity = "Lambda and k are found in figure and nowhere else. Curve can be seen at eleven of sixteen labelled abscissae, from 1 to 30, and it passes through gridline crossing at two of these only, 6 and 20, while at other nine it sits between gridlines by at least 16 percent of a step, so that two crossings cannot be mistaken. Beyond 30 curve has fallen below plotted range, where no reading can be made, though this does not touch two crossings. Text gives family, time and question but no parameter value, and Var[N(3)] needs both."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Probability: renewal theory (variance of the renewal counting process at finite time, numerical solution of renewal equations) with heavy-tailed inter-arrival times",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot of the survival function with a 1-2-5 grid)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "decimal_places", "digits": 3}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
KEY = 0.520129
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    # One grading policy only: exact match on the rounded value the stem asks for.
    dp = task["task"]["answerPrecision"]
    assert dp == {"kind": "decimal_places", "digits": 3}, "precision must match the stem"
    assert task["task"]["answerType"] == "exact_match", "answerType must match how the platform grades"
    assert "graderSpec" not in task["task"], "no invented grader fields; the platform ignores them"
    assert f"{KEY:.3f}" == final_answer, f"key {final_answer} is not {KEY:.6f} at 3 decimals"
    # Every variant must be the same number, not a nearby one.
    for v in variants:
        head = [w for w in v.split() if w[0].isdigit()][0]
        assert abs(float(head) - float(final_answer)) < 1e-9, f"variant {v} is not equal to the key"
    # Every listed wrong answer must round differently from the key.
    for w in wrong:
        assert f"{float(w):.3f}" != final_answer, f"wrong answer {w} rounds to the key"
    # The stem states the output format and the parameter precision, and leaks no value.
    assert "3 decimal places" in question, "stem must state the rounding the grader applies"
    assert "4 significant figures" in question, "stem must pin the parameter precision at the level the solution demonstrates"
    assert "FINAL" not in question, "no output prefix, the grader matches the bare number"
    for leak in (final_answer, "0.52", "0.5201"):
        assert leak not in question, f"stem leaks the answer: {leak}"
    # c1 must grade exactly what the grader grades.
    assert final_answer in rubric[0]["description"], "c1 must name the keyed value"
    for c in rubric:
        assert len(c["description"]) <= 500, f"{c['id']} is {len(c['description'])} chars, the platform caps criteria at 500"
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("\u2014", "\u2013", "\u2019", "\u201c", "\u200b"): assert ch not in text, name
    # Voice gate: Summit's AI Authorship Check reads sentence shape, not em dashes.
    vc = subprocess.run([sys.executable, str(HERE.parent.parent / "voice_check.py"), "-"],
                        input=json.dumps(task), capture_output=True, text=True)
    if vc.returncode != 0:
        print(vc.stdout); raise AssertionError("voice check failed, see above")
    print("package checks passed, voice check passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: variance of the number of renewals by time 3, log-logistic renewal process

Answer key: 0.520, which is Var[N(3)] = 0.520129 rounded to 3 decimals. Grading is exact match on that rounded
value, and every number below is marked by what it rounds to at 3 decimals.

1. The figure. Horizontal gridlines mark the survival axis at 1, 2 and 5 of every decade (1e-4 to 1); the
   horizontal axis is labelled at 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100. The curve
   S(t) = 1/(1 + (t/lambda)^k) is drawn exactly through the gridline crossings (6, 0.02) and (20, 0.0005). At the
   nine other labelled abscissae where it is visible, 1 to 30, it runs between gridlines; the program prints S(t)
   and the distance to the nearest line at each of them (the closest are t = 1 and t = 10, 16 percent off, and
   t = 8, 17 percent off). From t = 40 on the curve is below the plotted range.
2. Parameters: (t/lambda)^k = 1/S - 1 at the two crossings gives (10/3)^k = 1999/49, k = 3.0803, lambda = 1.6960.
   E[X] = 2.03015 and E[X^2] = 6.57795, both finite since r < k; the first divergent integer moment of X is the fourth.
3. The answer, three independent ways. P(N(3) >= n) = F_n(3), so E[N] = sum F_n and E[N^2] = sum (2n - 1) F_n;
   in renewal form E[N(t)^2] = M(t) + 2 (M * dM)(t). No usable closed form is known for either under this law.
   Route 1 solves M = F + M * f by product integration and then takes M + 2 M * dM - M^2 on the same grid: 1000,
   2000, 4000 and 8000 intervals give Var = 0.520129 or 0.520130 each time, with M(3) = 1.201419. Route 2 is the
   convolution series with the convolutions taken numerically: F_1(3) = 0.852799, F_2(3) = 0.317143,
   F_3(3) = 0.030527, F_4(3) = 0.000938, F_5(3) = 0.000012, so E[N] = 1.201419, E[N^2] = 1.963537 and
   Var = 0.520129. Route 3 is a simulation of 1000000 paths, giving Var = 0.5195 with a standard error of 0.0007,
   which agrees within one standard error but is too coarse to fix the third decimal; it is corroboration only.
   Key 0.520 at 3 decimals.
4. The discretisation trap. The key sits 0.00037 below the upper edge of its 3-decimal bin (0.5195 to 0.5205),
   so a scheme has to be settled to about 0.0002 before its rounded value can be trusted.
   Coupled trapezoid scheme on dF (M = F + M * dF, A = M + A * dF, Var = 2A - M - M^2): 0.59021 at h = 0.75,
   0.55006 at 0.5, 0.52744 at 0.25, 0.52195 at 0.125, 0.52058 at 0.0625, none rounding to 0.520; second order
   Richardson gives 0.51989 from (0.5, 0.25), 0.52012 from (0.25, 0.125) and 0.52013 from (0.125, 0.0625), all
   rounding to 0.520.
   Midpoint lattice convolution (each cell's mass at its centre): 0.57304, 0.54556 and 0.53264 at steps 0.5, 0.25
   and 0.125, none rounding to 0.520.
   When each change is at most half the one before, the error left is no larger than the last change, so a last
   change under 0.0002 settles the third decimal; that is what rubric criterion c4 tests.
5. The rounding trap. With four significant figures, k = 3.080 and lambda = 1.696, Var = 0.520202 rounds to 0.520;
   with three, k = 3.08 and lambda = 1.70, it is 0.518861 and rounds to 0.519, which is why the question asks for
   at least four figures. Forcing k to the round value 3 (and then lambda^3 = 4) gives a law with S(6) = 0.018182
   against the drawn crossing 0.0200, nine per cent low, and Var = 0.5771.
6. Wrong formulas: treating N(3) as Poisson gives Var = E[N] = 1.2014; the asymptotic sigma^2 t / mu^3 gives
   0.8807 (t = 3 is only about 1.5 mean gaps); leaving out the - E[N]^2 gives 1.9635; using M + 2 (M * dF) in
   place of M + 2 (M * dM) gives 0.4553; F(3)(1 - F(3)) = 0.1255. None rounds to 0.520.
7. The figure (image.png) was drawn by work/draw.py from the survival function with the parameters above; there
   are no data markers.

8. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    for stale in ("2.691", "2.718", r"\binterval\b", r"\bIN\b", r"\bOUT\b", "half a per cent", "two significant figures", "five significant"):
        assert not re.search(stale, txt), f"stale grading wording in the notes: {stale!r}"
    (HERE / "reference.txt").write_text(txt); print("reference.txt written, no interval wording")
def build_readme():
    lines = ["task11 variance of the renewal count at finite time", "", "REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes Var[N(3)] = 0.520129 three independent ways (renewal equation with E[N^2] = M + 2 M * dM at four step sizes, the convolution series sum (2n - 1) F_n(3), and a simulation of 1000000 paths giving 0.5195 with standard error 0.0007); section 4 tables two discretisation schemes and what each value rounds to at 3 decimals; section 5 is the rounding trap (three-figure parameters give 0.519, forcing k = 3 gives 0.577); section 6 gives each wrong formula, none of which rounds to 0.520; section 8 embeds verify_key.py with its full output.", "", "## Screen", "", "Local screen 2026-10-18 on this exact wording (figure plus stem, no code): Opus 2 of 3 correct, Sonnet 1 of 1 correct. Opus answers 0.521 (correct method, slip in the final subtraction: 1.963520 - 1.443396 written as 0.52112), 0.520 (renewal equations for M and E[N(N-1)]/2 at h = 0.1), 0.520 (convolution series with Simpson, 0.52013). Sonnet 0.520 (coupled trapezoid at three steps and a polynomial fit). The same question at 2 decimals scored Opus 3 of 3 and Sonnet 0 of 1 (Sonnet 0.56 from a coarse midpoint lattice). Earlier E[N(t)] versions: t = 6 at 3 decimals gave Summit 1/5 with 4 cut-offs; t = 3 at 2 decimals Summit 5/5; t = 3.5 at 2 decimals local Opus 3/3 and Sonnet 1/1, with or without the refine hint."]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
