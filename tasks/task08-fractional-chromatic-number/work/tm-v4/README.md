# task08: smallest pairwise-covering fatigue test programme with unavailable level combinations (version 4: eight unavailable, gap two, unique optimum)

Engineering (materials testing, design of experiments), subdomain: Materials testing: design of a fatigue test programme (pairwise covering test matrices with constraints). Earlier contents of this folder (fractional chromatic number v1 and v2; three crack-growth versions; the earlier test-matrix versions: five unavailable with key 11, seven unavailable with unique key 10, six factors with key 11) are archived in work/v1, work/v2-math, work/eng-v1, work/eng-v2, work/eng-v3, work/tm-v1, work/tm-v2, work/tm-v3.

## Question

A fatigue test programme on metal injection moulded Ti-6Al-7Nb varies the five factors listed in the figure, each at three levels: the powder, the specimen geometry, the space-holder content, the oxygen content and the load ratio. Every specimen is made and tested at one level of each factor. The eight level combinations listed in the lower table of the figure are not available; a specimen containing any of them cannot be made or tested.

The programme must cover every admissible pair of levels of two different factors, which is to say that for any two factors and any level of the first with any level of the second, unless that combination is one of the eight unavailable ones, at least one specimen must carry both levels. No other requirement is imposed.

Find the smallest number of specimens with which this can be done. Give a single integer.

## Answer

11

## Solution

Step 1: Set up the counting objects.
Write the factors as $A$ (powder), $B$ (specimen geometry), $C$ (space-holder content), $D$ (oxygen content), $E$ (load ratio), with levels $0, 1, 2$ in the order of the figure, so that the unavailable combinations are $A_0C_2$, $A_0D_1$, $A_1C_1$, $A_1E_0$, $A_2B_2$, $B_0C_2$, $B_1D_2$ and $B_2E_1$. A specimen is a choice of one level per factor containing none of them; there are $82$ admissible specimens. The pairs to be covered are the $90 - 8 = 82$ admissible level pairs. Each specimen carries exactly one level pair for each of the ten factor pairs.

Step 2: The bounds that come first, and why they are not the answer.
The factor pairs $CD$, $CE$ and $DE$ keep all $9$ of their level pairs, and one specimen covers one level pair of a given factor pair, so at least $9$ specimens are needed. Counting specimens level by level gives no more: every level of every factor needs at least three specimens, and no level is forced into a single level of another factor. Neither $9$ nor $10$ specimens suffice, as the next step shows.

Step 3: Lower bound $11$.
Call two admissible level pairs incompatible if no admissible specimen contains both. Consider the eleven pairs
$$A_1B_0,\ A_1B_1,\ A_0E_1,\ A_0E_2,\ A_2E_1,\ A_2E_2,\ B_2D_1,\ C_2D_2,\ D_0E_0,\ D_1E_0,\ D_2E_0 .$$
They are pairwise incompatible, for the following reasons. Couples that need one factor at two different levels: $A_1B_j$ against $A_0E_n$ and $A_2E_n$ (factor $A$), $A_0E_n$ against $A_2E_n$ (factor $A$), $A_1B_0$ against $A_1B_1$ and both against $B_2D_1$ (factor $B$), every $A_iE_n$ with $n \in \{1, 2\}$ against the three $D_mE_0$ and against one another when $n$ differs (factor $E$), and $B_2D_1$, $C_2D_2$, $D_0E_0$, $D_1E_0$, $D_2E_0$ against one another whenever their $D$ levels differ (factor $D$). Couples whose union contains an unavailable combination: $A_1B_j$ with any $D_mE_0$ contains $A_1E_0$; $A_1B_0$ with $C_2D_2$ contains $B_0C_2$; $A_1B_1$ with $C_2D_2$ contains $B_1D_2$; $A_0E_n$ with $B_2D_1$ contains $A_0D_1$; $A_0E_n$ with $C_2D_2$ contains $A_0C_2$; $A_2E_n$ with $B_2D_1$ contains $A_2B_2$. Finally four couples whose union is admissible but cannot be completed to a specimen: $A_2E_n$ with $C_2D_2$ fixes $A_2$, $C_2$, $D_2$, and then $B_0$ is unavailable with $C_2$, $B_1$ with $D_2$ and $B_2$ with $A_2$, so no geometry remains; $B_2D_1$ with $D_1E_0$ fixes $B_2$, $D_1$, $E_0$, and then $A_0$ is unavailable with $D_1$, $A_1$ with $E_0$ and $A_2$ with $B_2$, so no powder remains; $C_2D_2$ with $D_2E_0$ fixes $C_2$, $D_2$, $E_0$, and then $A_0$ is unavailable with $C_2$, $A_1$ with $E_0$, and $A_2$ would leave no geometry, as just shown. Since each of the eleven pairs must be covered and no specimen covers two of them, every programme has at least $11$ specimens.

