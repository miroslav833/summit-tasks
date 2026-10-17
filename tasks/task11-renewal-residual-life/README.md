task11 renewal function at finite time

SUBMIT AS A NEW SUBMISSION (Import .zip on the Submit page), not as a revision of SUM-MVB7DTW7: the revision editor keeps the old bandwidth references text, which was the first blocking problem on the v4 consistency check.

Domain: Mathematics. Subdomain: Probability: renewal theory (the renewal function at finite time, numerical solution of the renewal equation) with heavy-tailed inter-arrival times

## Question

The figure shows, on logarithmic axes, the survival function $S(t) = P(X > t)$ of the inter-arrival time $X$ of a renewal process, where $X$ has a log-logistic distribution, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$. The curve passes exactly through gridline crossings at two of the $t$ values labelled on the axis, at $t = 6$ and $t = 20$, and reading those two crossings fixes $\lambda$ and $k$.

Let $N(t)$ be the number of renewals in $(0, t]$, the arrivals of the process, with the process starting at time $0$. Using the $\lambda$ and $k$ fixed by the figure, find $E[N(6)]$ to two significant figures. Neither parameter is a round number, and the answer is wanted to a relative accuracy better than one per cent, so carry the parameters to three significant figures and make sure any numerical scheme you use has converged to that accuracy. Give only this number as the answer.

## Answer

2.7

## Solution

Step 1: The parameters from the figure.
The gridlines of the vertical axis sit at $1$, $2$ and $5$ in every decade. Checking the curve at each labelled $t$, it passes through a gridline crossing at exactly two of them, $(6, 0.02)$ and $(20, 0.0005)$; everywhere else it runs between lines (at $t = 4$ it is at about $0.066$, at $t = 8$ about $0.0083$, at $t = 10$ about $0.0042$, at $t = 15$ about $0.0012$). Since $(t/\lambda)^k = 1/S(t) - 1$, the two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, so $(10/3)^k = 1999/49 = 40.80$, $k = \ln 40.80/\ln(10/3) = 3.7087/1.2040 = 3.080$, and $\lambda = 6/49^{1/k} = 6/3.538 = 1.696$.

Step 2: Why no formula finishes the job.
The renewal function $M(t) = E[N(t)]$ satisfies $M(t) = F(t) + \int_0^t M(t-u)\,f(u)\,du$, and for the log-logistic law this equation has no closed-form solution: the Laplace transform of $f$ is not elementary, so $M$ must be obtained numerically. The mean is $E[X] = \lambda\,(\pi/k)/\sin(\pi/k) = 2.030$, so $t = 6$ is only about three mean gaps, far too early for the asymptotics to be accurate.

Step 3: Solving the renewal equation, and the discretisation trap.
Discretise $[0, 6]$ with step $h$ and advance $M$ by product integration on the density, $M(t_i) = F(t_i) + \sum_j w_j f(u_j) M(t_i - u_j)$ with trapezoidal weights $w_j$; the $u = 0$ term vanishes because $f(0) = 0$ for $k > 1$. Here $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$. This scheme is second order and already stable at a coarse grid: $1000$, $2000$, $4000$ and $8000$ intervals all give $M(6) = 2.70496$.

The choice of scheme decides the answer, and that is the crux of the question. The two natural hand schemes converge to $2.705$ from opposite sides and both need care: a midpoint or lattice rule that rounds arrival times to the nearest node approaches from above, giving $2.9501$, $2.8312$, $2.7678$, $2.7363$, $2.7206$ at steps $1$, $0.5$, $0.25$, $0.125$, $0.0625$, and a Richardson step taken on its two coarsest values overshoots to $2.79$; a right-endpoint rule approaches from below, as set out next. A trapezoidal product rule on the measure $dF$, taken implicitly in $M_i$, is second order and already gives $2.7496$, $2.7155$, $2.7076$ at steps $1$, $0.5$, $0.25$: it rounds correctly even on a coarse grid. The obvious hand method is the discrete renewal recursion instead, $M_i = F(t_i) + \sum_{j=1}^{i} p_j M_{i-j}$ with cell masses $p_j = F(t_j) - F(t_{j-1})$. That scheme places each cell's mass at its right endpoint, so it delays every renewal by up to $h$ and converges to the answer only from below, at first order: $h = 1$ gives $2.2395$, $h = 0.5$ gives $2.4417$, $h = 0.25$ gives $2.5644$, $h = 0.125$ gives $2.6322$. A step small enough to be read off by hand therefore returns $2.2$, $2.4$ or $2.6$, none of them the answer; the step has to come down to about $0.06$, or two steps have to be combined by Richardson extrapolation ($2M(h/2) - M(h)$, which gives $2.6870$ from the pair $0.5, 0.25$ and $2.7001$ from the pair $0.25, 0.125$).

