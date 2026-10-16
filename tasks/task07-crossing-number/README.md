# task07: fatigue life from a crack-growth plot with closure

Domain: Engineering. Subdomain: Fatigue and fracture of titanium alloys

## Question

The figure shows fatigue crack growth data for a powder injection moulded alpha plus beta titanium alloy: the crack growth rate $\mathrm{d}a/\mathrm{d}N$ against the stress intensity factor range $\Delta K$ on logarithmic axes, measured on compact tension specimens at the load ratios $R = 0.1$ (filled circles) and $R = 0.5$ (open squares). The two straight lines are the Paris fits of the data above the threshold region, the solid line for $R = 0.5$ and the dashed line for $R = 0.1$. Each line passes exactly through its two crosses, and every cross sits on an intersection of gridlines.

Take the following as given. Crack growth in this alloy is governed by the effective range $\Delta K_{\mathrm{eff}} = U \, \Delta K$, where the closure factor $U$ depends only on the load ratio, and in the Paris regime $\mathrm{d}a/\mathrm{d}N = C \, (\Delta K_{\mathrm{eff}})^{n}$ with the same $C$ and $n$ at every load ratio. The $R = 0.5$ data are free of crack closure, so $U = 1$ at $R = 0.5$, and $U$ varies linearly with $R$ between $R = 0.1$ and $R = 0.5$.

A plate of this alloy of width $W = 20$ mm carries a remote tensile stress that cycles with the stress range $\Delta\sigma = 250$ MPa at the load ratio $R = 0.3$. A surface pore has started a through-thickness edge crack of depth $a_0 = 0.6$ mm. The stress intensity factor of the edge crack is $K = Y \sigma \sqrt{\pi a}$ with $Y = 1.12 - 0.231\,(a/W) + 10.55\,(a/W)^2 - 21.72\,(a/W)^3 + 30.39\,(a/W)^4$. The plate fails when the maximum stress intensity factor in a cycle reaches the fracture toughness $K_{\mathrm{IC}} = 60$ MPa$\sqrt{\mathrm{m}}$. Neglect the threshold, so that the Paris law applies from $a_0$ onwards.

How many load cycles does the plate survive from the crack depth $a_0$ to failure? Give the number of cycles to two significant figures.

## Answer

$1.1 \times 10^{5}$ cycles (two significant figures; exact model value 110212)

## Solution

Step 1: Read the Paris constants from the $R = 0.5$ line.
The solid line passes through $(\Delta K, \mathrm{d}a/\mathrm{d}N) = (5, 10^{-9})$ and $(50, 10^{-6})$, in MPa$\sqrt{\mathrm{m}}$ and m/cycle. A factor $10$ in $\Delta K$ gives a factor $10^{3}$ in rate, so $n = \log(10^{3}) / \log(10) = 3$. Since $U = 1$ at $R = 0.5$, $C = 10^{-9} / 5^{3} = 8 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^{3}$.

Step 2: Read the closure factor at $R = 0.1$ from the dashed line.
The dashed line passes through $(10, 10^{-9})$ and $(100, 10^{-6})$, so it has the same slope $n = 3$ and reaches a given rate at twice the $\Delta K$ of the $R = 0.5$ line. The same rate means the same $\Delta K_{\mathrm{eff}}$, so $U(0.1) \cdot 10 = 1 \cdot 5$ and $U(0.1) = 0.5$.

Step 3: Closure factor at the service load ratio.
With $U$ linear in $R$ between $U(0.1) = 0.5$ and $U(0.5) = 1$, at $R = 0.3$ (the midpoint) $U = 0.5 + \dfrac{0.3 - 0.1}{0.5 - 0.1}\,(1 - 0.5) = 0.75$. The growth law in service is therefore $\mathrm{d}a/\mathrm{d}N = 8 \times 10^{-12}\,(0.75\,\Delta K)^{3}$ with $\Delta K = Y \Delta\sigma \sqrt{\pi a}$.

Step 4: Critical crack depth.
The maximum stress in the cycle is $\sigma_{\max} = \Delta\sigma / (1 - R) = 250 / 0.7 = 357.1$ MPa. Failure occurs when $Y \sigma_{\max} \sqrt{\pi a} = K_{\mathrm{IC}} = 60$ MPa$\sqrt{\mathrm{m}}$. At $a = 4.40$ mm, $a/W = 0.220$, $Y = 1.4197$, $\sqrt{\pi a} = 0.11757$ $\sqrt{\mathrm{m}}$ and $K_{\max} = 59.6$; at $a = 4.50$ mm, $Y = 1.4326$, $\sqrt{\pi a} = 0.11890$ and $K_{\max} = 60.8$. Interpolating, $a_c = 4.43$ mm ($a_c/W = 0.222$, $Y = 1.424$).

