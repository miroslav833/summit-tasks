task11 variance of the renewal count at finite time

REVISE SUM-MVBYB83A with these fields. Do not create a new submission. That entry was made from this zip, so its References text is already clean; SUM-MVB7DTW7 is the older bandwidth entry and keeps stale References text in the revision editor.

Domain: Mathematics. Subdomain: Probability: renewal theory (variance of the renewal counting process at finite time, numerical solution of renewal equations) with heavy-tailed inter-arrival times

## Question

Figure shows, on logarithmic axes, survival function $S(t) = P(X > t)$ of inter-arrival time $X$ of renewal process, and $X$ is log-logistic, so that $S(t) = 1/(1 + (t/\lambda)^k)$ for $t > 0$.

That curve, which looks like any smooth bend on log paper, passes exactly through gridline crossings at two of labelled $t$ values, at $t = 6$ and $t = 20$, and those two crossings, and nothing else in figure, fix $\lambda$ and $k$.

$N(t)$ counts renewals in $(0, t]$, process having started at time $0$, and what is wanted is $\mathrm{Var}[N(3)]$, variance of number of renewals by time $3$, with $\lambda$ and $k$ as you read them from figure. Neither parameter is round number, and rounding them to 3 significant figures already moves third decimal of answer, so carry both to at least 4 significant figures through whole calculation.

No usable closed form is known for this quantity, so say which method you used and show your working, and give your final answer as value rounded to 3 decimal places.

## Answer

0.520

## Solution

Gridlines of survival axis, which run across figure horizontally, sit at $1$, $2$ and $5$ in each decade, and when curve is checked against them at every labelled $t$ it is found to pass through a crossing at two of them only, $(6, 0.02)$ and $(20, 0.0005)$, while at others it runs between lines, being about $0.066$ at $t = 4$, about $0.0083$ at $t = 8$, about $0.0042$ at $t = 10$ and about $0.0012$ at $t = 15$.

Since $(t/\lambda)^k = 1/S(t) - 1$, two crossings give $(6/\lambda)^k = 49$ and $(20/\lambda)^k = 1999$, and dividing one by other leaves $(10/3)^k = 1999/49 = 40.80$, from which $k = \ln 40.80/\ln(10/3) = 3.080$ and then $\lambda = 6/49^{1/k} = 1.696$.

Since $P(N(3) \ge n) = F_n(3)$, where $F_n$ is distribution function of $n$th arrival time $S_n$, mean is $E[N(3)] = \sum_n F_n(3)$ and second moment is $E[N(3)^2] = \sum_n (2n - 1) F_n(3)$, because $n^2$ is sum of first $n$ odd numbers, and variance is second moment less square of mean. Same thing in renewal form reads $E[N(t)^2] = M(t) + 2\int_0^t M(t-x)\,dM(x)$ with $M(t) = E[N(t)]$, and for log-logistic law no usable closed form is known for either one, so both must come from numerical work.

For key I took step $h$ on $[0, 3]$ and solved $M(t) = F(t) + \int_0^t M(t-u) f(u)\,du$ by product integration on density with trapezoidal weights, where $F(t) = 1 - S(t)$ and $f(t) = (k/\lambda)(t/\lambda)^{k-1}/(1 + (t/\lambda)^k)^2$, and then took $2\int_0^3 M(3-x)\,dM(x)$ on same grid. On $1000$, $2000$, $4000$ and $8000$ intervals this gives $M(3) = 1.201419$ and $\mathrm{Var}[N(3)] = 0.520129$ every time, and to 3 decimals that is $0.520$.

Convolution series gives same number term by term, with $F_1(3) = 0.852799$, $F_2(3) = 0.317143$, $F_3(3) = 0.030527$, $F_4(3) = 0.000938$ and $F_5(3) = 0.000012$, which sum to $E[N(3)] = 1.201419$, while $\sum_n (2n - 1) F_n(3) = 1.963537$, so that variance is $1.963537 - 1.201419^2 = 0.520129$. Simulation of one million paths gives $0.5195 \pm 0.0007$, which agrees within one standard error, though it is too rough to fix third decimal by itself.

Third decimal is what makes this question hard, because key sits only $0.00037$ below edge of its rounding bin, and coarse schemes miss it. Coupled trapezoid scheme on $dF$, which runs $M = F + M * dF$ alongside $A = M + A * dF$ and takes variance as $2A - M - M^2$, gives $0.5501$ at $h = 0.5$, $0.5274$ at $h = 0.25$, $0.5220$ at $h = 0.125$ and $0.5206$ at $h = 0.0625$, which last still rounds to $0.521$, and only second order Richardson from $(0.25, 0.125)$, which gives $0.52012$, comes to $0.520$. Midpoint lattice convolution, which puts each cell mass at its centre, comes down from above and comes slowly, with $0.5730$, $0.5456$ and $0.5326$ at steps $0.5$, $0.25$ and $0.125$, not one of them right.

Parameters must be carried to 4 figures, as question says, since $k = 3.080$ with $\lambda = 1.696$ gives $0.520202$ and third decimal is safe, whereas $k = 3.08$ with $\lambda = 1.70$ gives $0.518861$ and it has already moved to $0.519$. Rounding $k$ all way to $3$, with $\lambda = 4^{1/3}$, is tempting, but that law has $S(6) = 0.0182$ against drawn $0.0200$, a gap of nine per cent which can be seen on log axis, and it returns $0.5771$.

