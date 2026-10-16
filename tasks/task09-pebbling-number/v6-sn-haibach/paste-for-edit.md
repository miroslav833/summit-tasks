# Edit sheet: Engineering replacement for SUM-MVBG0GO3 (task09 v6, S-N curve with Haibach extension)

Edit the returned task09 entry field by field, or import the zip as a new task if a returned entry cannot
change domain. Category Engineering (fallback Physics, subdomain "Solid mechanics / fracture mechanics").

## Subdomain
Fatigue and fracture of titanium alloys

## Modality / image reasoning pattern
Multimodal (image). Figure/plot extraction with quantitative computation.

## Image
Upload image.png from this folder.

## Image source
matplotlib (S-N diagram generated from the Basquin fit stated in the solution)

## Why the image is necessary
The Basquin parameters and the fatigue limit at the knee exist only in the plotted curve; they have to be recovered from the two gridline crossings the curve passes through, and the text states neither the exponent nor the fatigue limit.

## Question text
The figure shows the S-N curve of a metal injection moulded Ti-6Al-7Nb alloy at $R = -1$: stress amplitude on a linear axis against cycles to failure on a logarithmic axis. The solid line is a Basquin fit $\sigma_a = A\,N^{-1/k}$ to the failures; it passes exactly through two of the gridline crossings of the plot, both between $10^4$ and $10^7$ cycles. At the knee at $N_e = 10^7$ cycles the fit meets the fatigue limit, and the specimens beyond the knee ran out.

A component of this material is loaded in repeated blocks at $R = -1$. Each block consists of $5\,000$ cycles at a stress amplitude of $320$ MPa followed by $5\,000\,000$ cycles at $180$ MPa. Use the linear damage rule with failure at a damage sum of one, and extend the S-N curve below the fatigue limit by Haibach's rule, a second Basquin line through the knee with the exponent $2k - 1$ in place of $k$. How many complete blocks does the component survive? Give an integer.

## Answer format / precision
Exact match. No precision stated (integer).

## Correct answer
5

## Also accepted (one per line)
5 blocks
five

## Solution
Step 1: Find the two crossings.
The vertical gridlines are at $1, 2, 5$ times each decade of cycles and the horizontal gridlines every $10$ MPa. Following the fitted curve across the horizontal lines, it meets a vertical line exactly at $(5 \times 10^4\ \text{cycles}, 310\ \text{MPa})$ and at $(2 \times 10^6\ \text{cycles}, 230\ \text{MPa})$. Everywhere else it crosses a horizontal line between two vertical lines: at $290$ MPa it is at about $1.14 \times 10^5$, past the $10^5$ line; at $240$ MPa at about $1.18 \times 10^6$, past the $10^6$ line; at $260$ MPa at about $4.4 \times 10^5$, short of the $5 \times 10^5$ line; at $350$ MPa at about $1.1 \times 10^4$.

Step 2: The Basquin parameters.
From the two crossings, $k = \ln(2 \times 10^6 / 5 \times 10^4) / \ln(310/230) = \ln 40 / \ln 1.3478 = 3.689 / 0.2985 = 12.36$, and $A = 310 \times (5 \times 10^4)^{1/12.36} = 310 \times 2.400 = 744$ MPa. The fatigue limit at the knee is $\sigma_e = A\,N_e^{-1/k} = 744 \times 10^{-7/12.36} = 744 \times 0.2714 = 201.9$ MPa.

Step 3: Life at the two amplitudes of the block.
At $320$ MPa, above the fatigue limit, $N = (A/320)^{k} = (2.325)^{12.36} = 3.38 \times 10^4$ cycles. At $180$ MPa, below the fatigue limit, Haibach's extension gives $N = N_e\,(\sigma_e/180)^{2k-1} = 10^7 \times (1.1218)^{23.72} = 10^7 \times 15.25 = 1.52 \times 10^8$ cycles.

