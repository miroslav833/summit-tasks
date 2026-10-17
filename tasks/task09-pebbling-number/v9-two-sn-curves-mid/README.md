# task09 v9: two S-N curves with mid-interval plateaus, block loading with Haibach extension (Engineering replacement candidate for SUM-MVBG0GO3)

Domain: Engineering. Subdomain: Fatigue and fracture of titanium alloys. Task type: graph extraction with computation.

## Question

The figure shows the S-N curves of a metal injection moulded Ti-6Al-7Nb alloy for two stress ratios, fully reversed loading ($R = -1$, solid line, filled circles) and $R = 0.1$ (dashed line, open squares): stress amplitude on a linear axis against cycles to failure on a logarithmic axis. Each line is a Basquin fit $\sigma_a = A\,N^{-1/k}$ to its failures, with its own $A$ and $k$, and each passes exactly through two of the gridline crossings of the plot, between $10^4$ and $10^7$ cycles. At the knee at $N_e = 10^7$ cycles each fit meets its fatigue limit, and the specimens beyond the knee ran out.

A component of this material is loaded in repeated blocks. Each block consists of $20\,000$ cycles at a stress amplitude of $220$ MPa with $R = -1$, then $10\,000$ cycles at $170$ MPa with $R = 0.1$, then $2\,000\,000$ cycles at $140$ MPa with $R = -1$. Use the linear damage rule with failure at a damage sum of one, and below a fatigue limit extend that curve by Haibach's rule, a second Basquin line through its knee with the exponent $2k - 1$ in place of $k$. How many complete blocks does the component survive? Give an integer.

## Answer

7 (complete blocks)

Also accepted: 7 blocks, seven

## Image necessity

The Basquin parameters of both curves and the two fatigue limits exist only in the plotted lines; they have to be recovered from the gridline crossings each line passes through, and the text states neither exponent nor limit.

## Solution

Step 1: Find the crossings of each curve.
The vertical gridlines are at $1, 2, 5$ times each decade of cycles and the horizontal gridlines every $10$ MPa. The solid $R = -1$ line meets a vertical gridline exactly at $(10^5, 240\ \text{MPa})$ and at $(5 \times 10^5, 210\ \text{MPa})$; at $230$ MPa it is at about $1.67 \times 10^5$, short of the $2 \times 10^5$ line, and at $200$ MPa at about $9.0 \times 10^5$, short of the $10^6$ line. The dashed $R = 0.1$ line meets a crossing exactly at $(2 \times 10^4, 200\ \text{MPa})$ and at $(10^6, 150\ \text{MPa})$; at $180$ MPa it is at about $8.4 \times 10^4$, short of the $10^5$ line, at $170$ MPa at about $1.82 \times 10^5$, and at $160$ MPa at about $4.2 \times 10^5$. The curves are drawn from about $1.3 \times 10^4$ cycles, so their left ends are not on a gridline, and the two plateaus beyond the knee lie between gridlines, at about $164$ and $127$ MPa.

Step 2: The Basquin parameters.
$R = -1$: $k_1 = \ln(5 \times 10^5 / 10^5) / \ln(240/210) = 1.609 / 0.1335 = 12.05$, $A_1 = 240 \times (10^5)^{1/12.05} = 624$ MPa, fatigue limit $\sigma_{e1} = 624 \times 10^{-7/12.05} = 163.8$ MPa. $R = 0.1$: $k_2 = \ln(10^6 / 2 \times 10^4) / \ln(200/150) = 3.912 / 0.2877 = 13.60$, $A_2 = 200 \times (2 \times 10^4)^{1/13.60} = 414$ MPa, fatigue limit $\sigma_{e2} = 414 \times 10^{-7/13.60} = 126.6$ MPa.

Step 3: Life at the three amplitudes of the block.
$220$ MPa at $R = -1$ is above $\sigma_{e1}$: $N = (624/220)^{12.05} = 2.85 \times 10^5$ cycles, damage $20\,000 / 2.85 \times 10^5 = 0.0701$. $170$ MPa at $R = 0.1$ is above $\sigma_{e2}$: $N = (414/170)^{13.60} = 1.82 \times 10^5$ cycles, damage $10\,000 / 1.82 \times 10^5 = 0.0549$. $140$ MPa at $R = -1$ is below $\sigma_{e1}$: Haibach's extension gives $N = 10^7 (163.8/140)^{23.11} = 3.75 \times 10^8$ cycles, damage $2 \times 10^6 / 3.75 \times 10^8 = 0.0053$.

Step 4: Damage per block and the number of blocks.
$D = 0.0701 + 0.0549 + 0.0053 = 0.1303$ per block, so failure after $1/0.1303 = 7.68$ blocks. The component survives $7$ complete blocks.

