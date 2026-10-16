# task09 v4: Kitagawa diagram, internal pore, standard log axes (Engineering replacement for SUM-MVBG0GO3)

Domain: Engineering. Subdomain: Fatigue and fracture of titanium alloys. Task type: graph extraction with computation.

## Question

The figure shows the fatigue limit of a metal injection moulded Ti-6Al-7Nb alloy, measured at $R = -1$ as the stress amplitude that specimens survive for $10^7$ cycles, plotted against $\sqrt{\mathrm{area}}$ of an artificial defect, a small hole drilled into the specimen surface. All specimens come from one powder lot with $0.20$ wt% oxygen and a Vickers hardness of $320$ HV. Both axes are logarithmic.

A component is made from a second powder lot with $0.38$ wt% oxygen and a hardness of $372$ HV. Sectioning of a sister part found that its largest pore, with $\sqrt{\mathrm{area}} = 600\ \mu\mathrm{m}$, lies deep inside the material, far from every surface. Use Murakami's $\sqrt{\mathrm{area}}$ model, and take the long-crack threshold stress intensity range at $R = -1$ to be the same for both lots. Estimate the fatigue limit of the component at $R = -1$, as a stress amplitude in MPa, to two significant figures.

## Answer

200 MPa (two significant figures)

Also accepted: 200 MPa, $2.0 \times 10^{2}$ MPa

## Image necessity

The long-crack threshold of the alloy and the position of the knee between the small-defect law and the long-crack regime exist only in the plotted data; the text gives hardnesses and the pore size but not the threshold, so the fatigue limit cannot be computed without reading the steep branch of the figure.

## Solution

Step 1: Read the figure.
The eight points lie at $\sqrt{\mathrm{area}} \approx 25, 50, 90, 170, 480, 650, 850, 1100\ \mu\mathrm{m}$ with fatigue limits of about $368, 328, 297, 267, 172, 148, 129, 114$ MPa; the axes are logarithmic with unlabelled minor gridlines at $2, 3, \dots, 9$ times each decade, so a value such as $148$ MPa sits at $\log_{10}(1.48)/\log_{10}(2) = 0.57$ of the way from the $100$ line to the $200$ line, not at $0.48$. The first four points fall on a line of slope $-1/6$ and the last four on a line of slope $-1/2$; the two lines cross near $215\ \mu\mathrm{m}$.

Step 2: Identify the two branches.
The shallow branch is the small-defect law of Murakami's model for surface defects, $\sigma_w = 1.43\,(HV + 120)\,(\sqrt{\mathrm{area}})^{-1/6}$ with $\sigma_w$ in MPa and $\sqrt{\mathrm{area}}$ in $\mu\mathrm{m}$: with $HV = 320$ it gives $629.2 \times 25^{-1/6} = 368.0$ MPa at $25\ \mu\mathrm{m}$ and $267.3$ MPa at $170\ \mu\mathrm{m}$, which is what the figure shows. The steep branch is the long-crack threshold. In the model the stress intensity range of a surface defect is $\Delta K = 0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ (with $\sigma$ the stress range at $R = -1$ counted as the amplitude, in the usual convention of the model), so the point $(650\ \mu\mathrm{m}, 148\ \mathrm{MPa})$ gives
$$\Delta K_{th} = 0.65 \times 148 \times \sqrt{\pi \times 650 \times 10^{-6}} = 0.65 \times 148 \times 0.04519 = 4.35\ \mathrm{MPa}\sqrt{\mathrm{m}},$$
and the points $(480, 172)$, $(850, 129)$ and $(1100, 114)$ give $4.34$, $4.34$ and $4.36$, the same value within the reading, as they must on a line of slope $-1/2$; the figure was drawn with $4.34\ \mathrm{MPa}\sqrt{\mathrm{m}}$. Beyond the knee the fatigue limit of the specimens is $\Delta K_{th} / (0.65\sqrt{\pi\sqrt{\mathrm{area}}})$ and no longer depends on the hardness.

Step 3: Which branch applies to the component.
The pore is internal, so the stress intensity range is $\Delta K = 0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ and the small-defect constant is $1.56$ instead of $1.43$. For the $372$ HV lot the small-defect branch at $600\ \mu\mathrm{m}$ would give $1.56 \times 492 \times 600^{-1/6} = 767.5 / 2.904 = 264$ MPa. The long-crack branch, with the threshold of Step 2 unchanged between the lots, gives
$$\sigma_w = \frac{\Delta K_{th}}{0.50\sqrt{\pi \times 600 \times 10^{-6}}} = \frac{4.34}{0.50 \times 0.04342} = 200\ \mathrm{MPa}.$$
The fatigue limit is the smaller of the two, so the pore lies in the long-crack regime of the component lot as well (its knee for internal defects is near $265\ \mu\mathrm{m}$), and the higher hardness of the second lot does not raise the limit.

