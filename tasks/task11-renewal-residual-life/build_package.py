import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "renewal-residual-life-log-logistic"
HINT = r", at $t = 6$ and $t = 20$"
question = r"""Figure shows survival function $S(t) = P(X > t)$ on logarithmic axes, where $X$ is inter-arrival time of renewal process and $X$ follows log-logistic law, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

Curve passes exactly through gridline crossings at two of labelled $t$ valuesHINT, and those two crossings together fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$ and process starts at time $0$, so find $E[N(6)]$ using $\lambda$ and $k$ which you read from figure. Neither parameter is round number, so keep at least 4 figures on both while you work.

This quantity has no closed form, and usual coarse schemes are still several per cent out at step which you would pick on first try, so your value has to be good to about half per cent. Say which method you used, then show why you trust it to that accuracy. There is one more thing, last line of your response must be FINAL: and then number with 3 decimal places.""".replace("HINT", HINT)
final_answer = "2.705"
variants = ["2.705", "2.7050", "2.70496", "2.705 renewals", "FINAL: 2.705"]
solution = r"""Vertical gridlines sit at $1$, $2$, $5$ in each decade, and when you check curve against them it hits a crossing at exactly two labelled $t$, which are $(6, 0.02)$ and $(20, 0.0005)$, while at other labelled values it runs between lines, about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

From $(t/\lambda)^k = 1/S(t) - 1$ these two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other gives $(10/3)^k = 1999/49 = 40.80$, so $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Renewal function $M(t) = E[N(t)]$ solves $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for log-logistic law there is no closed form because Laplace transform of $f$ is not elementary, so $M$ has to come from numerical work. Mean is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, which puts $t = 6$ at about 3 mean gaps, and asymptotics are still bad that early.

For the key I took step $h$ on $[0, 6]$ and advanced $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$, where $u = 0$ term drops because $f(0) = 0$ when $k > 1$, and here $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(6) = 2.70496$ every time.

Scheme choice is what decides this question, because all schemes below reach $2.70496$ in the limit but at half per cent they sit far apart, and at step which someone picks on first try none of them is inside.

Trapezoidal product rule on $dF$, implicit in $M_i$, is second order and gives $2.7496$ at $h = 1$, which is $1.65$ per cent high and outside, then $2.7155$ at $h = 0.5$ and $2.7076$ at $h = 0.25$, where both are inside.

Midpoint or lattice rule rounds arrival times to nearest node and comes from above slowly, giving $2.9501$, $2.8312$, $2.7678$, $2.7363$ and $2.7206$ at steps $1$, $0.5$, $0.25$, $0.125$, $0.0625$, so it needs $h$ under about $0.06$, while Richardson on its two coarsest values overshoots to $2.7916$.

Discrete renewal recursion is the one which people reach for, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$, and because each cell mass sits at right endpoint every renewal gets delayed by up to $h$, so it comes from below at first order with $2.2395$, $2.4417$, $2.5644$, $2.6322$ and $2.6679$ at same steps, all of them outside, and even at $h = 0.03125$ it is still $2.6863$. Richardson $2M(h/2) - M(h)$ fixes it earlier, where $2.6870$ from pair $(0.5, 0.25)$ is still outside while $2.7001$ from $(0.25, 0.125)$ is inside.

That is why accuracy is set at half per cent, because one run at one step proves nothing and the value has to be shown settled.

Two other routes confirm it. Convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$ with each $P(S_j \le 6)$ done by repeated numerical convolution of $f$ gives $2.70496$, and simulation of $400\,000$ paths gives $2.7068 \pm 0.0017$.

So $M(6) = 2.70496$, which is $2.705$ to 3 decimals and inside accepted $2.691$ to $2.718$.

Keeping 4 figures on parameters is enough, since $k = 3.080$ with $\lambda = 1.696$ gives $2.7050$, while nearby roundings $k = 3.08, \lambda = 1.70$ and $k = 3.1, \lambda = 1.70$ give $2.6980$ and $2.7011$ and both stay inside.

Rounding $k$ to $3$ with $\lambda = 4^{1/3}$ looks attractive but it breaks, because that law has $S(6) = 0.0182$ against drawn $0.0200$, a nine per cent gap which is visible on log axis, and it returns $M(6) = 2.8947$ which is outside.

Shortcuts all fail at this $t$ and the half per cent catches each one. Elementary renewal theorem alone gives $t/E[X] = 6/2.030 = 2.9555$ and that is nine per cent high, asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535$ is $1.8$ per cent high because $t = 6$ is only about 3 mean gaps, common slip $t/m - 1/2 = 2.4555$ is far out, and $F(6) = 0.98$ is probability of at least one renewal which is different quantity.

Reading curve through near misses instead of real crossings also lands elsewhere, where $(6, 0.02)$ with $(8, 0.01)$ gives $3.64$, with $(10, 0.005)$ gives $3.13$, with $(15, 0.001)$ gives $2.50$ and with $(3, 0.2)$ gives $2.24$.

Answer: $2.705$."""
rubric = [
    dict(id="c1", description=r"Final value of $E[N(6)]$ is within half per cent of $2.70496$, which means it sits in $2.691$ to $2.718$, and response reached it by converged numerical method instead of guess or closed-form formula. Question asks for that accuracy and not for fixed figure count, so any value in that range counts while nothing outside it does, and $2.7496$, $2.6679$, $2.6870$, $2.7916$, $2.7535$ and $2.9555$ all fail.", points=4, isFinalAnswer=True),
    dict(id="c2", description=r"Response says which parameters it used and they are $k = 3.080$ with $\lambda = 1.696$ at 4 figures, taken from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$. Rounding $k$ to $3$ loses this point, because that law gives $2.8947$ which is outside range.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Response names its method and that method actually computes finite-time renewal function, so it is renewal equation $M = F + M * f$, or convolution series $\sum_j P(S_j \le t)$, or simulation of process. This law has no closed form, so giving $t/\mu$ or asymptotic expansion as the method loses this point even when number lands in range.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Response gives objective evidence for half per cent accuracy, and any one of these counts: two successive refinements which agree within $0.013$ of each other with finer one reported, or Richardson extrapolation of two steps where scheme order is stated, or two different methods agreeing within $0.013$, or simulation with reported standard error of $0.003$ or less. Single run at single step earns nothing, and so does any claim of convergence with no numbers shown.", points=3, isFinalAnswer=False),
]
wrong = ["2.7496", "2.6679", "2.7535", "2.9555", "2.8947", "2.6870", "2.7916", "2.4555"]
references = r"""Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. The log-logistic law itself, with its mean through $(\pi/k)/\sin(\pi/k)$: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. It records that this law has no closed form renewal function, then computes $M(6)$ by three independent numerical routes, product integration of the renewal equation at four step sizes, the convolution series $\sum_j P(S_j \le 6)$ with convolutions done numerically, and a simulation of 400000 paths. After that it tables four discretisation schemes against the accepted interval, what each closed form shortcut returns, what rounding $k$ to $3$ does, and what each near miss reading of the figure would give. Program and its full output are at the end."""
necessity = "Lambda and k are only in the figure, where curve is visible at eleven of sixteen labelled abscissae from 1 to 30, and it passes through gridline crossing at exactly two of those, 6 and 20, while at other nine it sits between gridlines by at least 16 percent of a step, so the two crossings are unambiguous. Past 30 curve has dropped below plotted range and no reading is possible there, which does not affect the two crossings. Text gives family, time and question but no parameter values, and E[N(6)] needs both of them."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot of the survival function with a 1-2-5 grid)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "numeric_tolerance",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 4},
    "graderSpec": {"kind": "numeric_tolerance", "target": 2.704964, "absoluteTolerance": 0.0135, "acceptedInterval": [2.691, 2.718], "note": "Half a per cent either side of the converged value. Not stated in the question: the solver must converge its own scheme. Grade the number on the FINAL line."}, "solution": solution, "references": references,
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
    assert band in rubric[0]["description"], "interval must be stated in c1"
    # The stem must NOT leak the window: its midpoint is one digit from the key.
    # An accuracy requirement in the stem is fine. A number near the key is not.
    for leak in (str(LO), str(HI), band, "2.70", "2.705", "2.69", "2.71", "2.72"):
        assert leak not in question, f"stem leaks the answer window: {leak}"
    mid = (LO + HI) / 2
    assert abs(float(f"{mid:.4g}") - float(final_answer)) < 0.002, "midpoint is within a digit of the key, keep it hidden"
    globals()["_BAND"] = (LO, HI)
    for c in rubric:
        assert len(c["description"]) <= 500, f"{c['id']} is {len(c['description'])} chars, the platform caps criteria at 500"
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: expected number of renewals by time 6, log-logistic renewal process

Answer key: 2.705 (2.704964 exactly, to four significant figures).
Grading interval is 2.691 to 2.718, half a per cent either side of the true value. It is held in the grader
and is deliberately not stated in the question, so a solver has to converge a scheme to land inside it. Every
number below is labelled IN or OUT against that interval.

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
