task11 renewal function at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $E[N(6)]$ with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them to 3 figures moves third decimal of answer, so carry both to at least 4 significant figures through whole calculation.

This quantity has no closed form, and usual coarse schemes, at step which you would pick on first try, are still more than one per cent out, so refine step of your scheme, or extrapolate it, until third decimal stops moving. Say which method you used and show numbers which convinced you it had settled, and give your final answer as value rounded to 3 decimal places.

## Answer

2.705

## Solution

Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

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

Answer: $2.705$.

## Rubric

- c1 (4 pts, final answer): Final answer is $2.705$, which is $E[N(6)] = 2.70496$ rounded to 3 decimals as question asks, and values which come of stopping too soon are wrong, these being $2.750$ from coarse trapezoid at $h = 1$, $2.668$ from right-endpoint recursion at $h = 0.0625$, $2.687$ and $2.792$ from two Richardson overshoots, $2.754$ from asymptotic expansion, $2.956$ from $t/E[X]$ and $2.895$ when $k$ was rounded to $3$.
- c2 (1 pts): Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which rounds $k$ to $3$ loses this point, since that law gives $2.8947$, which rounds to $2.895$.
- c3 (2 pts): Response names its method, and that method is one which really computes renewal function at finite time, either renewal equation $M = F + M * f$, convolution series $\sum_j P(S_j \le t)$ or simulation of process, so that giving $t/\mu$ or asymptotic expansion as method loses this point, even when number happens to come out near key, because this law has no closed form.
- c4 (3 pts): Response shows third decimal has settled, either by halving step at least twice with ratio of successive changes between 1.5 and 2.5 for first order scheme or between 3 and 5 for second order and last change under $0.0005$, or by Richardson value agreeing with finer run within $0.0005$, or by two schemes agreeing within $0.0005$, or by simulation with 95 per cent confidence interval whose two ends round alike. One run at one step earns nothing.

Common wrong answers: 2.750, 2.668, 2.754, 2.956, 2.895, 2.687, 2.792, 2.456

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that renewal function of this law cannot be written in closed form, then they verify $M(6) = 2.70496$ three times and every route is numerical, where first route is product integration of renewal equation at four step sizes, second is convolution series $\sum_j P(S_j \le 6)$ with convolutions done numerically, and third is simulation of 400000 paths. After that notes table four discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each near miss reading of figure would give, then program and its full output come at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(6) = 2.704964 three independent ways (the renewal equation M = F + M * f by product integration at four step sizes, the convolution series sum_j P(S_j <= 6), and a simulation of 400000 paths giving 2.7068 with standard error 0.0017); section 4 is the discretisation trap (the discrete renewal recursion converges from below: 2.24 at step 1, 2.44 at step 0.5, 2.56 at step 0.25, and the Richardson repair); section 5 is the rounding trap (forcing k = 3 gives 2.9); section 6 gives the value returned by each closed-form shortcut (t/m = 2.96, the asymptotic expansion 2.75, t/m - 1/2 = 2.46, F(6) = 0.98) and by each near-miss reading of the figure, none of which rounds to 2.7; section 8 embeds the program verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md.