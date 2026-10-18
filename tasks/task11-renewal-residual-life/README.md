task11 renewal function at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $E[N(3)]$ with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them too early can move second decimal of answer, so carry both to at least 4 significant figures through whole calculation.

No usable closed form is known for this quantity, and usual coarse schemes, at step which you would pick on first try, are still several per cent out, so refine step of your scheme, or extrapolate it, until second decimal stops moving. Say which method you used and show numbers which convinced you it had settled, and give your final answer as value rounded to 2 decimal places.

## Answer

1.20

## Solution

Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

Since $(t/\lambda)^k = 1/S(t) - 1$, two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other leaves $(10/3)^k = 1999/49 = 40.80$, from which $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Renewal function $M(t) = E[N(t)]$ satisfies $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for log-logistic law no usable closed form for its solution is known, Laplace transform of $f$ having no elementary form either, so that $M$ is best got from numerical work. Mean of $X$ is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, which puts $t = 3$ at only about one and a half mean gaps, far too early for asymptotics to be trusted.

For key I took step $h$ on $[0, 3]$ and advanced $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$, where $u = 0$ term drops out because $f(0) = 0$ when $k > 1$, and where $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(3) = 1.20142$ every time, and to 2 decimals that is $1.20$.

Choice of scheme is what decides this question, for all schemes below come to $1.20142$ in the limit, yet at second decimal they lie apart, and at step which someone picks on first try not one of them has settled.

Trapezoidal product rule on $dF$, taken implicitly in $M_i$, is second order, and it gives $1.2481$ at $h = 1$ and $1.2126$ at $h = 0.5$, which still round to $1.25$ and $1.21$, and only at $h = 0.25$, with $1.2042$, does it come to $1.20$.

Midpoint or lattice rule, which rounds arrival times to nearest node, comes down from above and comes slowly, giving $1.4504$, $1.3294$, $1.2651$, $1.2331$, $1.2172$ and $1.2093$ at steps from $1$ down to $0.03125$, not one of them right, and Richardson on its two coarsest values overshoots to $1.2891$.

Discrete renewal recursion, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$, is the method which most people reach for first, and because it puts each cell mass at right endpoint it delays every renewal by up to $h$ and creeps up from below at first order, with $1.0353$, $1.1060$, $1.1498$, $1.1745$, $1.1877$ and $1.1945$ at same steps. Richardson $2M(h/2) - M(h)$ helps it, though not quickly, for pairs give $1.1767$ and $1.1937$ before $(0.25, 0.125)$ at last gives $1.1993$, which rounds to $1.20$.

Two other routes agree with key, convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, with each $P(S_j \le 3)$ done by repeated numerical convolution of $f$, giving $1.20142$, and simulation of $400\,000$ paths giving $1.2032 \pm 0.0011$, which agrees with key, though its 95 per cent band from $1.2010$ to $1.2054$ is too wide to fix second decimal by itself, so it serves only as a check.

Parameters must be carried to 4 figures, as question says, since $k = 3.080$ with $\lambda = 1.696$ gives $1.2015$ and second decimal is safe, whereas $\lambda = 1.69$ gives $1.2068$ and it has already moved. Rounding $k$ all way to $3$, with $\lambda = 4^{1/3}$, is tempting, but that law has $S(6) = 0.0182$ against drawn $0.0200$, a gap of nine per cent which can be seen on log axis, and it returns $M(3) = 1.3028$.

Shortcuts, as I say, all fail at this $t$, for elementary renewal theorem alone gives $t/E[X] = 1.4777$, asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2)$ gives $1.2757$, still $6$ per cent high, common slip $t/m - 1/2$ gives $0.9777$, and $F(3) = 0.85$ is probability of at least one renewal, which is another thing altogether. Reading curve through near misses in place of true crossings lands elsewhere too, $(6, 0.02)$ with $(8, 0.01)$ giving $1.73$, with $(10, 0.005)$ giving $1.44$, with $(15, 0.001)$ giving $1.09$ and with $(3, 0.2)$ giving $0.95$.

Answer: $1.20$.

## Rubric

- c1 (4 pts, final answer): Final answer is $1.20$, which is $E[N(3)] = 1.20142$ rounded to 2 decimals as question asks, and it is reached by renewal equation, convolution series or simulation with numbers shown which settle second decimal, as stem demands, so bare number or one coarse run gets nothing here. Values which come of stopping too soon are wrong, these being $1.25$, $1.19$, $1.18$, $1.29$, $1.28$, $1.48$ and $1.30$.
- c2 (1 pts): Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which rounds $k$ to $3$ loses this point, since that law gives $1.3028$, which rounds to $1.30$.
- c3 (2 pts): Response names its method, and that method is one which really computes renewal function at finite time, either renewal equation $M = F + M * f$, convolution series $\sum_j P(S_j \le t)$ or simulation of process, so that giving $t/\mu$ or asymptotic expansion as method loses this point, even when number happens to come out near key, because no usable closed form is known for this law.
- c4 (3 pts): Response earns this by any one of four tests. It halves step at least twice and each change in value is at most half the one before and under $0.001$, or it gives Richardson value from two steps of stated order which agrees with a third finer run within $0.001$, or two different schemes agree within $0.001$, or it states error bound or 95 per cent band which lies wholly in $1.195$ to $1.205$. One run at one step, and anything else, earns nothing.

Common wrong answers: 1.25, 1.21, 1.19, 1.18, 1.29, 1.28, 1.48, 1.30

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that no usable closed form is known for renewal function of this law, then they verify $M(3) = 1.20142$ three times and every route is numerical, where first route is product integration of renewal equation at four step sizes, second is convolution series $\sum_j P(S_j \le 3)$ with convolutions done numerically, and third is simulation of 400000 paths. After that notes table four discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each near miss reading of figure would give, then program and its full output come at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(3) = 1.201419 three independent ways (product integration of the renewal equation at four step sizes, the convolution series sum_j P(S_j <= 3), and a simulation of 400000 paths giving 1.2032 with standard error 0.0011); section 4 tables four discretisation schemes and what each value rounds to at 2 decimals; section 5 is the rounding trap (forcing k = 3 gives 1.30, cutting lambda to 1.69 gives 1.21); section 6 gives each closed-form shortcut and each near-miss reading, none of which rounds to 1.20; section 8 embeds verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md.