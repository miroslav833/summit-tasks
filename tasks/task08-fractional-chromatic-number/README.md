# task08: smallest covering array with five columns avoiding seven forbidden pairs

Mathematics, subdomain: Combinatorial design theory: covering arrays avoiding forbidden pairs. The same instance was first built as an engineering test-matrix question (archived in work/tm-v2); the account offers only the Mathematics category, so the question is now stated as pure combinatorics. Earlier contents of this folder (fractional chromatic number; three crack-growth versions; four test-matrix versions) are archived under work/.

## Question

An array has $N$ rows and $5$ columns, and every entry is one of the symbols $0$, $1$, $2$. Write $x_1, \dots, x_5$ for the entries of a row. The figure marks seven forbidden pairs: a cell marked F in the row labelled $x_i = a$ and the column labelled $x_j = b$ means that no row of the array may have $x_i = a$ and $x_j = b$ at the same time. Every row of the array must avoid all seven forbidden pairs.

The array is called covering if, for every two distinct columns $i$ and $j$ and every pair of symbols $(a, b)$ that is not forbidden for the columns $(i, j)$, some row of the array has $x_i = a$ and $x_j = b$. Nothing else is required.

Find the smallest $N$ for which a covering array exists. Give a single integer.

## Answer

10

## Solution

Step 1: Set up the counting objects.
The forbidden pairs read from the figure are $(x_1 = 0, x_5 = 1)$, $(x_1 = 1, x_2 = 0)$, $(x_1 = 1, x_3 = 2)$, $(x_1 = 2, x_2 = 1)$, $(x_2 = 1, x_3 = 1)$, $(x_2 = 1, x_4 = 1)$ and $(x_4 = 0, x_5 = 0)$. Write $A, B, C, D, E$ for the columns $x_1, \dots, x_5$ and $A_a$ for the entry $x_1 = a$, so that the forbidden pairs are $A_0E_1$, $A_1B_0$, $A_1C_2$, $A_2B_1$, $B_1C_1$, $B_1D_1$, $D_0E_0$. An admissible row is a word of length $5$ over $\{0, 1, 2\}$ containing none of them; there are $105$ admissible rows. The pairs to be covered are the $90 - 7 = 83$ admissible symbol pairs. Each row carries exactly one symbol pair for each of the ten column pairs.

Step 2: The bound that comes first, and why it is not the answer.
The column pairs $AD$, $BE$, $CD$ and $CE$ keep all $9$ of their symbol pairs, and one row covers one symbol pair of a given column pair, so $N \ge 9$. Nine rows would have to form an orthogonal array on each of these column pairs at once, and the forbidden pairs make that impossible, as the next step shows in a way that counts. The unconstrained covering array number for five columns and three symbols is $11$, but it is not relevant here: the forbidden pairs remove seven pairs from the covering requirement, and the answer turns out to be smaller.

Step 3: Lower bound $10$.
Call two admissible symbol pairs incompatible if no admissible row contains both. Consider the ten pairs
$$A_0D_0,\ A_0D_1,\ A_0D_2,\ A_1E_0,\ A_1E_2,\ A_2E_0,\ A_2E_2,\ B_0E_1,\ B_1E_1,\ B_2E_1 .$$
They are pairwise incompatible: the three $A_0D_m$ disagree in column $D$ with one another and in column $A$ with the $A_1E_n$ and $A_2E_n$; the $A_1E_n$ and $A_2E_n$ disagree in column $A$ or in column $E$ with one another; the three $B_jE_1$ disagree in column $B$ with one another and in column $E$ with the $A_1E_n$ and $A_2E_n$ (which have $n \in \{0, 2\}$); and $A_0D_m$ with $B_jE_1$ would put $x_1 = 0$ and $x_5 = 1$ in one row, which is forbidden. In words: the rows with $x_1 = 0$ must show all three symbols in column $D$, so there are at least three of them; the rows with $x_1 = 1$ and the rows with $x_1 = 2$ must each show the symbols $0$ and $2$ in column $E$, so there are at least two of each; and the symbol $1$ in column $E$ must meet all three symbols of column $B$, on three further rows, none of which can have $x_1 = 0$ and none of which is among the four rows just counted, since those have $x_5 \in \{0, 2\}$. That is $3 + 2 + 2 + 3 = 10$ rows at least.

