
## Summit verdict on task08 (2026-10-16) and the revision

Item SUM-MVBCQZWW came back "too easy": it failed at the weaker-model probe (Sonnet trial 1 gave 13/4 with rubric 6/10,
trial 3 gave 13/4 with rubric 8/10), before the Opus rollouts. Reason given: 113 independent sets is small enough to list
by hand and solve the linear programme, and the 13:4-colouring is easy to find. One advisory on the solution: in the
lower-bound case split say "other positive-weight members", since the weight-0 vertices 6 and 7 can sit in those sets.
Lesson for the LP-duality family: the size that Sonnet still solves by hand is about 12 vertices and 100 independent
sets; the local Sonnet 5.5 screen (0/1 after a misread crossing) was no signal, because the miss came from the figure,
not from the mathematics. A 12-vertex graph is not "beyond hand reach" for this parameter.

Revision (same entry, edited field by field; paste sheet in tasks/task08-fractional-chromatic-number/paste-for-edit.md,
v1 kept in work/v1 and in the repo under v1/): a planar 4-regular graph on 20 vertices, built as the medial graph of a
random planar graph with 20 edges (scratchpad fc/planar4.py) so that the figure is a planar straight-line drawing
(Tutte embedding with a pentagonal outer face plus a planarity-preserving hill-climb; no crossing to misread). Search
filters as before (chi_f above n/alpha and above every induced-subgraph ratio, denominator at least 5); planar medial
graphs on 18 to 20 vertices give values 19/6, 16/5, 22/7, 29/9, 35/11. Chosen: 35/11 (seed 112): 2455 non-empty
independent sets, 212 maximal, alpha = 7, omega = 3, chi = 4, trivial automorphism group; n/alpha = 20/7, and the
best induced-subgraph ratio over all 2^20 subsets is 19/6 (delete vertex 2 or 3). Dual certificate: 1/11 on
L = {2, 3, 4, 17, 20} and 2/11 elsewhere; weight of an independent set is (2|I| - |I meets L|)/11, so the proof reduces to
two facts, every independent 6-set meets L (G - L has independence number 5) and each of the nine independent 7-sets
contains 2, 3 and one of 17, 20. Primal: 17 sets with weights k/11 covering every vertex exactly once (a 35:11-colouring).
Wrong routes computed: 20/7, 3, 19/6, 4, 7/2 (no 6:2-colouring). Verification as before (exact rational simplex, HiGHS,
brute-force certificate checks, numpy Hall-ratio pass over all subsets); the embedded program reruns to identical output
in about a minute. Risk, stated to the owner: at 20 vertices nobody solves the LP by hand, so the realistic Summit
outcomes are 0/5 (then "too hard") or guesses; the owner asked for this size.
SCREEN_PLACEHOLDER
