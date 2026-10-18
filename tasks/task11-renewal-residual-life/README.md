task11 renewal function at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

Figure is on logarithmic axes. It shows survival function $S(t) = P(X > t)$ for inter-arrival time $X$ of renewal process. $X$ is log-logistic, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

Curve passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$. Those two crossings fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process starts at time $0$. Find $E[N(6)]$ with the $\lambda$ and $k$ you read from figure. Give 4 significant figures.

Neither parameter is round number so keep 4 figures on both. This quantity has no closed form and the coarse schemes are still several per cent out at a step you would pick on a first try, so refine the step or extrapolate until the 4th figure stops moving. State which scheme you used and the values it gave at each step. Last line of your response must be FINAL: and then number.

## Answer

2.705

## Solution

Parameters from the figure.

Vertical gridlines sit at $1$, $2$, $5$ in each decade. Curve hits a crossing at exactly two labelled $t$, these are $(6, 0.02)$ and $(20, 0.0005)$. At other labelled values it runs between lines, for example about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$, about $0.0012$ at $t = 15$.

From $(t/\lambda)^k = 1/S(t) - 1$ the two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$. Divide them, $(10/3)^k = 1999/49 = 40.80$, so $k = \ln 40.80/\ln(10/3) = 3.080$ and $\lambda = 6/49^{1/k} = 1.696$.

No formula gives the answer here.

Renewal function $M(t) = E[N(t)]$ solves $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$. For log-logistic there is no closed form, Laplace transform of $f$ is not elementary, so $M$ has to be numerical. Mean is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$. At $t = 6$ we are about 3 mean gaps in, asymptotics are still bad there.

Solving it, and the scheme problem.

Take step $h$ on $[0, 6]$ and advance $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$, trapezoidal weights $w_j$. The $u = 0$ term drops because $f(0) = 0$ when $k > 1$. Here $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$, $8000$ intervals this gives $M(6) = 2.70496$ every time.

Scheme choice is what decides this question. All schemes below reach $2.70496$ in the limit, but at half a per cent they sit far apart, and at the step someone picks on a first try none of them is inside.

Trapezoidal product rule on $dF$, implicit in $M_i$, second order. Gives $2.7496$ at $h = 1$, that is $1.65$ per cent high and outside. Then $2.7155$ at $h = 0.5$ and $2.7076$ at $h = 0.25$, both inside.

Midpoint or lattice rule, arrival times rounded to nearest node, comes from above and slowly: $2.9501$, $2.8312$, $2.7678$, $2.7363$, $2.7206$ at steps $1$, $0.5$, $0.25$, $0.125$, $0.0625$. Needs $h$ under about $0.06$. Richardson on its two coarsest values overshoots to $2.7916$.

Discrete renewal recursion is the one people reach for, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$. Each cell mass sits at right endpoint, every renewal gets delayed by up to $h$, so it comes from below at first order: $2.2395$, $2.4417$, $2.5644$, $2.6322$, $2.6679$ at same steps, all outside. At $h = 0.03125$ still $2.6863$. Richardson $2M(h/2) - M(h)$ fixes it earlier, $2.6870$ from pair $(0.5, 0.25)$ still outside, $2.7001$ from $(0.25, 0.125)$ inside.

Grading interval is half per cent each side, kept out of the question on purpose. One run at one step proves nothing, the 4th figure has to be shown settled.

Check by other routes. Convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, each $P(S_j \le 6)$ by repeated numerical convolution of $f$, gives $2.70496$. Simulation of $400\,000$ paths gives $2.7068 \pm 0.0017$.

Result.

$M(6) = 2.70496$, so $2.705$ at 4 significant figures, inside $2.691$ to $2.718$.

4 figures on parameters is enough. $k = 3.080$ with $\lambda = 1.696$ gives $2.7050$. Nearby roundings $k = 3.08, \lambda = 1.70$ and $k = 3.1, \lambda = 1.70$ give $2.6980$ and $2.7011$, still inside.

