# task08: fatigue crack growth life with a constant opening level read from two load ratios

Engineering (materials), subdomain: Fatigue and fracture of titanium alloys. This folder was first used for the mathematics task on the fractional chromatic number (Summit SUM-MVBCQZWW, returned too easy); that package and its revision are archived in work/v1 and work/v2-math. Two earlier engineering versions (closure as a fixed fraction of K_max, 0.30 and 0.55) are archived in work/eng-v1 and work/eng-v2; both were solved by every local run.

## Question

The figure shows fatigue crack growth data for long cracks in a metal injection moulded Ti-6Al-7Nb alloy: the crack growth rate $da/dN$ against the stress intensity factor range $\Delta K$ on logarithmic axes, measured at the load ratios $R = 0.1$ and $R = 0.7$. The dashed line is the Paris-law fit to the straight part of the $R = 0.7$ data; the thin solid line through the $R = 0.1$ data only guides the eye. The difference between the two data sets is caused by crack closure. Assume that the crack-opening stress intensity factor $K_{op}$ has the same constant value at every load ratio at which closure occurs, independent of $K_{max}$, that closure is absent when $K_{min} \ge K_{op}$, and that the growth rate depends only on the effective range $\Delta K_{eff} = K_{max} - \max(K_{op}, K_{min})$.

A wide plate of the same material carries a constant-amplitude cyclic stress with $\sigma_{max} = 400$ MPa at $R = 0.4$. A surface pore is treated as an edge crack of initial length $a_0 = 0.20$ mm, with the geometry factor $Y = 1.12$ taken as constant, so that $K = Y \sigma \sqrt{\pi a}$. The plate fails when $K_{max}$ reaches the fracture toughness $K_{IC} = 55$ MPa$\sqrt{\mathrm{m}}$. Take the dashed Paris fit as the relation between $da/dN$ and $\Delta K_{eff}$ for the whole of the crack growth, and ignore the deviation of the data near the threshold.

Find the number of cycles from $a_0$ to failure. Give the answer to two significant figures.

## Answer

$1.2 \times 10^{6}$ cycles

## Solution

Step 1: Read the closure-free growth law from the figure.
The dashed Paris fit of the $R = 0.7$ data passes through the grid intersections $da/dN = 10^{-9}$ m/cycle at $\Delta K = 10$ MPa$\sqrt{\mathrm{m}}$ and $da/dN = 10^{-6}$ m/cycle at $\Delta K = 100$ MPa$\sqrt{\mathrm{m}}$, so $m = 3$ and $C = 10^{-9}/10^{3} = 1.0 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^{3}$. At $R = 0.7$, $K_{min} = 0.7\,K_{max}$ is far above any opening level that could explain the $R = 0.1$ data, so this fit is the closure-free law $da/dN = C\,\Delta K_{eff}^{3}$.

Step 2: Infer the opening level from the two data sets.
The $R = 0.1$ data are not a parallel line: they lie to the right of the $R = 0.7$ data by a gap that shrinks with $\Delta K$ and closes above $\Delta K \approx 54$ MPa$\sqrt{\mathrm{m}}$, which is the signature of a constant $K_{op}$. With closure, $\Delta K_{eff} = K_{max} - K_{op}$ and at $R = 0.1$, $K_{max} = \Delta K/0.9$, so points of equal growth rate satisfy $\Delta K_{0.1} = 0.9\,(\Delta K_{eff} + K_{op})$. Pairs of equal rate read from the plot are $\Delta K_{eff} = 4$ against $\Delta K_{0.1} = 9$, $14$ against $18$, $24$ against $27$, $34$ against $36$ and $44$ against $45$, each giving $K_{op} = \Delta K_{0.1}/0.9 - \Delta K_{eff} = 6$ MPa$\sqrt{\mathrm{m}}$. The merging point confirms it: closure vanishes at $R = 0.1$ when $K_{min} = \Delta K/9$ reaches $K_{op}$, that is at $\Delta K = 54$ MPa$\sqrt{\mathrm{m}}$.

