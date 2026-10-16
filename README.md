# Summit tasks (Mathematics)

One folder per task under tasks/. Each folder has the Import .zip (task.json + image.png + reference.txt at the top level), the README with the paste text for the References box ("Verify field"), the figure, and verify_key.py which recomputes the answer key.

| Task | Topic | Key | Zip |
|---|---|---|---|
| task01 | Shabat polynomial of a 9-edge plane tree, position of the valency-2 vertex | 0.1399 + 2.699i | tasks/task01-plane-tree-field-of-moduli/plane-tree-shabat-vertex-position.zip |
| task02 | Field of moduli of a 12-edge composite plane tree | 4 | tasks/task02-composite-tree-twelve-edges/composite-plane-tree-field-of-moduli.zip |
| task03 | Smallest field over which a 9-point configuration matroid is representable | 7 | tasks/task03-matroid-smallest-field/matroid-smallest-representing-field.zip |
| task05 | Bandwidth of a 12-vertex graph | 4 | tasks/task05-bandwidth/graph-bandwidth-twelve-vertices.zip |
| task06 | Bandwidth of a 14-vertex graph | 5 | tasks/task06-bandwidth-fourteen/graph-bandwidth-fourteen-vertices.zip |
| task07 | Crossing number of a 10-vertex, 21-edge graph (skewness 2, crossing number 3) | 3 | tasks/task07-crossing-number/graph-crossing-number-ten-vertices.zip |
| task06 v2 | Number of optimal numberings of a 14-vertex, 29-edge graph (counting version of task06, two edges added) | 6 | tasks/task06-bandwidth-fourteen/v2-count/graph-bandwidth-fourteen-optimal-numberings-count.zip |
| task08 | Fractional chromatic number of a 20-vertex planar 4-regular graph (revision of SUM-MVBCQZWW; the 12-vertex version, key 13/4, came back too easy and is kept in v1/) | 35/11 | tasks/task08-fractional-chromatic-number/fractional-chromatic-number-twenty-vertices.zip |
| task09 | Rooted pebbling number of a 10-vertex graph (target double-circled) | 13 | tasks/task09-pebbling-number/graph-rooted-pebbling-number-ten-vertices.zip |
| task10 | Bandwidth of a 16-vertex, 27-edge graph: no short lower bound, unique optimal numbering | 5 | tasks/task10-bandwidth-sixteen/graph-bandwidth-sixteen-vertices.zip |

Submission: Import .zip, open every section and check it, open References, make sure verification_notes.txt is attached (upload reference.txt by hand if not), paste the Verify field text from the task README into the explanation box, Submit.

note.md is the working log (rules, tooling, screen results, lessons).

## Direct download links for the Import .zip files

- task07 crossing number (10 vertices): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-crossing-number-ten-vertices.zip
- task10 bandwidth (16 vertices, hard instance): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-sixteen-vertices.zip
- task05 v4 (revision of SUM-MVB7DTW7, 14-vertex graph with a late-dying width-4 search): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-fourteen-vertices-v4.zip