An independent evaluation as the convolution series $M(t) = \sum_{j \ge 1} P(S_j \le t)$, with each $P(S_j \le 6)$ computed by repeated numerical convolution of $f$, gives $2.70496$ as well, and a simulation of $400\,000$ paths gives $2.7068 \pm 0.0017$.

Step 4: Result.
$M(6) = 2.705$, so to two significant figures $2.7$.

Rounding $k$ to $3$ and $\lambda$ to $4^{1/3}$ is tempting and wrong: that law gives $S(6) = 0.0182$ against the drawn $0.0200$, a visible nine per cent gap on a logarithmic axis, and it would give $M(6) = 2.89$, that is $2.9$.

The shortcuts all fail at this $t$. The elementary renewal theorem alone, $t/E[X] = 6/2.030 = 2.96$, gives $3.0$. The asymptotic expansion $t/m + (E[X^2] - 2m^2)/(2m^2) = 2.7535$ is still $1.8$ per cent high and gives $2.8$. The common slip $t/m - 1/2 = 2.46$ gives $2.5$, and $F(6) = 0.98$ is the probability of at least one renewal, not their expected number. Taking the curve through near misses instead of the true crossings also lands elsewhere: $(6, 0.02)$ with $(8, 0.01)$ gives $3.6$, with $(10, 0.005)$ gives $3.1$, with $(15, 0.001)$ gives $2.5$, with $(3, 0.2)$ gives $2.2$. None of these is the answer.

Answer: $2.7$.

## Rubric

- c1 (4 pts, final answer): Gives $2.7$ as the final answer (any value that rounds to $2.7$ at two significant figures, such as $2.705$).
- c2 (1 pts): Reads the two crossings as $(6, 0.02)$ and $(20, 0.0005)$ and obtains the intermediate values $k = 3.08$ and $\lambda = 1.70$ from $(t/\lambda)^k = 1/S - 1$, without rounding $k$ to $3$.
- c3 (2 pts): Recognises that $E[N(t)]$ at a finite $t$ needs the renewal equation $M = F + M * f$ (or the convolution series $\sum_j P(S_j \le t)$) because the log-logistic renewal function has no closed form, rather than quoting an asymptotic formula.
- c4 (3 pts): Controls the discretisation: either uses a scheme accurate on a coarse grid (product integration on the density) or refines the discrete recursion to a step near $0.06$ or extrapolates two steps correctly, reaching $2.70$ to $2.71$ before rounding. A coarse discrete recursion stopping at $2.2$, $2.4$ or $2.6$, a first-order extrapolation that overshoots to $2.75$, the asymptotic value $2.75$, or $t/E[X] = 2.96$, does not earn this point.

Common wrong answers: 2.9, 3.0, 2.8, 2.5, 2.6

## References box

The renewal equation and the renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI; S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, where the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ is derived and its slow approach noted. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Moments of the log-logistic distribution through the Beta function: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). The uploaded file verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa, solves $\lambda$ and $k$, and computes $M(6)$ three independent ways (the renewal equation at four step sizes, the convolution series, and a simulation of 400000 paths), together with the value returned by each shortcut and by each near-miss reading, and the program with its output.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes M(6) = 2.704964 three independent ways (the renewal equation M = F + M * f by product integration at four step sizes, the convolution series sum_j P(S_j <= 6), and a simulation of 400000 paths giving 2.7068 with standard error 0.0017); section 4 is the discretisation trap (the discrete renewal recursion converges from below: 2.24 at step 1, 2.44 at step 0.5, 2.56 at step 0.25, and the Richardson repair); section 5 is the rounding trap (forcing k = 3 gives 2.9); section 6 gives the value returned by each closed-form shortcut (t/m = 2.96, the asymptotic expansion 2.75, t/m - 1/2 = 2.46, F(6) = 0.98) and by each near-miss reading of the figure, none of which rounds to 2.7; section 8 embeds the program verify_key.py with its full output.

## Screen

Final wording (both crossings named, parameters stated not to be round, one per cent accuracy demanded): Opus 1/3 and Sonnet 1/1. The correct run used a midpoint-mass scheme at steps 1 and 0.5 and extrapolated to 2.7053. The two misses were numerical, not visual: one used the same scheme but Richardson-extrapolated its two coarsest values and overshot to 2.79 (2.8); the other used a right-endpoint lattice rule, calibrated its own error law against a second-order convolution and landed at 2.63 (2.6). Earlier wordings on the same figure, before both crossings were named, gave Opus 0/3 three times over, every miss a sub-pixel misreading of the second crossing; that is why the stem now names both. See the task11 row of note.md for the whole sequence.