Step 5: Integrate the growth law.
$N = \displaystyle\int_{a_0}^{a_c} \frac{\mathrm{d}a}{C\,(U Y \Delta\sigma \sqrt{\pi a})^{3}} = \frac{1}{C\,(U \Delta\sigma)^{3}\,\pi^{3/2}} \int_{a_0}^{a_c} \frac{\mathrm{d}a}{Y^{3} a^{3/2}}$, and $C\,(U\Delta\sigma)^{3}\,\pi^{3/2} = 8 \times 10^{-12} \cdot 187.5^{3} \cdot 5.5683 = 2.9364 \times 10^{-4}$ m$^{-1/2}$.
With the substitution $a = u^{2}$ the integral becomes $\displaystyle\int_{u_0}^{u_c} \frac{2\,\mathrm{d}u}{Y^{3} u^{2}}$ with $u_0 = \sqrt{0.0006} = 0.02449$ and $u_c = \sqrt{0.004432} = 0.06657$. Simpson's rule on eight panels ($h = 0.005260$) uses the integrand values $2/(Y^{3}u^{2})$ at $a = 0.600, 0.885, 1.226, 1.622, 2.073, 2.580, 3.142, 3.759, 4.432$ mm, where $Y = 1.1220, 1.1287, 1.1409, 1.1604, 1.1887, 1.2275, 1.2784, 1.3430, 1.4238$ and the integrand is $2359.9, 1571.1, 1098.5, 789.2, 574.3, 419.1, 304.7, 219.6, 156.4$; the rule gives $32.38$ (the exact value of the integral is $32.36$). Hence $N = 32.36 / (2.9364 \times 10^{-4}) = 1.10 \times 10^{5}$ cycles.

Step 6: Result.
The plate survives $1.1 \times 10^{5}$ cycles. Using the $R = 0.1$ line as it stands ($U = 0.5$) gives $3.7 \times 10^{5}$ cycles, using the $R = 0.5$ line as it stands ($U = 1$) gives $4.6 \times 10^{4}$, and holding $Y$ at $1.12$ throughout gives $1.3 \times 10^{5}$; only the closure factor interpolated to $R = 0.3$ together with the varying $Y$ gives the stated result.

Answer: $1.1 \times 10^{5}$ cycles.

## Rubric

- c1 (5 pts, final answer): Gives $1.1 \times 10^{5}$ cycles (110000 to two significant figures).
- c2 (1 pts): Reads the Paris exponent $n = 3$ and the constant $C = 8 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^{3}$ from the $R = 0.5$ line.
- c3 (2 pts): Obtains the closure factor $U(0.1) = 0.5$ from the horizontal shift between the two lines and interpolates to $U = 0.75$ at $R = 0.3$.
- c4 (1 pts): Finds the critical crack depth $a_c = 4.4$ mm (accept 4.3 to 4.5 mm) from $K_{\max} = K_{\mathrm{IC}}$ with $\sigma_{\max} = \Delta\sigma/(1 - R) = 357$ MPa.
- c5 (1 pts): Integrates $\mathrm{d}a/\mathrm{d}N = C (U Y \Delta\sigma \sqrt{\pi a})^{3}$ from $a_0$ to $a_c$ with $Y$ varying along the integration (numerically or by a stated quadrature), not held constant.

Common wrong answers: $3.7 \times 10^{5}$, $4.6 \times 10^{4}$, $2.0 \times 10^{5}$, $1.3 \times 10^{5}$

## References box

Crack closure and the effective stress intensity range: W. Elber, The significance of fatigue crack closure, in Damage Tolerance in Aircraft Structures, ASTM STP 486 (1971), 230-242. The Paris relation: P. C. Paris and F. Erdogan, A critical analysis of crack propagation laws, Journal of Basic Engineering 85 (1963), 528-534. The edge-crack geometry factor used in the stem is the standard single-edge-notch polynomial, for instance in H. Tada, P. C. Paris and G. R. Irwin, The Stress Analysis of Cracks Handbook, 3rd edition, ASME Press (2000). Closure effects and load-ratio dependence of crack growth in titanium alloys: R. O. Ritchie, Mechanisms of fatigue-crack propagation in ductile and brittle solids, International Journal of Fracture 100 (1999), 55-83. The uploaded file verification_notes.txt gives the model from which the figure was generated (the two fit lines are exact, through the marked anchors), recomputes the Paris constants and the closure factors from the anchors, solves for the critical crack depth, integrates the growth law by two independent routes (scipy adaptive quadrature; mpmath tanh-sinh quadrature at 30 digits plus a composite Simpson rule with Richardson extrapolation), evaluates every plausible wrong route, and embeds the program with its output.

## Verify field

Section 2 of verification_notes.txt gives the model that generated the figure (the solid fit through (5, 1e-9) and (50, 1e-6), the dashed fit through (10, 1e-9) and (100, 1e-6), hence n = 3, C = 8e-12 and U(0.1) = 0.5, U(0.3) = 0.75); section 3 gives the critical crack depth 4.43 mm; section 4 gives the life 110212 cycles by scipy quadrature and independently by mpmath tanh-sinh quadrature and a composite Simpson rule, and shows the value is 4.3 percent away from the nearest two-significant-figure rounding boundary; section 5 lists the plausible wrong routes with their values; section 6 embeds the program verify_key.py with its full output.

## Screen

Screen 2026-10-17, figure plus stem only, no web, no code: Opus 3/3 correct, each in about two minutes and 45k tokens (anchors read exactly, n = 3, C = 8e-12, U(0.1) = 0.5 from the factor-2 shift, U(0.3) = 0.75, a_c = 4.43 mm from sigma_max = 357 MPa, then the substitution u = a^(-1/2) and a nine-point Simpson rule giving 1.10e5). Sonnet 1/1 correct by the same route in 2.5 minutes. Tally: Opus 3/3, Sonnet 1/1. Too easy; held back, the owner decides.