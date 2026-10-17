# task09 v8: two S-N curves (R = -1 and R = 0.1), block loading with Haibach extension (Engineering replacement candidate for SUM-MVBG0GO3)

Domain: Engineering. Subdomain: Fatigue and fracture of titanium alloys. Task type: graph extraction with computation.

## Question

The figure shows the S-N curves of a metal injection moulded Ti-6Al-7Nb alloy for two stress ratios, fully reversed loading ($R = -1$, solid line, filled circles) and $R = 0.1$ (dashed line, open squares): stress amplitude on a linear axis against cycles to failure on a logarithmic axis. Each line is a Basquin fit $\sigma_a = A\,N^{-1/k}$ to its failures, with its own $A$ and $k$, and each passes exactly through two of the gridline crossings of the plot, between $10^4$ and $10^7$ cycles. At the knee at $N_e = 10^7$ cycles each fit meets its fatigue limit, and the specimens beyond the knee ran out.

A component of this material is loaded in repeated blocks. Each block consists of $5\,000$ cycles at a stress amplitude of $260$ MPa with $R = -1$, then $10\,000$ cycles at $250$ MPa with $R = 0.1$, then $5\,000\,000$ cycles at $180$ MPa with $R = -1$. Use the linear damage rule with failure at a damage sum of one, and below a fatigue limit extend that curve by Haibach's rule, a second Basquin line through its knee with the exponent $2k - 1$ in place of $k$. How many complete blocks does the component survive? Give an integer.

## Answer

7 (complete blocks)

Also accepted: 7 blocks, seven

## Image necessity

The Basquin parameters of both curves and the two fatigue limits exist only in the plotted lines; they have to be recovered from the gridline crossings each line passes through, and the text states neither exponent nor limit.

## Solution

Step 1: Find the crossings of each curve.
The vertical gridlines are at $1, 2, 5$ times each decade of cycles and the horizontal gridlines every $10$ MPa. The solid $R = -1$ line meets a vertical gridline exactly at $(5 \times 10^4, 310\ \text{MPa})$ and at $(2 \times 10^6, 230\ \text{MPa})$; at $290$ MPa it is at about $1.14 \times 10^5$, past the $10^5$ line, and at $240$ MPa at about $1.18 \times 10^6$, past the $10^6$ line. The dashed $R = 0.1$ line meets a crossing exactly at $(2 \times 10^5, 240\ \text{MPa})$ and at $(5 \times 10^6, 190\ \text{MPa})$; at $250$ MPa it is at about $1.14 \times 10^5$, past the $10^5$ line, and at $200$ MPa at about $2.3 \times 10^6$, past the $2 \times 10^6$ line.

Step 2: The Basquin parameters.
$R = -1$: $k_1 = \ln(2 \times 10^6 / 5 \times 10^4) / \ln(310/230) = 3.689 / 0.2985 = 12.36$, $A_1 = 310 \times (5 \times 10^4)^{1/12.36} = 744$ MPa, fatigue limit $\sigma_{e1} = 744 \times 10^{-7/12.36} = 201.9$ MPa. $R = 0.1$: $k_2 = \ln(5 \times 10^6 / 2 \times 10^5) / \ln(240/190) = 3.219 / 0.2336 = 13.78$, $A_2 = 240 \times (2 \times 10^5)^{1/13.78} = 582$ MPa, fatigue limit $\sigma_{e2} = 582 \times 10^{-7/13.78} = 180.7$ MPa.

Step 3: Life at the three amplitudes of the block.
$260$ MPa at $R = -1$ is above $\sigma_{e1}$: $N = (744/260)^{12.36} = 4.40 \times 10^5$ cycles, damage $5\,000 / 4.40 \times 10^5 = 0.0114$. $250$ MPa at $R = 0.1$ is above $\sigma_{e2}$: $N = (582/250)^{13.78} = 1.14 \times 10^5$ cycles, damage $10\,000 / 1.14 \times 10^5 = 0.0877$. $180$ MPa at $R = -1$ is below $\sigma_{e1}$: Haibach's extension gives $N = 10^7 (201.9/180)^{23.72} = 1.52 \times 10^8$ cycles, damage $5 \times 10^6 / 1.52 \times 10^8 = 0.0328$.

Step 4: Damage per block and the number of blocks.
$D = 0.0114 + 0.0877 + 0.0328 = 0.1319$ per block, so failure after $1/0.1319 = 7.58$ blocks. The component survives $7$ complete blocks.