Step 4: Damage per block and the number of blocks.
$D = 5\,000 / 3.38 \times 10^4 + 5 \times 10^6 / 1.52 \times 10^8 = 0.148 + 0.033 = 0.181$ per block, so failure after $1/0.181 = 5.53$ blocks. The component survives $5$ complete blocks.

Step 5: What the other readings and rules give.
Taking the crossings at the major lines, $(10^5, 290)$ and $(10^6, 240)$, gives $k = 12.17$, $A = 747$ MPa and $4.63$ blocks, that is $4$; either one of them with the correct other crossing gives $4.9$ or $4.8$ blocks, again $4$. Pairing $(5 \times 10^5, 260)$ with $(2 \times 10^6, 230)$ gives $6.3$ blocks, that is $6$. Ignoring the cycles below the fatigue limit gives $6.75$ blocks, that is $6$; extending the Basquin line below the limit with the same exponent $k$ gives $3.7$ blocks, that is $3$. The integer $5$ is unchanged by rounding $k$ to $12.3$ or $12.4$ or the fatigue limit to $200$ or $202$ MPa.

Answer: $5$ complete blocks.

## Rubric (points 5/2/2/1; c1 is the final-answer criterion)
- c1 (5 pts, final answer): Gives $5$ (complete blocks).
- c2 (2 pts): Identifies the two crossings as $(5 \times 10^4, 310\ \text{MPa})$ and $(2 \times 10^6, 230\ \text{MPa})$ and obtains $k \approx 12.4$ (equivalently a Basquin exponent of about $-0.081$).
- c3 (2 pts): Obtains the fatigue limit at the knee, about $202$ MPa, and the Haibach life at $180$ MPa of about $1.5 \times 10^8$ cycles (within $10$ percent).
- c4 (1 pts): Obtains a damage of about $0.18$ per block, with about $0.15$ from the $320$ MPa cycles and $0.03$ from the $180$ MPa cycles.

## Common wrong answers (one per line)
4
6
3
7
9

## References file
Upload reference.txt from this folder as verification_notes.txt.

## References text
The power law for the finite-life region: O. H. Basquin, The exponential law of endurance tests, Proceedings of the American Society for Testing Materials 10 (1910), 625-630. The linear damage rule: A. Palmgren, Die Lebensdauer von Kugellagern, Zeitschrift des Vereines Deutscher Ingenieure 68 (1924), 339-341, and M. A. Miner, Cumulative damage in fatigue, Journal of Applied Mechanics 12 (1945), A159-A164. The extension of the S-N curve below the fatigue limit with the exponent $2k - 1$: E. Haibach, Modifizierte lineare Schadensakkumulations-Hypothese zur Beruecksichtigung des Dauerfestigkeitsabfalls mit fortschreitender Schaedigung, Technische Mitteilung TM 50/70, Laboratorium fuer Betriebsfestigkeit, Darmstadt (1970); see also E. Haibach, Betriebsfestigkeit, third edition, Springer (2006), chapter 3. The setting (metal injection moulded titanium alloy) is background; the figure is generated from the fit stated in the solution and no literature data are used. The uploaded file verification_notes.txt states the fit, lists where the drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, derives the block count by two routes, and evaluates the wrong crossings, the wrong damage rules and the rounding robustness of the integer, with the program embedded.

## Verify box
Section 1 of verification_notes.txt states the fit the figure was generated from (k = 12.36, A = 744 MPa, knee at 1e7 cycles, fatigue limit 201.9 MPa) and lists where the drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, showing that (5e4, 310) and (2e6, 230) are the only exact crossings; section 2 derives the block count by two routes (closed form, and a numerical reconstruction of the curve with the crossings and lives found by bisection), both 5.53 blocks; section 3 evaluates the wrong crossings (4 or 6 blocks), the wrong damage rules (6 and 3) and the rounding robustness of the integer; section 4 embeds the program verify_key.py with its output.
