task05 v5 (Engineering replacement)

Domain: Engineering. Subdomain: Fatigue and fracture mechanics of titanium alloys (defect-initiated fatigue, short-crack threshold)

## Question

The figure shows long-crack fatigue crack growth data for a Ti-6Al-7Nb alloy produced by metal injection moulding, measured on compact tension specimens at a load ratio $R = 0.1$ in laboratory air. The solid line is a fit of the Klesnil and Lukas form $da/dN = C\,(\Delta K^m - \Delta K_{th}^m)$ with a long-crack threshold $\Delta K_{th} = 4.0$ MPa m$^{1/2}$; it is drawn so that it passes exactly through gridline crossings at two of the $\Delta K$ values labelled on the axis, both of them below $30$ MPa m$^{1/2}$. Determine $C$ and $m$ from the figure ($da/dN$ in m/cycle, $\Delta K$ in MPa m$^{1/2}$). Smooth specimens of the same material have a fatigue limit at $R = 0.1$ of $\Delta\sigma_w = 500$ MPa (stress range, $10^7$ cycles).

A component of this material carries a cyclic stress range $\Delta\sigma = 450$ MPa at $R = 0.1$. Fractography of a failed component shows that the crack started at a surface pore of size $\sqrt{\mathrm{area}} = 50$ $\mu$m, where area is the pore area projected on the plane normal to the stress. Treat the pore as a crack of size $a = \sqrt{\mathrm{area}}$ from the first cycle and use $\Delta K = 0.65\,\Delta\sigma\sqrt{\pi a}$ for the whole growth, with $a$ standing for $\sqrt{\mathrm{area}}$ of the growing crack. For a crack of size $a$ replace the long-crack threshold in the growth law by $\Delta K_{th}(a) = \Delta K_{th}\sqrt{a/(a + a_0)}$, where the length $a_0$ is fixed by requiring that the smooth-specimen fatigue limit and the long-crack threshold are consistent under the same stress intensity relation.

How many cycles does the crack need to grow from the pore to $a = 0.5$ mm? Give the answer to two significant figures.

## Answer

1.4 \times 10^5 cycles

## Solution

Step 1: Constants from the figure.
The gridlines of the rate axis sit at 1, 2 and 5 in every decade. Checking the fitted curve at each labelled $\Delta K$, it passes through a gridline crossing at exactly two of them: $(6, 2 \times 10^{-9})$ and $(20, 1 \times 10^{-7})$; everywhere else it runs between gridlines (at $\Delta K = 8$ it is about $6 \times 10^{-9}$, at $10$ about $1.2 \times 10^{-8}$, at $100$ about $1.2 \times 10^{-5}$). With the threshold $\Delta K_{th} = 4.0$ the two crossings give $\frac{20^m - 4^m}{6^m - 4^m} = \frac{1 \times 10^{-7}}{2 \times 10^{-9}} = 50$. The left side is $47.0$ at $m = 2.9$, $49.6$ at $m = 2.95$ and $50.1$ at $m = 2.96$, so $m = 2.96$ (more precisely $2.959$). Then $C = 2 \times 10^{-9}/(6^{2.959} - 4^{2.959}) = 2 \times 10^{-9}/(200.4 - 60.3) = 1.43 \times 10^{-11}$ m/cycle (MPa m$^{1/2}$)$^{-m}$. Treating the two points as Paris-law points instead ($C\,\Delta K^m$ through both) gives $m = 3.25$ and $C = 5.9 \times 10^{-12}$, which is wrong because at $\Delta K = 6$ the threshold term still removes almost a third of the rate.

Step 2: The El Haddad length.
The smooth-specimen fatigue limit and the long-crack threshold are made consistent by $\Delta K_{th} = 0.65\,\Delta\sigma_w\sqrt{\pi a_0}$, so $a_0 = \frac{1}{\pi}\left(\frac{4.0}{0.65 \times 500}\right)^2 = \frac{1}{\pi}(0.012308)^2 = 4.82 \times 10^{-5}$ m $= 48.2$ $\mu$m.

Step 3: The pore is below the long-crack threshold but above its own.
At the pore, $\Delta K = 0.65 \times 450 \times \sqrt{\pi \times 50 \times 10^{-6}} = 292.5 \times 0.012533 = 3.67$ MPa m$^{1/2}$, which is below $4.0$. With the long-crack threshold the law gives a negative rate and the crack would never start, contradicting the fractography. The threshold of a $50$ $\mu$m crack is $\Delta K_{th}(50\ \mu\text{m}) = 4.0\sqrt{50/98.2} = 2.85$ MPa m$^{1/2}$, so the crack grows from the first cycle. (Equivalently, the Kitagawa diagram of this material puts the fatigue limit of a part with a $50$ $\mu$m surface pore at $500\sqrt{48.2/98.2} = 350$ MPa, below the applied $450$ MPa.)

Step 4: The life integral.
$N = \int_{a_i}^{a_f}\frac{da}{C\left[(0.65\,\Delta\sigma\sqrt{\pi a})^m - \left(\Delta K_{th}\sqrt{a/(a+a_0)}\right)^m\right]}$ with $a_i = 50 \times 10^{-6}$ m, $a_f = 0.5 \times 10^{-3}$ m, $m = 2.959$, $C = 1.43 \times 10^{-11}$. The integrand falls by almost an order of magnitude over the range and has no closed form because of the $a/(a + a_0)$ term, so it is integrated numerically. Writing $a = e^u$ and integrating $g(u) = a\,/(da/dN)$ in $u = \ln a$ spreads the weight evenly; with Simpson's rule on $8$ intervals ($h = \ln 10/8 = 0.28782$) the nodes are $a = 50.0, 66.7, 88.9, 118.6, 158.1, 210.8, 281.2, 375.0, 500$ $\mu$m and $g = 143\,402, 105\,097, 80\,312, 63\,419, 51\,383, 42\,466, 35\,630, 30\,229, 25\,855$ cycles, which gives $N = \frac{h}{3}\left[g_0 + g_8 + 4(g_1 + g_3 + g_5 + g_7) + 2(g_2 + g_4 + g_6)\right] = 140\,910$ cycles. Adaptive quadrature of the same integrand gives $140\,891$ cycles; Simpson with $2000$ intervals agrees to the last digit.