Step 4: Upper bound $11$, the decisive step.
The eleven specimens
$A_0B_0C_1D_2E_1$, $A_0B_1C_0D_0E_2$, $A_0B_2C_1D_0E_0$, $A_1B_0C_0D_1E_1$, $A_1B_1C_2D_0E_1$, $A_1B_2C_0D_1E_2$, $A_1B_2C_2D_2E_2$, $A_2B_0C_0D_2E_0$, $A_2B_0C_1D_0E_2$, $A_2B_1C_1D_1E_1$, $A_2B_1C_2D_1E_0$
are all admissible. Factor pair by factor pair they carry: $AB$: $A_0B_0$, $A_0B_1$, $A_0B_2$, $A_1B_0$, $A_1B_1$, $A_1B_2$ (twice), $A_2B_0$ (twice), $A_2B_1$ (twice), all $8$ admissible pairs; $AC$: $A_0C_1$ (twice), $A_0C_0$, $A_1C_0$ (twice), $A_1C_2$ (twice), $A_2C_0$, $A_2C_1$ (twice), $A_2C_2$, all $7$; $AD$: $A_0D_2$, $A_0D_0$ (twice), $A_1D_1$ (twice), $A_1D_0$, $A_1D_2$, $A_2D_2$, $A_2D_0$, $A_2D_1$ (twice), all $8$; $AE$: $A_0E_1$, $A_0E_2$, $A_0E_0$, $A_1E_1$ (twice), $A_1E_2$ (twice), $A_2E_0$ (twice), $A_2E_2$, $A_2E_1$, all $8$; $BC$: $B_0C_1$ (twice), $B_1C_0$, $B_2C_1$, $B_0C_0$ (twice), $B_1C_2$ (twice), $B_2C_0$, $B_2C_2$, $B_1C_1$, all $8$; $BD$: $B_0D_2$ (twice), $B_1D_0$ (twice), $B_2D_0$, $B_0D_1$, $B_2D_1$, $B_2D_2$, $B_0D_0$, $B_1D_1$ (twice), all $8$; $BE$: $B_0E_1$ (twice), $B_1E_2$, $B_2E_0$, $B_1E_1$ (twice), $B_2E_2$ (twice), $B_0E_0$, $B_0E_2$, $B_1E_0$, all $8$; $CD$: $C_1D_2$, $C_0D_0$, $C_1D_0$ (twice), $C_0D_1$ (twice), $C_2D_0$, $C_2D_2$, $C_0D_2$, $C_1D_1$, $C_2D_1$, all $9$; $CE$: $C_1E_1$ (twice), $C_0E_2$ (twice), $C_1E_0$, $C_0E_1$, $C_2E_1$, $C_2E_2$, $C_0E_0$, $C_1E_2$, $C_2E_0$, all $9$; $DE$: $D_2E_1$, $D_0E_2$ (twice), $D_0E_0$, $D_1E_1$ (twice), $D_0E_1$, $D_1E_2$, $D_2E_2$, $D_2E_0$, $D_1E_0$, all $9$. All $82$ admissible pairs are covered, so $11$ specimens suffice. This programme is the only one with $11$ specimens, as the complete enumeration in the verification notes shows.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $11$. The bound $9$ of Step 2 is not attainable and neither is $10$; sets of ten pairwise incompatible pairs that use only level clashes and unavailable combinations are easy to find, but closing the gap to $11$ needs the couples that are incompatible only because no completion to a specimen exists. Constructions that add specimens one at a time covering as many new pairs as possible end at $12$ or more almost always, because a single arrangement of $11$ specimens works.

Answer: $11$.

## Rubric

- c1 (5 pts, final answer): Gives $11$.
- c2 (2 pts): Exhibits an explicit programme of $11$ admissible specimens covering every admissible level pair (a correct $11$-row test matrix).
- c3 (2 pts): Proves that $10$ specimens are not enough by a valid argument, for instance a set of $11$ admissible level pairs no two of which fit into one admissible specimen (such as $A_1B_0$, $A_1B_1$, $A_0E_1$, $A_0E_2$, $A_2E_1$, $A_2E_2$, $B_2D_1$, $C_2D_2$, $D_0E_0$, $D_1E_0$, $D_2E_0$, including the couples that are incompatible only because they cannot be completed), or an exhaustive argument whose case structure is stated.
- c4 (1 pts): Establishes the lower bound $10$ (for instance from ten pairwise incompatible level pairs) and recognises that it is not attained.

Common wrong answers: 9, 10, 12, 13

## References box

Pairwise covering test suites (covering arrays of strength two) with constraints between factor levels, and the practice of building them greedily: D. M. Cohen, S. R. Dalal, M. L. Fredman and G. C. Patton, The AETG system: an approach to testing based on combinatorial design, IEEE Transactions on Software Engineering 23 (1997), 437-444. Covering arrays in general, their lower bounds and the hardness of finding minimum ones: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 82 admissible specimens and the 82 admissible pairs, checks the set of 11 pairwise incompatible pairs against every admissible specimen with the reason for each incompatible couple, checks the 11-specimen programme pair by pair, confirms the minimum by an integer programme and shows by complete enumeration that the 11-specimen programme is unique; the program is embedded with its output.

## Verify field

Section 3 of verification_notes.txt gives the lower-bound certificate: eleven admissible level pairs (A1B0, A1B1, A0E1, A0E2, A2E1, A2E2, B2D1, C2D2, D0E0, D1E0, D2E0 in the notation of the solution), checked against all 82 admissible specimens so that no specimen contains two of them, with the reason for every one of the 55 couples, four of which are incompatible only because no completion to a specimen exists. Section 4 gives the 11-specimen programme and checks that it covers all 82 admissible pairs. Section 5 confirms the minimum 11 by an integer programme (scipy HiGHS), shows by enumeration with no-good cuts that this programme is the only one with 11 specimens, and counts the eleven-pair certificates of the bound. Section 6 shows what randomised greedy constructions reach. Section 7 embeds the program verify_key.py with its output.

## Screen

(filled in after the screen)