Step 4: Assemble.
Equivalently, from the specimen value at $650\ \mu\mathrm{m}$: $\sigma_w = 148 \times (0.65/0.50) \times \sqrt{650/600} = 148 \times 1.3 \times 1.0408 = 200$ MPa, and the other three points of the steep branch give $200$ to $201$ MPa. To two significant figures the fatigue limit of the component is $200$ MPa. A reading of the steep branch that is $3$ percent high, which is what linear interpolation between the $100$ and $200$ MPa lines produces, gives $206$ MPa and rounds to $210$.

Step 5: Conclusion.
The component with the $600\ \mu\mathrm{m}$ internal pore has a fatigue limit of about $200$ MPa at $R = -1$. Keeping the surface factor $0.65$ gives $154$ MPa, scaling the long-crack branch with the hardness ratio $492/440$ gives $224$ MPa, and the small-defect law with the internal constant gives $264$ MPa; each of these misses one of the three decisions, the regime, the hardness independence of the threshold, and the internal-defect factor.

Answer: $200$ MPa.

## Rubric

- c1 (5 pts, final answer): Gives $200$ MPa (two significant figures).
- c2 (2 pts): Recognises that the steep branch of the figure is the long-crack threshold and obtains $\Delta K_{th} \approx 4.3$ to $4.4\ \mathrm{MPa}\sqrt{\mathrm{m}}$ from it (for instance from the point $650\ \mu\mathrm{m}$, $148$ MPa with the factor $0.65$).
- c3 (2 pts): Uses the internal-defect factor $0.50$ in place of the surface factor $0.65$ (the fatigue limit of the internal pore is $1.3$ times the surface value at the same $\sqrt{\mathrm{area}}$).
- c4 (1 pts): States that the $600\ \mu\mathrm{m}$ pore lies in the long-crack regime, so the hardness of the second lot does not change the result (the small-defect value $264$ MPa is not the limit).

Common wrong answers: 210, 150, 220, 260, 240, 170

## References box

The $\sqrt{\mathrm{area}}$ model, with the small-defect law $\sigma_w = C\,(HV + 120)\,(\sqrt{\mathrm{area}})^{-1/6}$ ($C = 1.43$ for surface and $1.56$ for internal defects), the stress intensity factors $\Delta K = 0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for surface and $0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for internal defects, and the transition to the long-crack threshold for large defects: Y. Murakami and M. Endo, Quantitative evaluation of fatigue strength of metals containing various small defects or cracks, Engineering Fracture Mechanics 17 (1983), 1-15, and Y. Murakami and M. Endo, Effects of defects, inclusions and inhomogeneities on fatigue strength, International Journal of Fatigue 16 (1994), 163-182. The diagram of fatigue limit against defect size with its two regimes: H. Kitagawa and S. Takahashi, Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proceedings of the Second International Conference on Mechanical Behavior of Materials, ASM (1976), 627-631; M. H. El Haddad, T. H. Topper and K. N. Smith, Prediction of non propagating cracks, Engineering Fracture Mechanics 11 (1979), 573-584. Fatigue of metal injection moulded titanium alloys with interstitial oxygen as the hardness lever: a background setting, no data from the literature are used. The uploaded file verification_notes.txt states the model the figure was generated from, derives the key by two routes (closed form from each plotted point of the long-crack branch, and a least-squares fit of that branch through the regenerated points), checks the regime for the component lot, evaluates the wrong routes, and embeds the program with its output.

## Verify field

Section 1 of verification_notes.txt states the model the figure was generated from (small-defect law with 320 HV, long-crack branch fixed so that the key is 200.0 MPa) and lists the eight plotted values; section 2 derives the key by two routes, the closed form v x 0.65/0.50 x sqrt(s/600) = 200 MPa from every point of the steep branch and a least-squares fit of that branch through the regenerated points followed by the regime check for the 372 HV lot (small-defect value 264 MPa against long-crack value 200 MPa), with the reading sensitivity; section 3 evaluates the wrong routes; section 4 embeds the program verify_key.py with its output.

## Screen

Figure plus stem only, one Read of the figure, no code. Opus 5.5 high: 3/3 correct, 200 MPa, in 62 s, 115 s and 69 s (41k to 45k tokens); all three read the steep-branch points to within one percent on the standard logarithmic axes (173, 129, 113 MPa against 172, 129, 114), fitted both branches and applied the internal factor with the regime check. Sonnet: 240 MPa, wrong (used the small-defect law at 600 um). The log-axis reading lever did not bite. Not in band.