Rounding $k$ to $3$ with $\lambda = 4^{1/3}$ looks attractive but breaks. That law has $S(6) = 0.0182$ against drawn $0.0200$, nine per cent gap, visible on log axis, and returns $M(6) = 2.8947$, outside.

Shortcuts all fail at this $t$ and interval catches each one. Elementary renewal theorem alone, $t/E[X] = 6/2.030 = 2.9555$, nine per cent high. Asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535$, $1.8$ per cent high, outside half per cent, because $t = 6$ is only about 3 mean gaps. Common slip $t/m - 1/2 = 2.4555$, far out. $F(6) = 0.98$ is probability of at least one renewal, different quantity.

Reading curve through near misses instead of real crossings also lands elsewhere. $(6, 0.02)$ with $(8, 0.01)$ gives $3.64$, with $(10, 0.005)$ gives $3.13$, with $(15, 0.001)$ gives $2.50$, with $(3, 0.2)$ gives $2.24$.

Answer: $2.705$.

## Rubric

- c1 (4 pts, final answer): Final value of $E[N(6)]$ lands in $2.691$ to $2.718$ inclusive, half per cent each side of true $2.70496$. The question does not give this interval, the solver has to converge its own scheme to reach it. Outside that interval is wrong, so coarse grid values $2.7496$ and $2.6679$ fail, extrapolated $2.6870$ and $2.7916$ fail, asymptotic $2.7535$ fails, $t/E[X] = 2.9555$ fails.
- c2 (1 pts): Response says which parameters it used and they are $k = 3.080$, $\lambda = 1.696$ at 4 figures, taken from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$. Rounding $k$ to $3$ loses this point, that law gives $2.8947$ which is outside interval.
- c3 (2 pts): Response names its method and it is renewal equation $M = F + M * f$, or convolution series $\sum_j P(S_j \le t)$, or simulation. Not a closed form or asymptotic formula. Log-logistic renewal function has no closed form, so giving $t/\mu$ or asymptotic expansion as the method loses this point even when number happens to land inside interval.
- c4 (3 pts): Response shows its scheme reached the 4th figure. Any one of these counts. Deterministic scheme at two or more step sizes with the value settling. An extrapolation of two steps. Two independent methods that agree. Or, for simulation, a standard error or confidence interval small enough for the 4th figure, roughly $0.003$ or below, which needs on the order of $10^5$ paths or more, with the path length long enough that truncation does not bite. One run at one step size earns nothing here whatever it returns, and a simulation quoted with no uncertainty estimate earns nothing either. A step too coarse for the scheme also fails, for example right-endpoint recursion at $h = 0.0625$ which is still at $2.6679$.

Common wrong answers: 2.7496, 2.6679, 2.7535, 2.9555, 2.8947, 2.6870, 2.7916, 2.4555

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Moments of the log-logistic distribution through the Beta function: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. It records that this law has no closed form renewal function, then computes $M(6)$ by three independent numerical routes, product integration of the renewal equation at four step sizes, the convolution series $\sum_j P(S_j \le 6)$ with convolutions done numerically, and a simulation of 400000 paths. After that it tables four discretisation schemes against the accepted interval, what each closed form shortcut returns, what rounding $k$ to $3$ does, and what each near miss reading of the figure would give. Program and its full output are at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(6) = 2.704964 three independent ways (the renewal equation M = F + M * f by product integration at four step sizes, the convolution series sum_j P(S_j <= 6), and a simulation of 400000 paths giving 2.7068 with standard error 0.0017); section 4 is the discretisation trap (the discrete renewal recursion converges from below: 2.24 at step 1, 2.44 at step 0.5, 2.56 at step 0.25, and the Richardson repair); section 5 is the rounding trap (forcing k = 3 gives 2.9); section 6 gives the value returned by each closed-form shortcut (t/m = 2.96, the asymptotic expansion 2.75, t/m - 1/2 = 2.46, F(6) = 0.98) and by each near-miss reading of the figure, none of which rounds to 2.7; section 8 embeds the program verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md.