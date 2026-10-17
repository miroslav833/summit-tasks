# task08: smallest covering array with six columns avoiding ten forbidden pairs

Mathematics, subdomain: Combinatorial design theory: covering arrays avoiding forbidden pairs. The five-column version (key 10, solved by Opus 3/3 locally) is archived in work/ca-v1. Earlier contents of this folder (fractional chromatic number; three crack-growth versions; four test-matrix versions) are archived under work/.

## Question

An array has $N$ rows and $6$ columns. The entries $x_1, \dots, x_5$ of a row are symbols from $\{0, 1, 2\}$ and the entry $x_6$ is a symbol from $\{0, 1\}$. The figure marks ten forbidden pairs: a cell marked F in the row labelled $x_i = a$ and the column labelled $x_j = b$ means that no row of the array may have $x_i = a$ and $x_j = b$ at the same time. Every row of the array must avoid all ten forbidden pairs.

The array is called covering if, for every two distinct columns $i$ and $j$ and every pair of symbols $(a, b)$ allowed in those columns that is not forbidden, some row of the array has $x_i = a$ and $x_j = b$. Nothing else is required.

Find the smallest $N$ for which a covering array exists. Give a single integer.

## Answer

10

## Solution

Step 1: Set up the counting objects.
Write $A, \dots, F$ for the columns $x_1, \dots, x_6$ and $A_a$ for the entry $x_1 = a$. The forbidden pairs read from the figure are $A_1B_1$, $A_1C_2$, $A_1E_1$, $A_2C_0$, $A_2D_0$, $C_0E_0$, $C_1F_0$, $C_2E_1$, $D_0E_1$ and $D_2F_0$. An admissible row avoids all of them; there are $136$ admissible rows out of $3^5 \cdot 2 = 486$. The pairs to be covered are the $120 - 10 = 110$ admissible symbol pairs, and each row carries exactly one symbol pair for each of the fifteen column pairs.

Step 2: The bounds that come first.
The column pairs $BC$, $BD$, $BE$ and $CD$ keep all $9$ of their symbol pairs, so $N \ge 9$. Without forbidden pairs the smallest covering array with five ternary and one binary column has $11$ rows; the forbidden pairs remove requirements as well as rows, and the answer is smaller.

Step 3: Lower bound $10$.
Call two admissible symbol pairs incompatible if no admissible row contains both. The ten pairs
$$B_0E_1,\ B_1E_1,\ B_2E_1,\ C_0D_0,\ C_1D_0,\ C_2D_0,\ D_1E_0,\ D_1E_2,\ D_2E_0,\ D_2E_2$$
are pairwise incompatible. Pairs that need one column with two different symbols account for most couples: the three $B_jE_1$ differ in $B$, the three $C_iD_0$ differ in $C$, the four $D_mE_n$ differ in $D$ or $E$ among themselves, every $B_jE_1$ differs in $E$ from every $D_mE_n$ (where $n \in \{0, 2\}$), and every $C_iD_0$ differs in $D$ from every $D_mE_n$ (where $m \in \{1, 2\}$). The remaining nine couples, $B_jE_1$ with $C_iD_0$, put $x_4 = 0$ and $x_5 = 1$ into one row, which is the forbidden pair $D_0E_1$. In words: the symbol $1$ in column $E$ must meet all three symbols of column $B$, the symbol $0$ in column $D$ must meet all three symbols of column $C$ on rows that cannot have $x_5 = 1$, and the four pairs $(x_4, x_5) \in \{1, 2\} \times \{0, 2\}$ need four more rows. Hence $N \ge 3 + 3 + 4 = 10$.

