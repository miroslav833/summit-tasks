import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "renewal-residual-life-log-logistic"
HINT = r", at $t = 6$ and $t = 20$"
question = r"""The figure shows, on logarithmic axes, the survival function $S(t) = P(X > t)$ of the inter-arrival time $X$ of a renewal process, where $X$ has a log-logistic distribution, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$. The curve passes exactly through gridline crossings at two of the $t$ values labelled on the axisHINT, and reading those two crossings fixes $\lambda$ and $k$.

Let $N(t)$ be the number of renewals in $(0, t]$, the arrivals of the process, with the process starting at time $0$. Using the $\lambda$ and $k$ fixed by the figure, find $E[N(6)]$, and give it to four significant figures. Neither parameter is a round number, so carry both to at least four significant figures. The answer is graded against the interval $2.691$ to $2.718$, which is half a per cent either side of the true value, so a coarse discretisation will not pass: refine the step of whatever scheme you use, or extrapolate it, until the value stops moving at that accuracy. End your response with the line FINAL: followed by the number alone.""".replace("HINT", HINT)
final_answer = "2.705"
variants = ["2.7050", "2.705 renewals", "2.704", "2.706", "2.7049", "2.70496", "FINAL: 2.705"]
solution = r"""Step 1: The parameters from the figure.
The gridlines of the vertical axis sit at $1$, $2$ and $5$ in every decade. Checking the curve at each labelled $t$, it passes through a gridline crossing at exactly two of them, $(6, 0.02)$ and $(20, 0.0005)$; everywhere else it runs between lines (at $t = 4$ it is at about $0.066$, at $t = 8$ about $0.0083$, at $t = 10$ about $0.0042$, at $t = 15$ about $0.0012$). Since $(t/\lambda)^k = 1/S(t) - 1$, the two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, so $(10/3)^k = 1999/49 = 40.80$, $k = \ln 40.80/\ln(10/3) = 3.7087/1.2040 = 3.080$, and $\lambda = 6/49^{1/k} = 6/3.538 = 1.696$.

Step 2: Why no formula finishes the job.
The renewal function $M(t) = E[N(t)]$ satisfies $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for the log-logistic law this equation has no closed-form solution: the Laplace transform of $f$ is not elementary, so $M$ must be obtained numerically. The mean is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, so $t = 6$ is only about three mean gaps, far too early for the asymptotics to be accurate.

Step 3: Solving the renewal equation, and the discretisation trap.
Discretise $[0, 6]$ with step $h$ and advance $M$ by product integration on the density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$; the $u = 0$ term vanishes because $f(0) = 0$ for $k > 1$. Here $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. At $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(6) = 2.70496$ every time, which is the key.

The choice of scheme decides the answer, and that is the crux of the question. Every scheme below converges to $2.70496$, but at the half a per cent demanded they are far apart, and none of them passes at the step a quick attempt would choose.

A trapezoidal product rule on the measure $dF$, taken implicitly in $M_i$, is second order: it gives $2.7496$ at $h = 1$, which is $1.65$ per cent high and outside the interval, then $2.7155$ at $h = 0.5$ and $2.7076$ at $h = 0.25$, which are inside. A midpoint or lattice rule that rounds arrival times to the nearest node approaches from above and converges slowly: $2.9501$, $2.8312$, $2.7678$, $2.7363$, $2.7206$ at steps $1$, $0.5$, $0.25$, $0.125$, $0.0625$, so it needs $h$ below about $0.06$, and a Richardson step on its two coarsest values overshoots to $2.7916$. The obvious hand method is the discrete renewal recursion, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$. That scheme places each cell's mass at its right endpoint, so it delays every renewal by up to $h$ and converges from below at first order only: $2.2395$, $2.4417$, $2.5644$, $2.6322$, $2.6679$ at the same steps, every one of them outside the interval. Even at $h = 0.03125$ it is still at $2.6863$, and it is the step after that before it arrives. Richardson extrapolation, $2M(h/2) - M(h)$, repairs it sooner: $2.6870$ from the pair $(0.5, 0.25)$ is still outside, $2.7001$ from $(0.25, 0.125)$ is inside.

So the half a per cent is what makes the question work: a single run at one step size is not evidence of anything, and the value has to be shown to have stopped moving.

An independent evaluation as the convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, with each $P(S_j \le 6)$ computed by repeated numerical convolution of $f$, gives $2.70496$ as well, and a simulation of $400\,000$ paths gives $2.7068 \pm 0.0017$.

Step 4: Result.
$M(6) = 2.70496$, so to four significant figures $2.705$, inside the stated interval $2.691$ to $2.718$.

Carrying the parameters to four significant figures is enough: $k = 3.080$ with $\lambda = 1.696$ gives $2.7050$, and the nearby roundings $k = 3.08, \lambda = 1.70$ and $k = 3.1, \lambda = 1.70$ give $2.6980$ and $2.7011$, all inside. Rounding $k$ to $3$ and $\lambda$ to $4^{1/3}$ is tempting and wrong: that law gives $S(6) = 0.0182$ against the drawn $0.0200$, a visible nine per cent gap on a logarithmic axis, and returns $M(6) = 2.8947$, outside.

The shortcuts all fail at this $t$, and the interval is narrow enough to catch each one. The elementary renewal theorem alone, $t/E[X] = 6/2.030 = 2.9555$, is $9$ per cent high. The asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535$ is $1.8$ per cent high, well outside the half a per cent, because $t = 6$ is only about three mean gaps. The common slip $t/m - 1/2 = 2.4555$ is far out, and $F(6) = 0.98$ is the probability of at least one renewal, not their expected number. Taking the curve through near misses instead of the true crossings also lands elsewhere: $(6, 0.02)$ with $(8, 0.01)$ gives $3.64$, with $(10, 0.005)$ gives $3.13$, with $(15, 0.001)$ gives $2.50$, with $(3, 0.2)$ gives $2.24$. None of these is the answer.

Answer: $2.705$."""
rubric = [
    dict(id="c1", description=r"Gives a final value of $E[N(6)]$ that lies in the interval $2.691$ to $2.718$ inclusive, the half a per cent either side of the true $2.70496$ stated in the question. Anything outside that interval is wrong, including the coarse-grid values $2.7496$ and $2.6679$, the extrapolated $2.6870$ and $2.7916$, the asymptotic $2.7535$ and $t/E[X] = 2.9555$.", points=4, isFinalAnswer=True),
    dict(id="c2", description=r"The response states the parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to four significant figures, obtained from $(t/\lambda)^k = 1/S - 1$ at the two crossings $(6, 0.02)$ and $(20, 0.0005)$. Rounding $k$ to $3$ loses this point, since that law returns $2.8947$ and falls outside the accepted interval.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"The response names the method it used, and that method is the renewal equation $M = F + M * f$, the convolution series $\sum_j P(S_j \le t)$, or simulation, rather than a closed-form or asymptotic formula. The log-logistic renewal function has no closed form, so quoting $t/\mu$ or the asymptotic expansion as the method loses this point even if the number happens to land in the interval.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"The response gives evidence that its scheme has converged to the accuracy the question demands: at least two step sizes with the value settling, an extrapolation, or a second independent method agreeing. A single run at one step size earns nothing here, whatever it returns, and so does a stated step too coarse for the scheme used, such as the right-endpoint recursion at $h = 0.0625$ (which is still at $2.6679$, outside the interval).", points=3, isFinalAnswer=False),
]
wrong = ["2.7496", "2.6679", "2.7535", "2.9555", "2.8947", "2.6870", "2.7916", "2.4555"]
references = r"""The renewal equation and the renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI; S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, where the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ is derived and its slow approach noted. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Moments of the log-logistic distribution through the Beta function: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). The uploaded file verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from them. It records that the renewal function of this law has no closed form and computes $M(6)$ at finite time by three independent numerical routes: product integration of the renewal equation at four step sizes, the convolution series $\sum_j P(S_j \le 6)$ with the convolutions taken numerically, and a simulation of 400000 paths. It then tabulates four discretisation schemes against the accepted interval, the value each closed-form shortcut returns, the effect of rounding $k$ to $3$, and the value each near-miss reading of the figure would give, and ends with the program and its full output."""
necessity = "The parameters lambda and k exist only in the figure: the curve passes through gridline crossings at exactly two of the sixteen labelled abscissae (6 and 20) and runs between gridlines at every other one, by at least 16 percent of a step. The text gives the family, the time and the question but neither parameter, and E[N(6)] depends on both."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot of the survival function with a 1-2-5 grid)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 4}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    LO, HI = 2.691, 2.718
    assert LO <= float(final_answer) <= HI, "key outside its own interval"
    for w in wrong: assert not (LO <= float(w) <= HI), f"wrong answer {w} is inside the accepted interval"
    for v in variants:
        head = [w for w in v.replace("FINAL:", " ").split() if w[0].isdigit()][0]
        assert LO <= float(head) <= HI, f"variant {v} is outside the accepted interval"
    band = f"${LO}$ to ${HI}$"
    assert band in question and band in rubric[0]["description"], "interval not stated in both the question and c1"
    globals()["_BAND"] = (LO, HI)
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: expected number of renewals by time 6, log-logistic renewal process

