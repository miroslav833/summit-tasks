# Domains for new tasks

Read with note.md. This file says which domain the owner of this folder submits in and which shapes of
question are still worth building.

## Submission domain

Mathematics only. In task.json: `"domain": "mathematics"`. Confirmed on the Submit page on 2026-10-16
(Classification shows "Mathematics · Image" by default) and confirmed again by the owner on 2026-10-17:
no other category is open to this account. Do not build in Engineering, Physics, Biology or anything else,
and do not dress a mathematics question in a materials or engineering setting. The owner's research
background is not a source of settings for this account.

The account is in a trial period (banner on the Submit page). The first submissions carry more weight than
usual, so no rushed packages.

## What Summit has returned so far (all bandwidth, all "too easy")

- task05 v1, 12 vertices, bandwidth 4: Model A 3/3, 2.5 to 8.5 minutes.
- task05 v2, same graph, count of optimal numberings (6): 5/5.
- task06 v3 (submitted on the task05 entry SUM-MVB7DTW7), 16 vertices, bandwidth 5, no density bound,
  unique optimal numbering: 5/5 in 8 to 13 minutes, by the forced-ends squeeze and a fixed-ends search.

Model A reads a 16-vertex figure without error, finds a lower-bound argument that the local screen did not
find, and searches a fixed-ends numbering in ten minutes. The band is 1 to 3 correct out of 5.

## What has to hold before a question is built

1. No short lower bound. Run, in this order: degree bound, diameter bound, density bound over every
   connected induced subgraph, the forced-ends squeeze (pairs at distance at least ceil((n-1)/(b-1)); for
   each pair the distance intervals must admit a placement), and the prefix-boundary chain. If any of them
   settles the answer in a few lines, the instance is out.
2. No short construction. The optimal object must be hard to find even after the obvious reductions (fixed
   ends, level structure, breadth-first orders). Measure it before screening: a long annealer with
   restarts, and the size of the fixed-ends search tree. Anything a 10-minute hand search reaches is out.