Step 5: What the other readings and rules give.
Reading the $R = -1$ line through $(10^5, 240)$ with the major-line crossing $(10^6, 200)$ gives $8.0$ blocks, that is $8$; through $(2 \times 10^5, 230)$ with $(5 \times 10^5, 210)$ gives $6.9$ blocks, $6$; through $(2 \times 10^5, 230)$ with $(10^6, 200)$ gives $8.3$ blocks, $8$. Reading the $R = 0.1$ line through $(10^5, 180)$ with $(10^6, 150)$ gives $8.1$ blocks, $8$; through $(2 \times 10^4, 200)$ with $(5 \times 10^5, 160)$ gives $8.1$ blocks, $8$. Ignoring the cycles below the fatigue limit gives $8.0$ blocks, $8$; extending the $R = -1$ line below the limit with the same exponent gives $6.4$ blocks, $6$. The integer $7$ is unchanged by rounding either exponent by $0.05$ or either fatigue limit to a neighbouring gridline value.

Answer: $7$ complete blocks.

## Rubric

- c1 (5 pts, final answer): Gives $7$ (complete blocks).
- c2 (2 pts): Identifies the crossings $(10^5, 240)$ and $(5 \times 10^5, 210)$ for $R = -1$ and $(2 \times 10^4, 200)$ and $(10^6, 150)$ for $R = 0.1$, with $k_1 \approx 12.1$ and $k_2 \approx 13.6$.
- c3 (2 pts): Obtains the $R = -1$ fatigue limit of about $164$ MPa at the knee and the Haibach life at $140$ MPa of about $3.8 \times 10^8$ cycles (within $15$ percent).
- c4 (1 pts): Obtains a damage of about $0.13$ per block, with about $0.07$ from the $220$ MPa cycles, $0.055$ from the $R = 0.1$ cycles and $0.005$ from the $140$ MPa cycles.

Common wrong answers: 8, 6, 9, 5, 10, 4

## References box

The power law for the finite-life region: O. H. Basquin, The exponential law of endurance tests, Proceedings of the American Society for Testing Materials 10 (1910), 625-630. The linear damage rule: A. Palmgren, Die Lebensdauer von Kugellagern, Zeitschrift des Vereines Deutscher Ingenieure 68 (1924), 339-341, and M. A. Miner, Cumulative damage in fatigue, Journal of Applied Mechanics 12 (1945), A159-A164. The extension of the S-N curve below the fatigue limit with the exponent $2k - 1$: E. Haibach, Modifizierte lineare Schadensakkumulations-Hypothese zur Beruecksichtigung des Dauerfestigkeitsabfalls mit fortschreitender Schaedigung, Technische Mitteilung TM 50/70, Laboratorium fuer Betriebsfestigkeit, Darmstadt (1970); see also E. Haibach, Betriebsfestigkeit, third edition, Springer (2006), chapter 3. The setting (metal injection moulded titanium alloy, two stress ratios) is background; the figure is generated from the two fits stated in the solution and no literature data are used. The uploaded file verification_notes.txt states both fits, lists where each drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, derives the block count by two routes, and evaluates the wrong crossings on either curve, the wrong damage rules and the rounding robustness of the integer, with the program embedded.

## Verify field

Section 1 of verification_notes.txt states the two fits the figure was generated from (R = -1: k = 12.05, A = 624 MPa, limit 163.8 MPa; R = 0.1: k = 13.60, A = 414 MPa, limit 126.6 MPa) and lists where each drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, showing the only exact crossings are (1e5, 240), (5e5, 210) and (2e4, 200), (1e6, 150); section 2 derives the block count by two routes (closed form, and a numerical reconstruction of both curves with the crossings and lives found by bisection), both 7.68 blocks; section 3 evaluates the wrong crossings on either curve (8 or 6 blocks), the wrong damage rules (8 and 6) and the rounding robustness of the integer; section 4 embeds the program verify_key.py with its output.

## Screen

Figure plus stem only. Opus 5.5 high: run 1 wrong (8): took the solid line through (2e4, 280) and (1e6, 200) and the dashed line through (1e5, 180) and (1e6, 150), all near misses, 8.70 blocks, 3 min. Run 2 wrong (8): the same four readings, 8.69 blocks, 4.5 min. Run 3 correct (7): the exact crossings (1e5, 240), (5e5, 210), (2e4, 200), (1e6, 150), 7.68 blocks, 4.5 min. Sonnet: correct (7) by a misread solid line through (5e4, 250) and (1e6, 200), 7.79 blocks, 4.7 min. Tally Opus 1/3, Sonnet 1/1, no cut-offs. In band locally; the strongest tally in this folder.