Answer key: 2.705 (2.704964 exactly, to four significant figures). The question states and the rubric enforces an
acceptance interval of 2.691 to 2.718, half a per cent either side of the true value. Every number below is
labelled IN or OUT against that interval.

1. The figure. The vertical axis carries gridlines at 1, 2 and 5 of every decade (1e-4 to 1); the horizontal axis is
   labelled at 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100. The curve S(t) = 1/(1 + (t/lambda)^k) is
   drawn exactly through the gridline crossings (6, 0.02) and (20, 0.0005). At every other labelled abscissa it runs
   between gridlines; the program prints S(t) and the distance to the nearest line at each of them (the closest are
   t = 1 and t = 10, 16 percent off, and t = 8, 17 percent off).
2. Parameters: (t/lambda)^k = 1/S - 1 at the two crossings gives (10/3)^k = 1999/49, k = 3.0803, lambda = 1.6960.
   E[X] = 2.03015 and E[X^2] = 6.57795, both finite since r < k; the first divergent integer moment of X is the fourth.
3. The answer, three independent ways. The renewal function solves M = F + M * f, which has no closed form for this
   law. Product integration of that equation on 1000, 2000, 4000 and 8000 intervals gives M(6) = 2.704964 each time;
   the convolution series M(6) = sum_j P(S_j <= 6), with the convolutions taken numerically, gives 2.704964; a
   simulation of 400000 paths gives 2.7068 with a standard error of 0.0017 (IN). Key 2.705 at four significant
   figures. The three routes agree to six digits where they are deterministic, and the simulation agrees inside
   its own standard error, so the key is not an artefact of one scheme.