Step 4: Upper bound $10$, the decisive step.
The ten rows (written $x_1 x_2 x_3 x_4 x_5 x_6$)
$$001211,\ 010110,\ 011021,\ 022000,\ 100020,\ 101101,\ 120221,\ 202120,\ 212201,\ 221111$$
contain no forbidden pair. Column pair by column pair they carry every admissible symbol pair: $AB$ all $8$ (everything except $A_1B_1$), $AC$ all $7$, $AD$ all $8$, $AE$ all $8$, $AF$ all $6$; $BC$, $BD$, $BE$ all $9$ each; $BF$ all $6$; $CD$ all $9$; $CE$ all $7$ (missing only $C_0E_0$ and $C_2E_1$); $CF$ all $5$ (missing only $C_1F_0$); $DE$ all $8$ (missing only $D_0E_1$); $DF$ all $5$ (missing only $D_2F_0$); $EF$ all $6$. For instance $CD$ is read off as $C_1D_2$, $C_0D_1$, $C_1D_0$, $C_2D_0$, $C_0D_0$, $C_1D_1$, $C_0D_2$, $C_2D_1$, $C_2D_2$, $C_1D_1$, and $DE$ as $D_2E_1$, $D_1E_0$, $D_0E_2$, $D_0E_0$, $D_0E_2$, $D_1E_1$, $D_2E_2$, $D_1E_2$, $D_2E_0$, $D_1E_1$. All $110$ admissible pairs are covered, so $N = 10$ is attained. A $10$-row array must use each of the ten pairs of Step 3 on its own row, which leaves very little freedom: exactly two covering arrays with $10$ rows exist (the verification notes enumerate them), so the construction cannot be found by local improvements of a greedy array.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $N = 10$. The bound $9$ is not attainable, and the unconstrained value $11$ is one too many; constructions that add rows greedily end at $11$ to $16$.

Answer: $10$.

## Rubric

- c1 (5 pts, final answer): Gives $10$.
- c2 (3 pts): Exhibits an explicit covering array of $10$ admissible rows (every admissible symbol pair present, no forbidden pair in any row).
- c3 (1 pts): Proves that $9$ rows are not enough by a valid argument, for instance ten admissible symbol pairs no two of which fit into one admissible row (such as $(x_2,x_5) = (0,1), (1,1), (2,1)$, $(x_3,x_4) = (0,0), (1,0), (2,0)$ and $(x_4,x_5) = (1,0), (1,2), (2,0), (2,2)$), or an equivalent counting argument.
- c4 (1 pts): States the bound of $9$ rows from a column pair with $9$ admissible symbol pairs and recognises that it is not attained.

Common wrong answers: 9, 11, 12, 13

## References box

Covering arrays avoiding forbidden edges, which is exactly the object of the question, and the hardness of their minimum size: P. Danziger, E. Mendelsohn, L. Moura and B. Stevens, Covering arrays avoiding forbidden edges, Theoretical Computer Science 410 (2009), 5403-5414. Covering arrays in general and their known small values: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 136 admissible rows and 110 admissible pairs, checks the set of ten pairwise incompatible pairs against every admissible row with the reason for each couple, checks the 10-row array column pair by column pair, confirms the minimum by an integer programme and enumerates the two optimal arrays; the program is embedded with its output.

## Verify field

Section 3 of verification_notes.txt gives the lower-bound certificate: ten admissible symbol pairs (B0E1, B1E1, B2E1, C0D0, C1D0, C2D0, D1E0, D1E2, D2E0, D2E2, where A to F stand for the columns x1 to x6), checked against all 136 admissible rows so that no row contains two of them, with the reason for every one of the 45 couples. Section 4 gives the 10-row array and checks every column pair. Section 5 confirms the minimum 10 by an integer programme (scipy HiGHS) and enumerates the two optimal arrays. Section 7 embeds the program verify_key.py with its output.

## Screen

Six columns (five ternary, one binary), ten forbidden pairs, key 10, two optimal arrays: Opus 3/3 correct (2.5, 4 and about 5 minutes), Sonnet 1/1 correct (8 minutes). Every run proved 9 impossible by a counting argument on the unconstrained column pairs and then built one of the two optimal arrays from the forced structure (group sizes 4, 3, 3 on one column). Too easy.

Five-column version (key 10, archived in work/ca-v1): Opus 3/3, Sonnet lost.