Step 3: The decisive step: at $R = 0.4$ closure is present at first and disappears during the growth.
With $K_{max} = Y \sigma_{max} \sqrt{\pi a} = 794.1\sqrt{a}$ (MPa$\sqrt{\mathrm{m}}$, $a$ in m), the initial crack has $K_{max} = 11.23$ and $K_{min} = 0.4\,K_{max} = 4.49$ MPa$\sqrt{\mathrm{m}}$, below $K_{op} = 6$: the crack closes during part of every cycle and $\Delta K_{eff} = K_{max} - 6 = 5.23$ MPa$\sqrt{\mathrm{m}}$ at $a_0$, above the threshold of the closure-free data. $K_{min}$ grows with the crack and reaches $K_{op}$ when $K_{max} = K_{op}/R = 15$ MPa$\sqrt{\mathrm{m}}$, at $a_t = \dfrac{1}{\pi}\left(\dfrac{15}{1.12 \times 400}\right)^{2} = 0.357$ mm. Beyond $a_t$ the crack is closure-free and $\Delta K_{eff} = \Delta K = Y \Delta\sigma \sqrt{\pi a}$ with $\Delta\sigma = 240$ MPa. The life is the sum of the two parts; ignoring the closure altogether, or keeping $\Delta K_{eff} = K_{max} - K_{op}$ after $a_t$ (where it would exceed $\Delta K$), both give wrong lives.

Step 4: Critical crack length.
Failure occurs when $K_{max} = K_{IC}$: $a_c = \dfrac{1}{\pi}\left(\dfrac{55}{1.12 \times 400}\right)^{2} = 4.798$ mm (with $\Delta\sigma$ in place of $\sigma_{max}$ one would get $13.3$ mm, which is wrong). The closure-free part runs from $\Delta K = 9.00$ to $\Delta K = 33.0$ MPa$\sqrt{\mathrm{m}}$, inside the straight part of the data.

Step 5: Integrate the two parts.
Part 1, $a_0 \le a \le a_t$, with $w = K_{max} - K_{op} = 794.1\sqrt{a} - 6$: substituting $u = \sqrt{a}$, $da = 2u\,du$, and $w = 794.1\,u - 6$,
$$N_1 = \int_{a_0}^{a_t} \frac{da}{C\,w^{3}} = \frac{2}{C\,B^{2}} \int_{w_0}^{w_t} \frac{w + K_{op}}{w^{3}}\,dw = \frac{2}{C\,B^{2}} \left[ -\frac{1}{w} - \frac{K_{op}}{2 w^{2}} \right]_{w_0}^{w_t},$$
with $B = 794.1$, $w_0 = 11.23 - 6 = 5.23$ and $w_t = 15 - 6 = 9$ MPa$\sqrt{\mathrm{m}}$. The bracket is $(-0.14815) - (-0.30091) = 0.15276$ (MPa$\sqrt{\mathrm{m}}$)$^{-1}$ and $2/(C B^{2}) = 3.1719e+06$, so $N_1 = 4.845e+05$ cycles.
Part 2, $a_t \le a \le a_c$, closure-free Paris law with $Y \Delta\sigma \sqrt{\pi} = 476.4$:
$$N_2 = \frac{2}{C\,(Y \Delta\sigma \sqrt{\pi})^{3}}\left(a_t^{-1/2} - a_c^{-1/2}\right) = 18493 \times (52.94 - 14.44) = 7.12e+05 \text{ cycles}.$$
Total: $N = N_1 + N_2 = 1.197e+06 \approx 1.2 \times 10^{6}$ cycles.

Step 6: Conclusion.
The plate survives $1.2 \times 10^{6}$ cycles. Ignoring closure (the dashed fit with $\Delta K$ throughout) gives $1e+06$; keeping $\Delta K_{eff} = K_{max} - K_{op}$ up to $a_c$ gives $8.9 \times 10^{5}$; treating $K_{op}$ as the fixed fraction of $K_{max}$ that holds at $a_0$ gives $2.2 \times 10^{6}$; computing $a_c$ from $\Delta\sigma$ gives $1.3 \times 10^{6}$.

