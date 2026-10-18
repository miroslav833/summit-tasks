task11 renewal function at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

Figure shows survival function $S(t) = P(X > t)$ on logarithmic axes, where $X$ is inter-arrival time of renewal process and $X$ follows log-logistic law, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

Curve passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$, and those two crossings together fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$ and process starts at time $0$, so find $E[N(6)]$ using $\lambda$ and $k$ which you read from figure. Neither parameter is round number, so carry both to at least 4 significant figures through whole calculation, because rounding them to 3 figures moves third decimal of answer.

This quantity has no closed form, and usual coarse schemes are still more than one per cent out at step which you would pick on first try, so refine step of your scheme, or extrapolate it, until third decimal stops moving. Say which method you used, then show numbers which convinced you it settled. There is one more thing, your final answer must be value rounded to 3 decimal places.

## Answer

2.705

## Solution

Horizontal gridlines sit at $1$, $2$, $5$ in each decade, and when you check curve against them it hits a crossing at exactly two labelled $t$, which are $(6, 0.02)$ and $(20, 0.0005)$, while at other labelled values it runs between lines, about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

From $(t/\lambda)^k = 1/S(t) - 1$ these two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other gives $(10/3)^k = 1999/49 = 40.80$, so $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Renewal function $M(t) = E[N(t)]$ solves $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for log-logistic law there is no closed form because Laplace transform of $f$ is not elementary, so $M$ has to come from numerical work. Mean is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, which puts $t = 6$ at about 3 mean gaps, and asymptotics are still bad that early.

For the key I took step $h$ on $[0, 6]$ and advanced $M$ by product integration on density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$, where $u = 0$ term drops because $f(0) = 0$ when $k > 1$, and here $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(6) = 2.70496$ every time.

Scheme choice is what decides this question, because all schemes below reach $2.70496$ in the limit but at third decimal they sit far apart, and at step which someone picks on first try none of them has settled.

Trapezoidal product rule on $dF$, implicit in $M_i$, is second order and gives $2.7496$ at $h = 1$, which is $1.65$ per cent high, then $2.7155$ at $h = 0.5$, $2.7076$ at $h = 0.25$ and $2.7056$ at $h = 0.125$, where none of them rounds to $2.705$ yet, and $h = 0.0625$ gives $2.7051$ which does.

Midpoint or lattice rule rounds arrival times to nearest node and comes from above slowly, giving $2.9501$, $2.8312$, $2.7678$, $2.7363$ and $2.7206$ at steps $1$, $0.5$, $0.25$, $0.125$, $0.0625$, so even $h = 0.03125$ with $2.7128$ has not reached $2.705$, while Richardson on its two coarsest values overshoots to $2.7916$.

Discrete renewal recursion is the one which people reach for, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$, and because each cell mass sits at right endpoint every renewal gets delayed by up to $h$, so it comes from below at first order with $2.2395$, $2.4417$, $2.5644$, $2.6322$ and $2.6679$ at same steps, none of them near $2.705$, and even at $h = 0.03125$ it is still $2.6863$. Richardson $2M(h/2) - M(h)$ fixes it earlier, where $2.6870$ from pair $(0.5, 0.25)$ and $2.7001$ from $(0.25, 0.125)$ are still short while $2.7046$ from $(0.0625, 0.03125)$ rounds to $2.705$.

That is why question asks for third decimal, because one run at one step tells you nothing and value has to be shown settled.

Two other routes confirm it. Convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$ with each $P(S_j \le 6)$ done by repeated numerical convolution of $f$ gives $2.70496$, and simulation of $400\,000$ paths gives $2.7068 \pm 0.0017$.

So $M(6) = 2.70496$, and rounding that to 3 decimals gives $2.705$, which is answer.

Parameters need 4 figures here and question says so, because $k = 3.080$ with $\lambda = 1.696$ gives $2.70500$ where third decimal is safe, while cutting them back to $k = 3.08$ with $\lambda = 1.70$ gives $2.6980$ and third decimal has already moved.