Step 5: Result.
$N = 1.41 \times 10^5$, so to two significant figures $1.4 \times 10^5$ cycles.

Taking the curve through the near misses instead of the true crossings gives other answers: $(8, 5 \times 10^{-9})$ with $(20, 10^{-7})$ gives $1.7 \times 10^5$, $(10, 10^{-8})$ with $(100, 10^{-5})$ gives $1.7 \times 10^5$, $(5, 10^{-9})$ with $(20, 10^{-7})$ gives $1.1 \times 10^5$, $(10, 10^{-8})$ with $(20, 10^{-7})$ gives $2.0 \times 10^5$; the Paris-law reading of the two true crossings also gives $2.0 \times 10^5$. Dropping the threshold from the integral gives $1.0 \times 10^5$ cycles; keeping the long-crack threshold predicts no growth at all, and starting the integral at the size where $\Delta K$ first reaches $4.0$ ($60$ $\mu$m) gives $7.0 \times 10^5$ cycles; computing $a_0$ from the stress amplitude instead of the range gives $1.1 \times 10^5$ cycles. None of these is the answer.

Answer: $1.4 \times 10^5$ cycles.

## Rubric

- c1 (4 pts, final answer): Gives $1.4 \times 10^5$ cycles (140 000; any value that rounds to $1.4 \times 10^5$ at two significant figures).
- c2 (2 pts): Identifies the crossings $(6, 2 \times 10^{-9})$ and $(20, 1 \times 10^{-7})$ as the two the curve passes through and solves the Klesnil and Lukas form with the threshold for both constants: $m = 2.96$, $C = 1.4 \times 10^{-11}$ m/cycle (MPa m$^{1/2}$)$^{-m}$ (not the Paris-law values $m = 3.25$, $C = 5.9 \times 10^{-12}$, and not a near miss such as $(10, 10^{-8})$ or $(8, 5 \times 10^{-9})$).
- c3 (1 pts): Computes the El Haddad length from the fatigue limit and the long-crack threshold with the same $0.65\sqrt{\pi a}$ relation: $a_0 = 48$ $\mu$m.
- c4 (2 pts): Shows that $\Delta K$ at the pore ($3.67$ MPa m$^{1/2}$) is below the long-crack threshold but above the size-corrected threshold ($2.85$ MPa m$^{1/2}$), so the crack grows from the first cycle and the size-dependent threshold must be used inside the integral.
- c5 (1 pts): Integrates $da/(da/dN)$ from $50$ $\mu$m to $0.5$ mm numerically with a scheme that resolves the steep start (substitution $u = \ln a$ or equivalent refinement), reaching $1.40$ to $1.42 \times 10^5$ before rounding.

Common wrong answers: 1.7 \times 10^5 cycles, 2.0 \times 10^5 cycles, 1.1 \times 10^5 cycles, 1.0 \times 10^5 cycles, the crack does not grow (infinite life)

## References box

Growth law with threshold: M. Klesnil and P. Lukas, Influence of strength and stress history on growth and stabilisation of fatigue cracks, Engineering Fracture Mechanics 4 (1972) 77-92. Short-crack threshold and the length $a_0$: M. H. El Haddad, T. H. Topper and K. N. Smith, Prediction of non propagating cracks, Engineering Fracture Mechanics 11 (1979) 573-584; H. Kitagawa and S. Takahashi, Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proceedings of the Second International Conference on Mechanical Behavior of Materials, ASM, 1976, 627-631. Stress intensity of a crack at a small surface defect in terms of $\sqrt{\mathrm{area}}$: Y. Murakami, Metal Fatigue: Effects of Small Defects and Nonmetallic Inclusions, Elsevier, 2002, chapter 2. The uploaded file verification_notes.txt states the two gridline crossings the fitted curve was drawn through and the distance of the curve from the nearest gridline at every other labelled abscissa, solves the two constants from the crossings, gives the two independent integrations of the life (adaptive quadrature and Simpson's rule in $\ln a$ with the nodes printed), the values of $a_0$ and of the thresholds at the pore, the life obtained from each near-miss reading and from each wrong route, and the program with its output.

## Verify field

Section 3 of verification_notes.txt gives the two independent integrations of the life (adaptive quadrature and Simpson's rule in ln a with the nodes printed); section 1 states the two gridline crossings the fitted curve was drawn through, the distance of the curve from the nearest gridline at every other labelled abscissa, and solves the two constants; section 2 gives the El Haddad length and the thresholds at the pore; section 4 gives the life from each misreading of the figure and from each wrong route; section 6 embeds the program verify_key.py with its full output.

## Screen

Final wording (both crossings below 30): Opus 2/3 (two runs found (6, 2e-9) and (20, 1e-7) and gave 1.4e5; one took the near miss (10, 1e-8) with (20, 1e-7) and gave 2.0e5), Sonnet see note.md. Earlier wordings on the same figure: no hint Opus 0/3 and Sonnet 0/1; one crossing below 10 Opus 3/3. Earlier figures with a straight Paris asymptote or dense minor gridlines: Opus 3/3 whenever the abscissae were named, 0/3 when not, with the misses inside human reading tolerance; see the task05 v5 row of note.md.