3. Size just beyond hand reach: 18 to 22 vertices for graph layout questions. 14 and 16 are inside reach.
4. One exact integer answer, verified by two independent programs, with a written lower-bound proof in the
   notes (the chain listing is acceptable; Summit's reviewer proposed a search-based lower bound himself).
5. Screen with one Opus and one Sonnet run on figure plus stem. A single Opus solve under 15 minutes means
   5/5 at Summit. A cut-off is not a pass; Summit treats cut-offs as a defect of the question.

## Mathematics shapes still open

- Graph layout at 18 to 22 vertices (bandwidth, and its relatives cutwidth and minimum linear arrangement)
  with the five rejection tests above. The generator and proxies are in
  tasks/task06-bandwidth-fourteen/v3-sixteen/work (gen.py, gen3.py, gen4.py, eval.py).
- Other graph parameters where the certificate is short but the search is long: crossing number,
  pebbling number, fractional chromatic number. Sibling sessions have packages for each; read their task
  log rows before starting another.
- Combinatorics on a drawn structure with a decisive wrong-but-plausible step: a symmetry the natural count
  double-counts, an exact Markov chain answer where the "obvious" symmetry argument fails.
- Number theory and algebra read from a drawing: Galois groups from a Newton polygon or splitting diagram,
  class numbers, unit groups.

## Constrained covering arrays (added 2026-10-17, measured on task08)

Pure combinatorics, no setting needed: the smallest number of rows of an array over k columns and 3 symbols in which
every admissible pair of symbols in two different columns occurs in some row, where a short list of symbol pairs is
forbidden (no row may contain them). Exact key by integer programme (scipy milp), all optimal arrays enumerated with
no-good cuts, lower bound certified by LP duality: a set of pairwise incompatible pairs when the dual is integral, a
half-integral weighting otherwise. Tools: scratchpad ca/search_ca3.py, search_ca4.py, search_ca5.py (filters: no
forced symbol, minimum above the level-counting bound, few optimal arrays, key different from the unconstrained
covering array number CAN(2,5,3) = 11, CAN(2,6,3) = 12, which are retrievable).
Local results (3 Opus + 1 Sonnet, figure plus stem): 5 columns, unique optimal array, key 10: Opus 3/3 in 5.5 to 9
minutes, each run proving the bound by a counting argument and then constructing the unique array from the tightness
of the bound; Sonnet cut off. 6 columns, key 11 with a half-integral bound and four optimal arrays: Opus 0/3 by
cut-off, Sonnet 13. The window between is what the search_ca5 filter (LP integrality gap, so the bound has no
tight structure to construct from) is for.

## Shapes already burned

- Dessins d'enfants and Shabat polynomials at 9 to 12 edges: Opus solves on the first try (task01, task02).
- Matroid representability with one free parameter (task03): a standard routine for both models.
- Bandwidth at 12 to 16 vertices in any form, including the count of optimal numberings.
- Treewidth at 12 to 14 vertices: the heuristics find the optimum, no overshoot trap exists (task04).
- Knot invariants to ten crossings, clean derivations of any length, pixel reading of clean figures
  (archive, colleague's account).

## Plot-reading shape (added 2026-10-17 after the Engineering detour; the detour itself is not submittable)

Opus solves every fully specified calculation, however long, in minutes. In eleven screening rounds on a self-drawn log-log plot the one step that made it miss fairly was finding which gridline crossings a curve passes through exactly: told that a curve passes exactly through two crossings but not which, it declared crossings 10 to 20 percent off the curve or invented gridlines that were not drawn. A person with a ruler does not make those errors on the figure described below. Rules:

- Sparse grid: minor lines at 2 and 5 only. With minor lines at every integer the near misses are within half a millimetre on the print, unfair to a person too.
- The curve sits exactly on two crossings and at least 17 percent of a step from every other crossing at a labelled abscissa; check by program and list the distances in the verification notes.
- No straight line on log-log axes: it always passes within a few percent of some decade crossing and Opus reads that one. Use a curved member of a two-parameter family.
- Data markers, if any, off the anchor abscissae.
- The hint in the stem sets the band: no hint on the abscissae gave Opus 0/3, naming both gave 3/3, "both below 30" gave 2/3 and Sonnet 0/1.
- The asked quantity must change bin at two significant figures under every near-miss reading (check all decoy pairs by program) and sit at least 3 percent from both edges of its own bin.
- The mathematics behind the plot must be graduate level with an exact key verified two ways and one further wrong-but-plausible route; the plot only carries the parameters. Summit type 4 ("Figure/plot extraction with quantitative computation") is on the form for Mathematics.

First Mathematics candidate of this shape: tasks/task11-renewal-residual-life (renewal theory, log-logistic inter-arrival survival function, long-run mean residual life over the mean).

## The Engineering detour (2026-10-17) and what it left behind

Before the owner confirmed that only Mathematics is open, seven Engineering versions were built in the
task09 folder (v3 to v9: Kitagawa diagrams, El Haddad, S-N block loading, rainflow) and one in task05
(v5). None can be submitted. What they taught, in case a Mathematics question ever carries a self-drawn
plot: every fully specified calculation is solved 3/3; the only reading that moved Opus was a curved fit on
a sparse 1-2-5 log grid passing exactly through two crossings on minor gridlines, with every tempting
major-line pair 15 to 25 percent of a step off and no free anchor on the frame. That lever is a plot
trick, not mathematics, and a Mathematics reviewer would see it as such; use it only inside a question
whose hard step is mathematical.

For the pebbling family the proxies that matter are pi - T1 and pi - T2 (the key minus the largest
failing configuration with one pile, respectively with at most two piles). Summit's verdict on task09 v1
asked for distance 4, a residual piece of 9 to 10 vertices and many spread failing configurations; v2 met
those and still had T2 = key - 1. v10 (14 vertices, key 27) is the first instance with pi - T2 >= 1; the
search tools are in tasks/task09-pebbling-number/work/rev (search2.py, eval2.py).