Step 5: What the other readings and rules give.
Reading the $R = -1$ line through the major-line crossings $(10^5, 290)$ and $(10^6, 240)$ gives $k_1 = 12.17$ and $6.6$ blocks, that is $6$; $(10^5, 290)$ with the correct $(2 \times 10^6, 230)$ gives $8.0$ blocks, $8$, and $(10^6, 240)$ with the correct $(5 \times 10^4, 310)$ gives $6.0$ blocks, $6$. Reading the $R = 0.1$ line through $(10^5, 250)$ with $(5 \times 10^6, 190)$ gives $6.9$ blocks, $6$; through $(2 \times 10^5, 240)$ with $(10^6, 200)$ gives $8.6$ blocks, $8$. Ignoring the cycles below the fatigue limit gives $10.1$ blocks, $10$; extending the $R = -1$ line below the limit with the same exponent gives $4.6$ blocks, $4$. The integer $7$ is unchanged by rounding either exponent by $0.05$ or either fatigue limit to the nearest gridline value.

Answer: $7$ complete blocks.

## Rubric

- c1 (5 pts, final answer): Gives $7$ (complete blocks).
- c2 (2 pts): Identifies the crossings $(5 \times 10^4, 310)$ and $(2 \times 10^6, 230)$ for $R = -1$ and $(2 \times 10^5, 240)$ and $(5 \times 10^6, 190)$ for $R = 0.1$, with $k_1 \approx 12.4$ and $k_2 \approx 13.8$.
- c3 (2 pts): Obtains the $R = -1$ fatigue limit of about $202$ MPa at the knee and the Haibach life at $180$ MPa of about $1.5 \times 10^8$ cycles (within $10$ percent).
- c4 (1 pts): Obtains a damage of about $0.13$ per block, with about $0.09$ from the $R = 0.1$ cycles, $0.03$ from the $180$ MPa cycles and $0.01$ from the $260$ MPa cycles.

Common wrong answers: 6, 8, 10, 4, 9, 5

## References box

The power law for the finite-life region: O. H. Basquin, The exponential law of endurance tests, Proceedings of the American Society for Testing Materials 10 (1910), 625-630. The linear damage rule: A. Palmgren, Die Lebensdauer von Kugellagern, Zeitschrift des Vereines Deutscher Ingenieure 68 (1924), 339-341, and M. A. Miner, Cumulative damage in fatigue, Journal of Applied Mechanics 12 (1945), A159-A164. The extension of the S-N curve below the fatigue limit with the exponent $2k - 1$: E. Haibach, Modifizierte lineare Schadensakkumulations-Hypothese zur Beruecksichtigung des Dauerfestigkeitsabfalls mit fortschreitender Schaedigung, Technische Mitteilung TM 50/70, Laboratorium fuer Betriebsfestigkeit, Darmstadt (1970); see also E. Haibach, Betriebsfestigkeit, third edition, Springer (2006), chapter 3. The setting (metal injection moulded titanium alloy, two stress ratios) is background; the figure is generated from the two fits stated in the solution and no literature data are used. The uploaded file verification_notes.txt states both fits, lists where each drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, derives the block count by two routes, and evaluates the wrong crossings on either curve, the wrong damage rules and the rounding robustness of the integer, with the program embedded.

## Verify field

Section 1 of verification_notes.txt states the two fits the figure was generated from (R = -1: k = 12.36, A = 744 MPa, limit 201.9 MPa; R = 0.1: k = 13.78, A = 582 MPa, limit 180.7 MPa) and lists where each drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, showing the only exact crossings are (5e4, 310), (2e6, 230) and (2e5, 240), (5e6, 190); section 2 derives the block count by two routes (closed form, and a numerical reconstruction of both curves with the crossings and lives found by bisection), both 7.58 blocks; section 3 evaluates the wrong crossings on either curve (6 or 8 blocks), the wrong damage rules (10 and 4) and the rounding robustness of the integer; section 4 embeds the program verify_key.py with its output.

## Screen

Figure plus stem only. Opus 5.5 high: 3/3 correct (7), 2.5 to 3.5 min. Two runs anchored the curves on their frame ends, (1e4, 350) and (1e7, 200) for R = -1 and (1e4, 300), (1e7, 180) for R = 0.1, which are within one percent of the true values; one run found the exact crossings of the solid line and the frame ends of the dashed one. Sonnet: 1/1 correct (7) by the same frame-end anchors, 8 min. Lesson: a curve that starts on the frame and a plateau within 2 MPa of a gridline hand the model free anchors; v9 moves both away. Out of band.