Shortcuts all fail here, for treating $N(3)$ as Poisson, so that variance equals mean, gives $1.201$, asymptotic formula $\sigma^2 t/\mu^3$ gives $0.881$ because $t = 3$ is only about one and a half mean gaps, and forgetting to subtract square of mean leaves $1.964$. Writing $E[N^2] = M + 2(M * dF)$, with $dF$ where $dM$ belongs, gives $0.455$, which is another thing altogether.

Answer: $0.520$.

## Rubric

- c1 (4 pts, final answer): Final answer is $0.520$, which is $\mathrm{Var}[N(3)] = 0.520129$ rounded to 3 decimals as question asks, and it is reached by any valid numerical method which working documents, such as renewal equations, convolution series, direct recursion on $P(N(3) = n)$ or simulation precise enough for third decimal, so bare number gets nothing here. Values which come of coarse grids or wrong formulas are wrong, these being $0.521$, $0.522$, $0.519$, $0.546$, $0.881$, $1.201$, $1.964$ and $0.455$.
- c2 (1 pts): Response states parameters it used, and they are $k = 3.080$ and $\lambda = 1.696$ to at least 4 figures, as got from $(t/\lambda)^k = 1/S - 1$ at crossings $(6, 0.02)$ and $(20, 0.0005)$, and a response which cuts them to $k = 3.08$ and $\lambda = 1.70$ loses this point, since that gives $0.519$.
- c3 (2 pts): Response uses correct second moment identity, either $E[N^2] = \sum_n (2n - 1) F_n(3)$ or $E[N^2] = M + 2\int_0^t M(t-x)\,dM(x)$, and then subtracts $M(3)^2$, so that taking $N(3)$ as Poisson, using asymptotic $\sigma^2 t/\mu^3$, or putting $dF$ where $dM$ belongs loses this point, because none of these is variance at finite time.
- c4 (3 pts): Working earns this when it shows third decimal has settled, by any one of four tests. It halves step at least twice and each change in value is at most half the one before and under $0.0002$, or it gives Richardson value from two steps of stated order which agrees with a third finer run within $0.0002$, or two different schemes agree within $0.0002$, or it states error bound or 95 per cent band which lies wholly in $0.5195$ to $0.5205$. Anything weaker earns nothing.

Common wrong answers: 0.521, 0.522, 0.519, 0.546, 0.881, 1.201, 1.964, 0.455

## References box

Renewal equation and renewal function: W. Feller, An Introduction to Probability Theory and Its Applications, vol. II, 2nd ed., Wiley, 1971, chapter XI. S. M. Ross, Stochastic Processes, 2nd ed., Wiley, 1996, sections 3.3 and 3.4, which derives the asymptotic expansion $M(t) = t/\mu + (\sigma^2 - \mu^2)/(2\mu^2) + o(1)$ and notes how slowly it comes in. Numerical solution of renewal equations by product integration: P. Linz, Analytical and Numerical Methods for Volterra Equations, SIAM, 1985, chapter 7. Uploaded file verification_notes.txt gives the two gridline crossings the curve was drawn through, the distance from curve to nearest gridline at every other labelled abscissa, and solves $\lambda$ and $k$ from the crossings. Notes record that no usable closed form is known for these quantities under this law, then they verify $\mathrm{Var}[N(3)] = 0.520129$ three times and every route is numerical, where first route is renewal equation by product integration with $E[N^2] = M + 2 M * dM$ at four step sizes, second is convolution series $\sum_n (2n - 1) F_n(3)$ with convolutions done numerically, and third is simulation of one million paths. After that notes table two discretisation schemes with value which each one returns, what happens when $k$ is rounded to $3$, and what each wrong formula would give, then program and its full output come at the end.

## Verify field

Section 1 of verification_notes.txt states the two gridline crossings the curve was drawn through, (6, 0.02) and (20, 0.0005), and the distance of the curve from the nearest gridline at every other labelled abscissa; section 2 solves lambda = 1.696 and k = 3.080; section 3 computes Var[N(3)] = 0.520129 three independent ways (renewal equation with E[N^2] = M + 2 M * dM at four step sizes, the convolution series sum (2n - 1) F_n(3), and a simulation of 1000000 paths giving 0.5195 with standard error 0.0007); section 4 tables two discretisation schemes and what each value rounds to at 3 decimals; section 5 is the rounding trap (three-figure parameters give 0.519, forcing k = 3 gives 0.577); section 6 gives each wrong formula, none of which rounds to 0.520; section 8 embeds verify_key.py with its full output.

## Screen

Local screen 2026-10-18 on this exact wording (figure plus stem, no code): Opus 2 of 3 correct, Sonnet 1 of 1 correct. Opus answers 0.521 (correct method, slip in the final subtraction: 1.963520 - 1.443396 written as 0.52112), 0.520 (renewal equations for M and E[N(N-1)]/2 at h = 0.1), 0.520 (convolution series with Simpson, 0.52013). Sonnet 0.520 (coupled trapezoid at three steps and a polynomial fit). The same question at 2 decimals scored Opus 3 of 3 and Sonnet 0 of 1 (Sonnet 0.56 from a coarse midpoint lattice). Earlier E[N(t)] versions: t = 6 at 3 decimals gave Summit 1/5 with 4 cut-offs; t = 3 at 2 decimals Summit 5/5; t = 3.5 at 2 decimals local Opus 3/3 and Sonnet 1/1, with or without the refine hint.