Step 4: Upper bound $10$, the decisive step.
The ten rows (written $x_1 x_2 x_3 x_4 x_5$)
$$00102,\ 01220,\ 02012,\ 11001,\ 11022,\ 12110,\ 20020,\ 20211,\ 22121,\ 22202$$
are all admissible: none contains $A_0E_1$, $A_1B_0$, $A_1C_2$, $A_2B_1$, $B_1C_1$, $B_1D_1$ or $D_0E_0$. Listing the symbol pairs they carry, column pair by column pair: $AB$ gives $A_0B_0$, $A_0B_1$, $A_0B_2$, $A_1B_1$ (twice), $A_1B_2$, $A_2B_0$ (twice), $A_2B_2$ (twice), all $7$ admissible pairs; $AC$ gives $A_0C_0$, $A_0C_1$, $A_0C_2$, $A_1C_0$ (twice), $A_1C_1$, $A_2C_0$, $A_2C_1$, $A_2C_2$ (twice), all $8$; $AD$ gives all nine $A_aD_m$, since the three rows with $x_1 = 0$ carry $D_0$, $D_2$, $D_1$, the three rows with $x_1 = 1$ carry $D_0$, $D_2$, $D_1$ and the four rows with $x_1 = 2$ carry $D_2$, $D_1$, $D_2$, $D_0$; $AE$ gives $A_0E_2$, $A_0E_0$, $A_1E_1$, $A_1E_2$, $A_1E_0$, $A_2E_0$, $A_2E_1$, $A_2E_2$, all $8$; $BC$ gives $B_0C_1$, $B_1C_2$, $B_2C_0$, $B_1C_0$, $B_2C_1$, $B_0C_0$, $B_0C_2$, $B_2C_2$, all $8$; $BD$ gives $B_0D_0$, $B_1D_2$, $B_2D_1$, $B_1D_0$, $B_2D_2$, $B_0D_2$, $B_0D_1$, $B_2D_0$, all $8$; $BE$, $CD$ and $CE$ give all $9$ each (for $CD$: $C_1D_0$, $C_2D_2$, $C_0D_1$, $C_0D_0$, $C_0D_2$, $C_1D_1$, $C_2D_1$, $C_1D_2$, $C_2D_0$); $DE$ gives $D_0E_2$, $D_2E_0$, $D_1E_2$, $D_0E_1$, $D_2E_2$, $D_1E_0$, $D_1E_1$, $D_2E_1$, all $8$. All $83$ admissible pairs are covered, so $N = 10$ is attained. This array is the only covering array with $10$ rows: with exactly $10$ rows every one of the ten pairs of Step 3 sits on its own row, which fixes $x_1$ and one more entry of each row, and the remaining entries are then forced one by one; the verification notes confirm by complete enumeration that no other $10$-row covering array exists.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $N = 10$. The bound $9$ of Step 2 is not attainable, and the unconstrained value $11$ is one too many. Constructions that start from a $3 \times 3$ orthogonal array on two of the columns, or add rows one at a time covering as many new pairs as possible, end at $11$ or more, because only one arrangement of $10$ rows works.

Answer: $10$.

## Rubric

- c1 (5 pts, final answer): Gives $10$.
- c2 (3 pts): Exhibits an explicit covering array of $10$ admissible rows (every admissible symbol pair present, no forbidden pair in any row).
- c3 (1 pts): Proves that $9$ rows are not enough by a valid argument, for instance a set of $10$ admissible symbol pairs no two of which fit into one admissible row (such as $A_0D_0$, $A_0D_1$, $A_0D_2$, $A_1E_0$, $A_1E_2$, $A_2E_0$, $A_2E_2$, $B_0E_1$, $B_1E_1$, $B_2E_1$ in the notation of the solution), or an equivalent counting argument.
- c4 (1 pts): States the bound of $9$ rows from a column pair with $9$ admissible symbol pairs and recognises that the forbidden pairs make it unattainable.

Common wrong answers: 9, 11, 12, 13

## References box

Covering arrays avoiding forbidden edges (CAFEs), which is exactly the object of the question, with the reduction to graph homomorphisms and the hardness of the minimum size: P. Danziger, E. Mendelsohn, L. Moura and B. Stevens, Covering arrays avoiding forbidden edges, Theoretical Computer Science 410 (2009), 5403-5414. Covering arrays in general, their lower bounds and known small values such as $\mathrm{CAN}(2, 5, 3) = 11$: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 105 admissible rows and the 83 admissible pairs, checks the set of 10 pairwise incompatible pairs against every admissible row with the reason for each incompatible couple, checks the 10-row array pair by pair, confirms the minimum by an integer programme and shows by complete enumeration that the 10-row array is unique; the program is embedded with its output.

## Verify field

Section 3 of verification_notes.txt gives the lower-bound certificate: ten admissible symbol pairs (A0D0, A0D1, A0D2, A1E0, A1E2, A2E0, A2E2, B0E1, B1E1, B2E1, where A to E stand for the columns x1 to x5), checked against all 105 admissible rows so that no row contains two of them, with the reason for every one of the 45 couples. Section 4 gives the 10-row array and checks that it covers all 83 admissible pairs. Section 5 confirms the minimum 10 by an integer programme (scipy HiGHS), shows by enumeration with no-good cuts that this array is the only one with 10 rows, and counts 47 different ten-pair certificates of the bound. Section 6 shows that randomised greedy constructions reach only 12 to 15 rows. Section 7 embeds the program verify_key.py with its output.

## Screen

Mathematics version (5 columns over {0,1,2}, seven forbidden pairs, unique optimal array, key 10): Opus 3/3 correct (266 s, 384 s, 597 s), each with a counting proof that 9 rows fail (balanced columns forced by the unconstrained column pairs, then one count table runs out of room) and the unique 10-row array found by hand. Sonnet: the run was lost when the session restarted, no result.

Same family, engineering wording (archived in work/tm-v1 to work/tm-v4): 5 columns key 11 Opus 3/3; 5 columns unique key 10 Opus 3/3; 5 columns gap two unique key 11 Opus 3/3 in 22 to 32 minutes (slack propagation through three count tables); 6 columns key 11 Opus 0/3 by cut-off. Sonnet never finished or overshot.