Answer: $1.2 \times 10^{6}$ cycles.

## Rubric

- c1 (5 pts, final answer): Gives $1.2 \times 10^{6}$ cycles (two significant figures; any equivalent numerical form).
- c2 (2 pts): Reads the closure-free law as $m = 3$, $C = 1.0 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^3$ from the $R = 0.7$ fit, and infers the constant opening level $K_{op} = 6$ MPa$\sqrt{\mathrm{m}}$ from the converging $R = 0.1$ data (equal-rate pairs or the merging point near $\Delta K = 54$).
- c3 (2 pts): Recognises that at $R = 0.4$ closure is present from $a_0$ and disappears when $K_{min}$ reaches $K_{op}$, at $K_{max} = 15$ MPa$\sqrt{\mathrm{m}}$ ($a_t = 0.357$ mm), and integrates the two parts separately.
- c4 (1 pts): Obtains the critical crack length $a_c = 4.80$ mm from $K_{max} = Y \sigma_{max} \sqrt{\pi a_c} = K_{IC}$ with $\sigma_{max} = 400$ MPa.

Common wrong answers: $1.0 \times 10^{6}$ cycles, $8.9 \times 10^{5}$ cycles, $2.2 \times 10^{6}$ cycles, $8.3 \times 10^{6}$ cycles, $1.3 \times 10^{6}$ cycles

## References box

Crack closure and the effective stress intensity range: W. Elber, The significance of fatigue crack closure, in Damage Tolerance in Aircraft Structures, ASTM STP 486 (1971), 230-242. The power-law relation between growth rate and stress intensity range: P. C. Paris and F. Erdogan, A critical analysis of crack propagation laws, Journal of Basic Engineering 85 (1963), 528-534. The uploaded file verification_notes.txt states the growth law and closure model from which the figure was generated (so the fit and the opening level are exact), lists every plotted point, derives the opening level from the equal-rate pairs and the merging point, finds the transition length at $R = 0.4$, computes the critical crack length and the two-part life by closed forms and by two numerical integrations, and computes the values reached by the wrong routes; the program is embedded with its output.

## Verify field

Section 1 of verification_notes.txt gives the growth law and closure model that generated the figure and the coordinates of every plotted point, so the fit can be checked against the plot (the R = 0.7 fit passes through 1e-9 m/cycle at 10 MPa sqrt m and 1e-6 at 100; the R = 0.1 points at 9, 18, 27, 36, 45 have the same rates as the R = 0.7 points at 4, 14, 24, 34, 44, giving K_op = 6 from each pair). Section 2 derives the transition at K_max = 15 MPa sqrt m (a_t = 0.357 mm) at R = 0.4. Section 3 computes a_c = 4.80 mm and the life 1,196,532 cycles as the sum of two closed forms, checked by composite Simpson integration and by scipy quad. Section 4 lists the wrong routes with their values. Section 5 embeds the program verify_key.py with its output.

## Screen

Constant-K_op version (key 1.2e6, this package; screened before the last rewording of the final stem sentence, see below): Opus 3/3 correct (88 s, 89 s, 78 s; each read C = 1e-12 and m = 3, K_op = 6 from equal-rate pairs such as 14 against 18 and 24 against 27 or from the merging point near 54, the transition at K_max = 15 (a_t = 0.357 mm), the two closed-form stages 4.85e5 + 7.12e5). Sonnet 0/1 (answered 1.0e6: it read "use the Paris fit of the R = 0.7 data as the closure-free growth law for the whole of the crack growth" as an instruction to ignore closure and integrated with delta K throughout). That sentence was then reworded to "take the dashed Paris fit as the relation between da/dN and delta K_eff for the whole of the crack growth", which removes the misreading; no new screen was run after the rewording.

Closure-0.55 version (key 2.47e6, archived in work/eng-v2): Opus 3/3 correct (58 s, 50 s, 39 s), Sonnet 1/1 correct (2 min).

Closure-0.30 version (key 1.04e6, archived in work/eng-v1): Opus 3/3 correct (56 s, 85 s, 82 s), Sonnet 1/1 correct (2 min).