- task09 rooted pebbling number (10 vertices): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-rooted-pebbling-number-ten-vertices.zip
- task05 v3 (revision of SUM-MVB7DTW7 with the reviewer's Graph A, 13 vertices): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-thirteen-vertices.zip

- task06 v2 (count of optimal numberings, 14 vertices, new figure): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-fourteen-optimal-numberings-count.zip
- task08 fractional chromatic number (20 vertices, revision): https://github.com/miroslav833/summit-tasks/raw/main/zips/fractional-chromatic-number-twenty-vertices.zip (the revision is entered field by field on the platform; the paste sheet is tasks/task08-fractional-chromatic-number/paste-for-edit.md)
- task05 v2 (count of optimal numberings, revision of the returned task05): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-optimal-numberings-count.zip

- task06 bandwidth (14 vertices): https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-fourteen-vertices.zip
- task05 bandwidth: https://github.com/miroslav833/summit-tasks/raw/main/zips/graph-bandwidth-twelve-vertices.zip
- task03 matroid: https://github.com/miroslav833/summit-tasks/raw/main/zips/matroid-smallest-representing-field.zip
- task02 composite tree: https://github.com/miroslav833/summit-tasks/raw/main/zips/composite-plane-tree-field-of-moduli.zip
- task01 plane tree: https://github.com/miroslav833/summit-tasks/raw/main/zips/plane-tree-shabat-vertex-position.zip

## Text for the References box (paste after the file is attached)

task07: Section 2 of verification_notes.txt checks the two facts given in the question (no single edge deletion and only the pairs 1-2 with 6-7 and 1-5 with 6-7 leave a planar graph) and gives the four-pairs argument that rules out two crossings; section 3 gives the figure's drawing with its four crossings and the straight-line drawing with three crossings, both with integer coordinates and the list of crossing pairs; section 4 is the exhaustive enumeration of crossing sets (none with one or two crossings, four with three); section 6 embeds the program verify_key.py with its full output, including an independent planarity test that does not use a graph library.

task10: Section 2 of verification_notes.txt is the written lower-bound proof (the first k vertices of a numbering of width 4 have at most four outside neighbours; the chain of such sets is listed in full and dies at six vertices). Section 3 gives two independent exact computations, section 4 the explicit numbering of width 5 with every edge stretch, section 5 the check that no degree, diameter or density bound reaches 5. Section 7 embeds the program with its output.

task05 v4: Section 2 of verification_notes.txt gives the two independent exact computations showing no numbering of width 4 exists (the pruned placement search with its tree printed to depth 3, and a dynamic programme), the check that every cheap lower bound stops at 4, and the two end-vertex tests that force nothing; section 3 gives the explicit width-5 numbering with every edge stretch; section 6 embeds the program verify_key.py with its full output.

task09: Sections 1 to 3 of verification_notes.txt give the graph, the trivial bounds, the twelve-pebble configuration (five pebbles on 9, five on 10, one on 4, one on 7, target 3) with the written proof that it fails and the list of all 590 configurations reachable from it, none with a pebble on 3; section 4 gives the two independent exact computations showing that every configuration of 13 pebbles reaches the target 3 (layer recursion and direct search, both embedded in the program verify_key.py with its full output in section 5), and the rooted pebbling numbers of all ten targets.

task05 v3: Section 2 of verification_notes.txt gives the two independent exact computations showing no numbering of width 4 exists (the pruned placement search with its tree printed to depth 3, and a dynamic programme) and the check that every cheap lower bound stops at 4; section 3 gives the explicit width-5 numbering with every edge stretch; section 6 embeds the program verify_key.py with its full output.

task08: Sections 3 and 4 of verification_notes.txt give the two certificates: the vertex weighting of total 35/11 (1/11 on vertices 2, 3, 4, 17, 20 and 2/11 on the other fifteen vertices) with the weight of every maximal independent set listed and the two facts behind it (every independent set of six vertices meets {2, 3, 4, 17, 20}; each of the nine independent sets of seven vertices contains three of them), and the seventeen weighted independent sets of total 35/11 that cover every vertex exactly once. Section 5 solves the linear programme exactly by a rational simplex and numerically by HiGHS, both giving 35/11. Section 6 computes the best induced-subgraph ratio 19/6 over all induced subgraphs. Section 7 embeds the program verify_key.py with its full output.

task06 v2: Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 5, the complete list of the six numberings of width 5 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six (the ends are 2 and 5 by a distance-2 ball count, 8 and 9 next to them); section 6 embeds the program with its output.

task05 v2: Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 4, the complete list of the six numberings of width 4 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six; section 6 embeds the program with its output.

task06: Sections 2 to 4 of verification_notes.txt give the certificate subgraph (the induced subgraph on vertices 1, 3, 4, 7, 8, 10, 11, 12, 13, 14 has ten vertices and diameter 2, with a common neighbour listed for every non-adjacent pair, so every numbering has width at least 5), the explicit numbering of width 5 with the stretch of every edge, and two independent exact computations (backtracking over numberings and a dynamic programme over sets of placed vertices) showing no numbering of width 4 exists. Section 6 embeds the program verify_key.py with its output.

task05: Sections 2 to 4 of verification_notes.txt give the lower-bound certificate (the induced subgraph on vertices 1, 2, 3, 4, 6, 9, 10, 11 has eight vertices and diameter 2, so every numbering has width at least 4), the explicit numbering of width 4 with the stretch of every edge, and two independent exact computations (backtracking over numberings and a dynamic programme over sets of placed vertices) showing no numbering of width 3 exists. Section 6 embeds the program verify_key.py with its output.

task03: Sections 1 to 3 of verification_notes.txt give the coordinatisation of the configuration (all nine points as vectors in one parameter t, with the eight incidences checked identically), the five degeneracy conditions (t = 0, 1, 2, 1/2 and the roots of t^2 - 3t + 1, each traced to the pair of points that coincide or the triple that becomes collinear), and the admissible parameters over each field up to GF(13), showing none exist over GF(2), GF(3), GF(4), GF(5) and that t = 3, 5, 6 work over GF(7). Section 4 is an independent brute-force search for representations in PG(2,q) for q up to 7. Section 5 embeds the program verify_key.py with its full output, including the explicit representation over GF(7) with every determinant.

task02: Sections 1 and 2 of verification_notes.txt give the quartic for the inner factor and its irreducibility; section 5 embeds verify_key.py, which rederives the quartic symbolically, traces the dessin for each of its four roots and compares it with the figure (the figure is the root s = 1.6628, the four trees are pairwise non-isomorphic), and section 4 recognises the Galois orbit independently from the normalised polynomials at 60 digits.

task01: Section 1 of verification_notes.txt gives the derivation down to the quartic for r; section 4 embeds the program verify_key.py, which redoes the derivation symbolically, traces the dessin for each of the four roots and compares it with the figure (only r = 0.1399 + 2.699i reproduces the drawn orientation), and enumerates the four plane trees of the passport; section 3 solves the full Shabat system numerically from random starts and recovers the same vertex.
