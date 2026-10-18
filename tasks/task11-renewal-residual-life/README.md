task11 renewal function at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $E[N(3.5)]$ with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them too early can move second decimal of answer, so carry both to at least 4 significant figures through whole calculation.

No usable closed form is known for this quantity, and usual coarse schemes, at step which you would pick on first try, still miss second decimal, so refine step of your scheme, or extrapolate it, until second decimal stops moving. Say which method you used and show numbers which convinced you it had settled, and give your final answer as value rounded to 2 decimal places.

## Answer

1.45

## Solution

Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

Since $(t/\lambda)^k = 1/S(t) - 1$, two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other leaves $(10/3)^k = 1999/49 = 40.80$, from which $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Renewal function $M(t) = E[N(t)]$ satisfies $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for log-logistic law no usable closed form for its solution is known, Laplace transform of $f$ having no elementary form either, so that $M$ is best got from numerical work. Mean of $X$ is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, which puts $t = 3.5$ at only about 1.7 mean gaps, far too early for asymptotics to be trusted.

For key I took step $h$ on $[0, 3.5]$ and advanced $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$, where $u = 0$ term drops out because $f(0) = 0$ when $k > 1$, and where $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(3.5) = 1.45364$ every time, and to 2 decimals that is $1.45$.

Choice of scheme is what decides this question, for all schemes below come to $1.45364$ in the limit, yet at second decimal they lie apart, and at step which someone picks on first try not one of them has settled.

Trapezoidal product rule on $dF$, taken implicitly in $M_i$, is second order, and it gives $1.4643$ at $h = 0.5$ and $1.4563$ at $h = 0.25$, which both still round to $1.46$, and only at $h = 0.125$, with $1.4543$, does it come to $1.45$.

Midpoint or lattice rule, which rounds arrival times to nearest node, comes down from above and comes slowly, giving $1.5814$, $1.5172$, $1.4853$, $1.4694$ and $1.4615$ at steps from $0.5$ down to $0.03125$, not one of them right, though Richardson on any two neighbouring steps gives $1.4531$ to $1.4536$, which rounds to $1.45$.

Discrete renewal recursion, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$, is the method which most people reach for first, and because it puts each cell mass at right endpoint it delays every renewal by up to $h$ and creeps up from below at first order, with $1.3297$, $1.3870$, $1.4190$, $1.4360$ and $1.4447$ at same steps. Richardson $2M(h/2) - M(h)$ helps it, though not quickly, for pair $(0.5, 0.25)$ gives $1.4443$ before $(0.25, 0.125)$ at last gives $1.4510$, which rounds to $1.45$.

Two other routes agree with key, convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, with each $P(S_j \le 3.5)$ done by repeated numerical convolution of $f$, giving $1.45364$, and simulation of $400\,000$ paths giving $1.4559 \pm 0.0012$, which agrees with key within two standard errors, though it rounds to $1.46$ and its 95 per cent band from $1.4535$ to $1.4583$ is too wide to fix second decimal, so it serves only as a check.

Parameters must be carried to 4 figures, as question says, since $k = 3.080$ with $\lambda = 1.696$ gives $1.4537$ and second decimal is safe, whereas $\lambda = 1.69$ gives $1.4599$ and it has already moved. Rounding $k$ all way to $3$, with $\lambda = 4^{1/3}$, is tempting, but that law has $S(6) = 0.0182$ against drawn $0.0200$, a gap of nine per cent which can be seen on log axis, and it returns $M(3.5) = 1.5701$.

Shortcuts, as I say, all fail at this $t$, for elementary renewal theorem alone gives $t/E[X] = 1.7240$, asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2)$ gives $1.5220$, still $5$ per cent high, common slip $t/m - 1/2$ gives $1.2240$, and $F(3.5) = 0.90$ is probability of at least one renewal, which is another thing altogether. Reading curve through near misses in place of true crossings lands elsewhere too, $(6, 0.02)$ with $(8, 0.01)$ giving $2.06$, with $(10, 0.005)$ giving $1.72$, with $(15, 0.001)$ giving $1.32$ and with $(3, 0.2)$ giving $1.16$.

Answer: $1.45$.

## Rubric

- c1 (4 pts, final answer): Final answer is $1.45$, which is $E[N(3.5)] = 1.45364$ rounded to 2 decimals as question asks, and it is reached by renewal equation, convolution series or simulation with numbers shown which settle second decimal, as stem demands, so bare number or one coarse run gets nothing here. Values which come of stopping too soon are wrong, these being $1.46$, $1.44$, $1.42$, $1.52$, $1.72$ and $1.57$.
- c2 (1 pts): Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which rounds $k$ to $3$ loses this point, since that law gives $1.5701$, which rounds to $1.57$.
- c3 (2 pts): Response names its method, and that method is one which really computes renewal function at finite time, either renewal equation $M = F + M * f$, convolution series $\sum_j P(S_j \le t)$ or simulation of process, so that giving $t/\mu$ or asymptotic expansion as method loses this point, even when number happens to come out near key, because no usable closed form is known for this law.
- c4 (3 pts): Response earns this by any one of four tests. It halves step at least twice and each change in value is at most half the one before and under $0.0005$, or it gives Richardson value from two steps of stated order which agrees with a third finer run within $0.0005$, or two different schemes agree within $0.0005$, or it states error bound or 95 per cent band which lies wholly in $1.445$ to $1.455$. One run at one step, and anything else, earns nothing.

Common wrong answers: 1.46, 1.44, 1.42, 1.40, 1.52, 1.72, 1.57, 1.22

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that no usable closed form is known for renewal function of this law, then they verify $M(3.5) = 1.45364$ three times and every route is numerical, where first route is product integration of renewal equation at four step sizes, second is convolution series $\sum_j P(S_j \le 3.5)$ with convolutions done numerically, and third is simulation of 400000 paths. After that notes table four discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each near miss reading of figure would give, then program and its full output come at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(3.5) = 1.453642 three independent ways (product integration of the renewal equation at four step sizes, the convolution series sum_j P(S_j <= 3.5), and a simulation of 400000 paths giving 1.4559 with standard error 0.0012); section 4 tables the discretisation schemes and what each value rounds to at 2 decimals; section 5 is the rounding trap (forcing k = 3 gives 1.57, cutting lambda to 1.69 gives 1.46); section 6 gives each closed-form shortcut and each near-miss reading, none of which rounds to 1.45; section 8 embeds verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md.