Rounding $k$ to $3$ with $\lambda = 4^{1/3}$ looks attractive but it breaks, because that law has $S(6) = 0.0182$ against drawn $0.0200$, a nine per cent gap which is visible on log axis, and it returns $M(6) = 2.8947$ which rounds to $2.895$.

Shortcuts all fail at this $t$ and third decimal catches each one of them. Elementary renewal theorem alone gives $t/E[X] = 6/2.030 = 2.9555$ and that is nine per cent high, asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535$ is $1.8$ per cent high because $t = 6$ is only about 3 mean gaps, common slip $t/m - 1/2 = 2.4555$ is far out, and $F(6) = 0.98$ is probability of at least one renewal which is different quantity.

Reading curve through near misses instead of real crossings also lands elsewhere, where $(6, 0.02)$ with $(8, 0.01)$ gives $3.64$, with $(10, 0.005)$ gives $3.13$, with $(15, 0.001)$ gives $2.50$ and with $(3, 0.2)$ gives $2.24$.

Answer: $2.705$.

## Rubric

- c1 (4 pts, final answer): Last line of response gives $2.705$, which is $E[N(6)] = 2.70496$ after rounding to 3 decimals as question asks for. Values which come from stopping too early are wrong here, and these are $2.750$ from coarse trapezoid at $h = 1$, $2.668$ from right-endpoint recursion at $h = 0.0625$, then $2.687$ and $2.792$ from two Richardson overshoots, $2.754$ from asymptotic expansion, $2.956$ from $t/E[X]$ and $2.895$ when $k$ was rounded to $3$.
- c2 (1 pts): Response says which parameters it used and they are $k = 3.080$ with $\lambda = 1.696$ at 4 figures, taken from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$. Rounding $k$ to $3$ loses this point, because that law gives $2.8947$ which rounds to $2.895$.
- c3 (2 pts): Response names its method and that method actually computes finite-time renewal function, so it is renewal equation $M = F + M * f$, or convolution series $\sum_j P(S_j \le t)$, or simulation of process. This law has no closed form, so giving $t/\mu$ or asymptotic expansion as the method loses this point even when number lands in range.
- c4 (3 pts): Response shows third decimal has settled in one of four ways. It halves step at least twice with ratio of successive changes between 1.5 and 2.5 for first order or 3 and 5 for second order and last change under $0.0005$, or Richardson result agrees with finer run within $0.0005$, or two schemes agree within $0.0005$, or simulation gives 95 per cent confidence interval whose both ends round to same third decimal. Two values sitting close, with no order and no error estimate, earns nothing.

Common wrong answers: 2.750, 2.668, 2.754, 2.956, 2.895, 2.687, 2.792, 2.456

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that renewal function of this law cannot be written in closed form, then they verify $M(6) = 2.70496$ three times and every route is numerical, where first route is product integration of renewal equation at four step sizes, second is convolution series $\sum_j P(S_j \le 6)$ with convolutions done numerically, and third is simulation of 400000 paths. After that notes table four discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each near miss reading of figure would give, then program and its full output come at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(6) = 2.704964 three independent ways (the renewal equation M = F + M * f by product integration at four step sizes, the convolution series sum_j P(S_j <= 6), and a simulation of 400000 paths giving 2.7068 with standard error 0.0017); section 4 is the discretisation trap (the discrete renewal recursion converges from below: 2.24 at step 1, 2.44 at step 0.5, 2.56 at step 0.25, and the Richardson repair); section 5 is the rounding trap (forcing k = 3 gives 2.9); section 6 gives the value returned by each closed-form shortcut (t/m = 2.96, the asymptotic expansion 2.75, t/m - 1/2 = 2.46, F(6) = 0.98) and by each near-miss reading of the figure, none of which rounds to 2.7; section 8 embeds the program verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 2/3 and Sonnet 1/1. The two correct Opus runs used product integration on the density and a midpoint-mass scheme, both extrapolated, reaching 2.7048 and 2.7053. The miss used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (answered 2.6); an earlier run of the same wording overshot a Richardson step to 2.79 (answered 2.8). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md.