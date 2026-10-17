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

## Shapes already burned

- Dessins d'enfants and Shabat polynomials at 9 to 12 edges: Opus solves on the first try (task01, task02).
- Matroid representability with one free parameter (task03): a standard routine for both models.
- Bandwidth at 12 to 16 vertices in any form, including the count of optimal numberings.
- Treewidth at 12 to 14 vertices: the heuristics find the optimum, no overshoot trap exists (task04).
- Knot invariants to ten crossings, clean derivations of any length, pixel reading of clean figures
  (archive, colleague's account).
