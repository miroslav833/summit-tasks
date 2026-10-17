task11 renewal residual life

Domain: Mathematics. Subdomain: Probability: renewal theory (limiting residual life, inspection paradox) with heavy-tailed inter-arrival times

## Question

The figure shows, on logarithmic axes, the survival function $S(t) = P(X > t)$ of the inter-arrival time $X$ of a renewal process. $X$ has a log-logistic distribution, $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$, with $\lambda > 0$ and $k > 0$ not given. The curve is drawn so that it passes exactly through gridline crossings at two of the $t$ values labelled on the axis, one of them $t = 6$. Determine $\lambda$ and $k$ from the figure.

Let $m = E[X]$ and let $r(t)$ be the residual life at time $t$, the time from $t$ until the next arrival of the process. Find $\lim_{t \to \infty} E[r(t)]\,/\,m$ to two significant figures.

## Answer

0.80

## Solution

Step 1: The parameters from the figure.
The gridlines of the vertical axis sit at $1$, $2$ and $5$ in every decade. Checking the curve at each labelled $t$, it passes through a gridline crossing at exactly two of them, $(6, 0.02)$ and $(20, 0.0005)$; everywhere else it runs between lines (at $t = 4$ it is at about $0.066$, at $t = 8$ about $0.0083$, at $t = 10$ about $0.0042$, at $t = 15$ about $0.0012$). Since $(t/\lambda)^k = 1/S(t) - 1$, the two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, so $(10/3)^k = 1999/49 = 40.80$, $k = \ln 40.80/\ln(10/3) = 3.7087/1.2040 = 3.080$, and $\lambda = 6/49^{1/k} = 6/3.538 = 1.696$.

Step 2: The moments of $X$.
For the log-logistic distribution $E[X^r] = \lambda^r\,\Gamma(1 + r/k)\,\Gamma(1 - r/k) = \lambda^r\,\dfrac{\pi r/k}{\sin(\pi r/k)}$, finite for $r < k$. Here $k = 3.080 > 2$, so the second moment exists (the third does not). With $\pi/k = 1.0200$: $E[X] = 1.696 \times 1.0200/\sin 1.0200 = 1.696 \times 1.0200/0.85221 = 2.030$; with $2\pi/k = 2.0400$: $E[X^2] = 1.696^2 \times 2.0400/\sin 2.0400 = 2.8766 \times 2.0400/0.89212 = 6.578$.

Step 3: The limiting residual life.
For a renewal process whose inter-arrival time has a finite second moment and a non-lattice distribution, the residual life $r(t)$ converges in distribution to the equilibrium distribution with density $S(t)/m$, and $E[r(t)] \to \int_0^\infty t\,S(t)\,dt/m = E[X^2]/(2m)$. This is the inspection paradox: the limit is not $m/2$, and for a heavy-tailed $X$ it can be close to or above $m$. Hence $\lim E[r(t)]/m = E[X^2]/(2m^2) = 6.578/(2 \times 2.030^2) = 6.578/8.243 = 0.798$. In closed form, $\dfrac{E[X^2]}{2E[X]^2} = \dfrac{(2\pi/k)\sin^2(\pi/k)}{2(\pi/k)^2 \sin(2\pi/k)} = \dfrac{k}{2\pi}\tan\dfrac{\pi}{k} = 0.49024 \times 1.6278 = 0.798$, independent of $\lambda$.

Step 4: Result.
$\lim_{t\to\infty} E[r(t)]/m = 0.798$, so to two significant figures $0.80$.

Taking the curve through near misses instead of the true crossings gives other answers: $(4, 0.05)$ with $(10, 0.005)$ gives $k = 2.56$ and $1.1$; $(4, 0.05)$ with $(20, 0.0005)$ gives $k = 2.89$ and $0.87$; $(3, 0.2)$ with $(8, 0.01)$ gives $k = 3.27$ and $0.74$; $(3, 0.2)$ with $(15, 0.001)$ gives $k = 3.43$ and $0.71$; $(8, 0.01)$ with $(20, 0.0005)$ gives $k = 3.27$ and $0.74$; $(6, 0.02)$ with $(10, 0.005)$ gives $k = 2.75$ and $0.96$. The naive answers $1/2$ (half the mean) and $1$ ignore the inspection paradox; $E[X^2]/(2E[X]) = 1.62$ is the limit itself, not its ratio to the mean. None of these is the answer.

Answer: $0.80$.

## Rubric

- c1 (4 pts, final answer): Gives $0.80$ (any value that rounds to $0.80$ at two significant figures, such as $0.798$).
- c2 (2 pts): Identifies the crossings $(6, 0.02)$ and $(20, 0.0005)$ as the two the curve passes through and obtains $k = 3.08$ and $\lambda = 1.70$ from $(t/\lambda)^k = 1/S - 1$ (not a near miss such as $(4, 0.05)$, $(8, 0.01)$, $(10, 0.005)$ or $(15, 0.001)$).
- c3 (2 pts): Uses the limit $E[r(t)] \to E[X^2]/(2E[X])$ (equilibrium residual-life distribution with density $S(t)/m$), not $m/2$ or $m$, and notes that it requires $k > 2$.
- c4 (2 pts): Computes the log-logistic moments through $\Gamma(1 + r/k)\Gamma(1 - r/k) = (\pi r/k)/\sin(\pi r/k)$ or the equivalent Beta integral, reaching $E[X] = 2.03$ and $E[X^2] = 6.58$ (or the closed form $(k/2\pi)\tan(\pi/k)$).

Common wrong answers: 0.5, 1, 1.1, 0.87, 0.74

## References box

Limiting residual life of a renewal process (key renewal theorem, equilibrium distribution with density $S(t)/m$): W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI; S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, section 3.4. Moments of the log-logistic distribution through the Beta function: N. L. Johnson, S. Kotz and N. Balakrishnan, Continuous Univariate Distributions, vol. 2, 2nd ed., Wiley, 1995, chapter 23 (the Fisk distribution). The uploaded file verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa, solves $\lambda$ and $k$, and gives four computations of the answer (closed form, quadrature of the survival function, the Beta function, and quadrature of the equilibrium residual-life density), the values obtained from every pair of near-miss readings and from each wrong route, and the program with its output.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda and k; section 3 gives four computations of the answer (closed form, quadrature of the survival function, the Beta function, quadrature of the equilibrium residual-life density); section 4 lists the value from every pair of near-miss readings and from each wrong route; section 6 embeds the program verify_key.py with its full output.

## Screen

Final wording (one crossing named, t = 6): Opus 1/3 (one run found (6, 0.02) and (20, 0.0005) and gave 0.80; two runs paired the named crossing with an invented gridline at (10, 4e-3), which is not drawn, and gave 0.77), Sonnet 0/1 (claimed the rate axis has decade lines only, read (6, 0.01) and (15, 0.001), answered 1.2). Same figure without the hint: Opus 0/3 and Sonnet 0/1, every miss an invented gridline. Earlier figures: v1 (9 labels) Opus 3/3 with or without hint; v2 (16 labels, crossings at 5 and 30) Opus 2/3 and Sonnet 1/1 but only through a lucky decade-line pair that rounded to the key, now excluded by the scan. Details in the task11 row of note.md.