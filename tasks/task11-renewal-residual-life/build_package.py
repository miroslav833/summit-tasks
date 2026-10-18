import json, zipfile, pathlib, textwrap, subprocess, sys, re
HERE = pathlib.Path(__file__).parent
SLUG = "renewal-residual-life-log-logistic"
HINT = r", at $t = 6$ and $t = 20$"
question = r"""Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ valuesHINT, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $E[N(6)]$ with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them to 3 figures moves third decimal of answer, so carry both to at least 4 significant figures through whole calculation.

This quantity has no closed form, and usual coarse schemes, at step which you would pick on first try, are still more than one per cent out, so refine step of your scheme, or extrapolate it, until third decimal stops moving. Say which method you used and show numbers which convinced you it had settled, and give your final answer as value rounded to 3 decimal places.""".replace("HINT", HINT)
final_answer = "2.705"
variants = ["2.705", "2.7050"]
solution = r"""Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

Since $(t/\lambda)^k = 1/S(t) - 1$, two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other leaves $(10/3)^k = 1999/49 = 40.80$, from which $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Renewal function $M(t) = E[N(t)]$ satisfies $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for log-logistic law this equation has no closed form, because Laplace transform of $f$ is not elementary, so that $M$ must come from numerical work. Mean of $X$ is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, which puts $t = 6$ at only about three mean gaps, far too early for asymptotics to be trusted.

For key I took step $h$ on $[0, 6]$ and advanced $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$, where $u = 0$ term drops out because $f(0) = 0$ when $k > 1$, and where $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(6) = 2.70496$ every time, and to 3 decimals that is $2.705$.

Choice of scheme is what decides this question, for all schemes below come to $2.70496$ in the limit, yet at third decimal they lie far apart, and at step which someone picks on first try not one of them has settled.

Trapezoidal product rule on $dF$, taken implicitly in $M_i$, is second order, and it gives $2.7496$ at $h = 1$, $2.7155$ at $h = 0.5$, $2.7076$ at $h = 0.25$ and $2.7056$ at $h = 0.125$, which last still rounds to $2.706$, and only at $h = 0.0625$, with $2.7051$, does it come to $2.705$.

Midpoint or lattice rule, which rounds arrival times to nearest node, comes down from above and comes slowly, giving $2.9501$, $2.8312$, $2.7678$, $2.7363$, $2.7206$ and $2.7128$ at steps from $1$ down to $0.03125$, not one of them right, and Richardson on its two coarsest values overshoots to $2.7916$.

Discrete renewal recursion, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$, is the method which most people reach for first, and because it puts each cell mass at right endpoint it delays every renewal by up to $h$ and creeps up from below at first order, with $2.2395$, $2.4417$, $2.5644$, $2.6322$, $2.6679$ and $2.6863$ at same steps. Richardson $2M(h/2) - M(h)$ helps it, though not quickly, for pairs give $2.6870$, $2.7001$ and $2.7037$ before $(0.0625, 0.03125)$ at last gives $2.7046$, which rounds to $2.705$.

Two other routes agree with key, convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, with each $P(S_j \le 6)$ done by repeated numerical convolution of $f$, giving $2.70496$, and simulation of $400\,000$ paths giving $2.7068 \pm 0.0017$, which is close enough to agree but far too rough to fix third decimal by itself.

Parameters must be carried to 4 figures, as question says, since $k = 3.080$ with $\lambda = 1.696$ gives $2.70500$ and third decimal is safe, whereas $k = 3.08$ with $\lambda = 1.70$ gives $2.6980$ and it has already moved. Rounding $k$ all way to $3$, with $\lambda = 4^{1/3}$, is tempting, but that law has $S(6) = 0.0182$ against drawn $0.0200$, a gap of nine per cent which can be seen on log axis, and it returns $M(6) = 2.8947$.

Shortcuts, as I say, all fail at this $t$, for elementary renewal theorem alone gives $t/E[X] = 2.9555$, asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2)$ gives $2.7535$, still $1.8$ per cent high, common slip $t/m - 1/2$ gives $2.4555$, and $F(6) = 0.98$ is probability of at least one renewal, which is another thing altogether. Reading curve through near misses in place of true crossings lands elsewhere too, $(6, 0.02)$ with $(8, 0.01)$ giving $3.64$, with $(10, 0.005)$ giving $3.13$, with $(15, 0.001)$ giving $2.50$ and with $(3, 0.2)$ giving $2.24$.

Answer: $2.705$."""
rubric = [
    dict(id="c1", description=r"Final answer is $2.705$, which is $E[N(6)] = 2.70496$ rounded to 3 decimals as question asks, and values which come of stopping too soon are wrong, these being $2.750$ from coarse trapezoid at $h = 1$, $2.668$ from right-endpoint recursion at $h = 0.0625$, $2.687$ and $2.792$ from two Richardson overshoots, $2.754$ from asymptotic expansion, $2.956$ from $t/E[X]$ and $2.895$ when $k$ was rounded to $3$.", points=4, isFinalAnswer=True),
    dict(id="c2", description=r"Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which rounds $k$ to $3$ loses this point, since that law gives $2.8947$, which rounds to $2.895$.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Response names its method, and that method is one which really computes renewal function at finite time, either renewal equation $M = F + M * f$, convolution series $\sum_j P(S_j \le t)$ or simulation of process, so that giving $t/\mu$ or asymptotic expansion as method loses this point, even when number happens to come out near key, because this law has no closed form.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Response shows third decimal has settled, either by halving step at least twice with ratio of successive changes between 1.5 and 2.5 for first order scheme or between 3 and 5 for second order and last change under $0.0005$, or by Richardson value agreeing with finer run within $0.0005$, or by two schemes agreeing within $0.0005$, or by simulation with 95 per cent confidence interval whose two ends round alike. One run at one step earns nothing.", points=3, isFinalAnswer=False),
]
wrong = ["2.750", "2.668", "2.754", "2.956", "2.895", "2.687", "2.792", "2.456"]
references = r"""Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that renewal function of this law cannot be written in closed form, then they verify $M(6) = 2.70496$ three times and every route is numerical, where first route is product integration of renewal equation at four step sizes, second is convolution series $\sum_j P(S_j \le 6)$ with convolutions done numerically, and third is simulation of 400000 paths. After that notes table four discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each near miss reading of figure would give, then program and its full output come at the end."""
necessity = "Lambda and k are found in figure and nowhere else. Curve can be seen at eleven of sixteen labelled abscissae, from 1 to 30, and it passes through gridline crossing at two of these only, 6 and 20, while at other nine it sits between gridlines by at least 16 percent of a step, so that two crossings cannot be mistaken. Beyond 30 curve has fallen below plotted range, where no reading can be made, though this does not touch two crossings. Text gives family, time and question but no parameter value, and E[N(6)] needs both."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot of the survival function with a 1-2-5 grid)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "decimal_places", "digits": 3}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
KEY = 2.704964
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
    for leak in (final_answer, "2.70", "2.691", "2.718"):
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
    txt = f"""VERIFICATION NOTES: expected number of renewals by time 6, log-logistic renewal process

Answer key: 2.705, which is M(6) = 2.704964 rounded to 3 decimals. Grading is exact match on that rounded value,
and every number below is marked by what it rounds to at 3 decimals.

1. The figure. Horizontal gridlines mark the survival axis at 1, 2 and 5 of every decade (1e-4 to 1); the
   horizontal axis is labelled at 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100. The curve
   S(t) = 1/(1 + (t/lambda)^k) is drawn exactly through the gridline crossings (6, 0.02) and (20, 0.0005). At the
   nine other labelled abscissae where it is visible, 1 to 30, it runs between gridlines; the program prints S(t)
   and the distance to the nearest line at each of them (the closest are t = 1 and t = 10, 16 percent off, and
   t = 8, 17 percent off). From t = 40 on the curve is below the plotted range.
2. Parameters: (t/lambda)^k = 1/S - 1 at the two crossings gives (10/3)^k = 1999/49, k = 3.0803, lambda = 1.6960.
   E[X] = 2.03015 and E[X^2] = 6.57795, both finite since r < k; the first divergent integer moment of X is the fourth.
3. The answer, three independent ways. The renewal function solves M = F + M * f, which has no closed form for this
   law. Product integration of that equation on 1000, 2000, 4000 and 8000 intervals gives M(6) = 2.704964 each time;
   the convolution series M(6) = sum_j P(S_j <= 6), with the convolutions taken numerically, gives 2.704964; a
   simulation of 400000 paths gives 2.7068 with a standard error of 0.0017, which agrees with the key inside two
   standard errors but is far too coarse to fix the third decimal on its own. Key 2.705 at 3 decimals.
4. The discretisation trap. The third decimal is what gives the question its difficulty: all four schemes below
   converge to 2.704964, but at the step a quick attempt would choose none of them rounds to 2.705, so a single
   unrefined run fails whichever scheme it uses.
   Trapezoidal product rule on dF, implicit in M_i (second order): 2.7496 at h = 1, 2.7155 at 0.5, 2.7076 at 0.25,
   2.7056 at 0.125 (rounds to 2.706, still wrong), 2.7051 at 0.0625 and 2.7050 at 0.03125 (both round to 2.705).
   Midpoint or lattice rule, arrival times rounded to the nearest node, converging from above: 2.9501, 2.8312,
   2.7678, 2.7363, 2.7206, 2.7128 at steps 1 down to 0.03125, none of them rounding to 2.705; a Richardson step
   on its two coarsest values overshoots to 2.7916.
   Discrete renewal recursion M_i = F(t_i) + sum over j of p_j times M_(i-j), cell masses p_j = F(t_j) - F(t_(j-1)),
   which puts each cell's mass at its right endpoint, delays every renewal by up to h and converges from below at
   first order: 2.2395, 2.4417, 2.5644, 2.6322, 2.6679, 2.6863 at steps 1 down to 0.03125, none rounding to 2.705.
   Richardson extrapolation of two steps: 2.6440 from (1, 0.5), 2.6870 from (0.5, 0.25), 2.7001 from (0.25, 0.125),
   2.7037 from (0.125, 0.0625), 2.7046 from (0.0625, 0.03125); only the last one rounds to 2.705.
   Product integration on the density, the scheme used for the key, has no such bias and is already exact to six
   digits at 1000 intervals. The program prints the whole table with what each value rounds to.
5. The rounding trap. Forcing k to the round value 3 (and then lambda^3 = 4) gives a law with S(6) = 0.018182
   against the drawn crossing 0.0200, nine per cent low, and S(10) = 0.003984 against the curve's 0.004213. That
   law returns M(6) = 2.8947. The true k is 3.0803. Four significant figures on the parameters are enough and
   three are not: k = 3.080 with lambda = 1.696 gives 2.70500 (rounds to 2.705, same as the exact 2.70496), while
   k = 3.08 with lambda = 1.70 gives 2.6980, k = 3.1 with lambda = 1.70 gives 2.7011 and k = 3.08 with
   lambda = 1.69 gives 2.7156, none of which rounds to 2.705. The question therefore asks for at least four figures.
   The key sits 0.00046 above the lower edge of its 3-decimal bin (2.7045 to 2.7055), so any scheme must be
   converged to better than 0.0005 before its rounded value can be trusted; that is what rubric criterion c4 tests.
6. Why the closed-form shortcuts fail at t = 6 (about three mean gaps): the elementary renewal theorem alone gives
   t/m = 2.9555; the asymptotic expansion t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535 is 1.8 percent high, the most
   plausible wrong route; t/m - 1/2 = 2.4555; F(6) = 0.9800 is the probability of at least one renewal, not their
   expected number. Near-miss readings of the figure, each pairing the named crossing at 6 with a crossing the
   curve does not pass through, give 3.64, 3.13, 2.50, 2.95, 3.88, 2.24, 2.30, 2.60 and 2.61; none rounds to 2.705.
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
    lines = ["task11 renewal function at finite time", "", "REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(6) = 2.704964 three independent ways (the renewal equation M = F + M * f by product integration at four step sizes, the convolution series sum_j P(S_j <= 6), and a simulation of 400000 paths giving 2.7068 with standard error 0.0017); section 4 is the discretisation trap (the discrete renewal recursion converges from below: 2.24 at step 1, 2.44 at step 0.5, 2.56 at step 0.25, and the Richardson repair); section 5 is the rounding trap (forcing k = 3 gives 2.9); section 6 gives the value returned by each closed-form shortcut (t/m = 2.96, the asymptotic expansion 2.75, t/m - 1/2 = 2.46, F(6) = 0.98) and by each near-miss reading of the figure, none of which rounds to 2.7; section 8 embeds the program verify_key.py with its full output.", "", "## Screen", "", "Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md."]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