4. The discretisation trap. The half a per cent interval is what gives the question its difficulty: all four
   schemes below converge to 2.704964, but at a step a quick attempt would choose none of them is inside, so a
   single unrefined run fails whichever scheme it uses.
   Trapezoidal product rule on dF, implicit in M_i (second order): 2.7496 OUT at h = 1 (1.65 percent high),
   2.7155 IN at h = 0.5, 2.7076 IN at h = 0.25, 2.7056 IN at h = 0.125.
   Midpoint or lattice rule, arrival times rounded to the nearest node, converging from above: 2.9501, 2.8312,
   2.7678, 2.7363 all OUT at steps 1, 0.5, 0.25, 0.125, then 2.7206 OUT at 0.0625 and 2.7128 IN at 0.03125. A
   Richardson step on its two coarsest values overshoots to 2.7916 OUT.
   Discrete renewal recursion M_i = F(t_i) + sum over j of p_j times M_(i-j), cell masses p_j = F(t_j) - F(t_(j-1)),
   which puts each cell's mass at its right endpoint, delays every renewal by up to h and converges from below at
   first order: 2.2395, 2.4417, 2.5644, 2.6322, 2.6679, 2.6863 at steps 1, 0.5, 0.25, 0.125, 0.0625, 0.03125, every
   one OUT. Richardson extrapolation of two steps repairs it sooner: 2.6440 OUT from (1, 0.5), 2.6870 OUT from
   (0.5, 0.25), 2.7001 IN from (0.25, 0.125).
   Product integration on the density, the scheme used for the key, has no such bias and is already exact to six
   digits at 1000 intervals. The program prints the whole table with the IN and OUT verdicts.
5. The rounding trap. Forcing k to the round value 3 (and then lambda^3 = 4) gives a law with S(6) = 0.018182
   against the drawn crossing 0.0200, nine per cent low, and S(10) = 0.003984 against the curve's 0.004213. That
   law returns M(6) = 2.8947, OUT. The true k is 3.0803. Carrying the parameters to four significant figures keeps
   the result inside the interval under any honest rounding: k = 3.08 with lambda = 1.696 gives 2.7050 IN,
   k = 3.1 with lambda = 1.70 gives 2.7011 IN, k = 3.08 with lambda = 1.70 gives 2.6980 IN, k = 3.07 with
   lambda = 1.70 gives 2.6964 IN, k = 3.08 with lambda = 1.69 gives 2.7156 IN. The interval therefore tests the
   numerical scheme, not the number of digits kept in the parameters.
6. Why the closed-form shortcuts fail at t = 6 (about three mean gaps): the elementary renewal theorem alone gives
   t/m = 2.9555 OUT; the asymptotic expansion t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535 is 1.8 percent high, OUT, and
   this is the one the interval was sized to exclude, since it is the most plausible wrong route; t/m - 1/2 = 2.4555
   OUT; F(6) = 0.9800 is the probability of at least one renewal, not their expected number. Near-miss readings of
   the figure, each pairing the named crossing at 6 with a crossing the curve does not pass through, give 3.64, 3.13,
   2.50, 2.95, 3.88, 2.24, 2.30, 2.60 and 2.61; every one is OUT.
7. The figure (image.png) was drawn by work/draw.py from the survival function with the parameters above; there
   are no data markers.

8. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    LO, HI = _BAND
    assert f"{LO} to {HI}" in txt, "the accepted interval is not stated in the verification notes"
    assert "two significant figures" not in txt, "stale two-significant-figure wording left in the notes"
    (HERE / "reference.txt").write_text(txt); print("reference.txt written, interval stated and consistent")
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
