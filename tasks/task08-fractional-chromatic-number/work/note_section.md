
## Session 2026-10-16 (evening): fractional chromatic number, task08

New mechanism, not tried before on this account: a parameter defined by a linear programme whose two certificates
(primal and dual) are both short, with the instinctive formula wrong. The fractional chromatic number of a regular
graph is n/alpha only when the graph is vertex-transitive; regular alone is not enough, and the drawn graph is
4-regular on 12 vertices with automorphism group of order 2. Design: search over random 4-regular graphs
(scratchpad fc/search2.py, scipy LP plus exact rational certificates) for instances where chi_f beats every
induced-subgraph ratio |S|/alpha(G[S]), so that no "density" style bound (the route Opus found for the bandwidth
tasks) reaches the answer. Cubic graphs on 12 vertices never do (chi_f is always 5/2, 8/3 or 3, equal to a C5,
8-vertex or triangle bound); 4-regular graphs on 12 vertices give about 40 such instances per 1500 seeds, most
with chi_f = 13/4, a few with 19/6, 16/5, 25/8, 22/7. Chosen: seed 455, chi_f = 13/4 against n/alpha = 3,
omega = 3, best subgraph ratio 3, chi = 4; 22 maximal independent sets, 113 independent sets in all; dual
certificate 1/2 on a triangle and 1/4 on seven more vertices, with a hand proof (case split on the triangle,
no independent triple among the remaining weight-1/4 vertices); primal certificate nine sets with weights
1/4 and 1/2, equivalently a 13:4-colouring. Wrong routes computed, not guessed: 3 (n/alpha, omega, subgraph
ratio, also the value a solver gets who mistakes the graph for the Chvatal graph, which has the same
parameters 12 vertices, 24 edges, 4-regular), 7/2 (best 2-fold colouring, chi_2 = 7), 10/3 (best 3-fold,
chi_3 = 10), 4 (chi). Key verified by: brute-force certificate checks over all 113 independent sets, an exact
rational tableau simplex written in the standard library, scipy HiGHS, and a k:d-colouring search (no 6:2,
9:3, 12:4). Program embedded in reference.txt, re-extracted and rerun to identical output. Figure: spring
layout followed by a hill-climb on crossings (6), vertex-to-edge distance and angular resolution
(work/layout.py, hill.py, hill2.py, polish.py; coordinates hardcoded in draw_figure.py). Findability: the
value 13/4 appears in the literature as the Hall ratio of 4-regular graphs of girth 4 (arXiv 1904.05618),
which does not apply to this graph (it has triangles); the stem and the drawn graph are not online.
Folder name: task07 was taken by a sibling session (crossing number) while this was being built, so this one
is task08.
SCREEN_PLACEHOLDER
