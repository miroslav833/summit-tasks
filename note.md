# Summit working notes

Read this file first in every new session, before drafting anything. Then read domains-for-new-task.md, instruction.md and submission-guide.md. For writing style read ../Humanize.md (and skim ../HumanWritingRecord.md for the sentence feel). humanism.md in this folder is only a pointer to those two.

## Design brief for the next candidate (written 2026-10-16 after nine solved candidates)

What is known to fail at Summit's size: any question whose hard side is a proof that something is
impossible. Opus 5.5 finds a short impossibility argument for layouts (forced ends by distance or 2-balls,
prefix boundaries, a middle split), for Shabat polynomials (derivative identity), for matroids (one
parameter plus degeneracies). Nine candidates, every Opus run correct.

What has never been tested here and is the only shape with a recorded Opus miss (the archive's task08,
accepted; its G2 with a unique optimal sequence, Opus 3/8): the hard side is a CONSTRUCTION with very few
solutions, the impossibility side is trivial (a counting bound that is tight), and a solver who fails to
find the construction overshoots or undershoots and writes a false proof in a modest number of tokens
(no cut-off). Candidates in this shape: a cubic graph of girth 5 that is 3-edge-colourable with one or two
colourings (ask for the maximum number of pairwise edge-disjoint perfect matchings: 3 if found, a false
"snark" answer of 1 if not); an edge-decomposition of a drawn graph into triangles or K4's with a unique
decomposition (ask for the maximum number of edge-disjoint copies; the trivial bound m/3 is tight and the
greedy attempts stall one short); more generally any exact-cover instance with a unique cover and many
near-covers. Generate by computer, keep instances with 1 or 2 solutions and many maximal near-solutions,
screen with three Opus runs. Started 2026-10-16 as tasks/task08-cubic-matchings (generator running).

## What this folder is (owner's section, written 2026-10-16)

This folder belongs to the owner of this box. The long log that starts at "Archive" further down was written by a colleague on a different Summit account (Biology/Medicine only) and was copied here so new sessions can learn from what already failed. It is reference, not instructions. None of its task folders, scripts, scratchpad files or the summit-task skill exist on this box. Its task log statuses are his submissions, not ours.

Account check 2026-10-17: the Category dropdown offers only Mathematics on both the new-task form and the revision editor, so this account is Mathematics only; see domains-for-new-task.md. An Engineering detour on 2026-10-17 (task05 v5, crack growth from a pore) is not submittable but produced the screening lessons in the task05 v5 row below: the only lever that moved Opus fairly was finding the exact gridline crossings of a self-drawn curve on a sparse 1-2-5 grid.

Submit page as seen 2026-10-16: four required sections (Classification, Question & answer key, Solution, Grading rubric) plus optional References, a progress line "0 of 4 sections complete", Import .zip at the top right, Submit question at the bottom. Subdomain is a required text field inside Classification; the page refuses to submit with "Subdomain is required" if it is blank, so task.json must always carry a specific `subdomain`.

## Hard rules for every task

1. Everything that goes to Summit must read as written by a person. Question, solution, rubric lines, image-necessity box, references, reference.txt. Plain prose, the voice of a mathematician writing a problem for a graduate exam. No em dashes, no "Note that", no bullet-list solutions, no remarks about models or about the question itself. Run the detector in ../Humanize.md on every text field before packaging, then do the read-aloud test. The owner edits the final prose himself; drafts are drafts.
2. One folder per task under AQ_Summit/tasks/, named taskNN-short-slug. Never two tasks in one folder.
3. The answer key is verified by two independent routes before the figure is drawn. Both routes, with their code and output, go into reference.txt. Summit's consistency check reads only the uploaded file, so every computational claim needs its program embedded there, with the command line and the Python version.
4. Difficulty sits in one decisive step that the obvious approach gets wrong, not in volume. A question that needs a long search is returned as "unfair" even when the models miss it (see the archive, task06 verdict). A question that is a known theorem plus a finite case analysis is solved five out of five.
5. Do not reuse a stem from the archive. The duplicate check runs across accounts' submissions as far as we know, and a byte-identical stem was refused once (archive, task11).
6. Screen before submitting: one Opus 5.5 high agent and one Sonnet agent, figure plus stem only, no web, no code. Report both to the owner, who decides. If Opus solves it but there is a plausible change that could make it fail, improve and re-screen rather than stopping.
7. Add a row to the task log below whenever a task is created, and update it after Summit returns a verdict.

## Tools on this box

- Python 3.12 system-wide, no pip. A persistent venv with pip, numpy, sympy, scipy, matplotlib, networkx and mpmath is at AQ_Summit/venv. Use `venv/bin/python` for everything. If it is ever missing, rebuild it: `python3 -m venv --without-pip venv`, fetch get-pip.py from bootstrap.pypa.io, `venv/bin/python get-pip.py`, then `venv/bin/pip install numpy sympy scipy matplotlib networkx mpmath`.
- No TeX. No pdflatex, no TikZ, no Asymptote, no Sage, no PARI, no Graphviz, no ImageMagick. Figures are made with matplotlib (mathtext handles labels like $\delta_p$). Save PNG at 300 dpi and a PDF of the same figure, keep the .py that drew it.
- pdftoppm, zip and unzip are available.
- No sudo. Anything else must be installed user-local (venv or a tarball under the home directory) and recorded here.

## Delivery: the GitHub repo

Finished packages are mirrored to the public repo https://github.com/miroslav833/summit-tasks (local clone at
~/aq-summit-repo). Layout: tasks/<task folder> (zip, task.json, image, reference.txt, verify_key.py, README),
zips/ (every Import .zip at the top level, direct links https://github.com/miroslav833/summit-tasks/raw/main/zips/<name>.zip),
README.md (table of tasks, direct links, and the paste text for the References box of each task). The owner
submits from there with a browser extension. Pushing needs a GitHub token pasted by the owner in the session;
use it once on the remote URL and reset the URL to the plain https address afterwards. The Summit import
fills the four sections and attaches the reference file but leaves the "explain where to verify" box empty,
so every README carries that text under "Verify field".

Summit calibration in progress (2026-10-16): task05 (bandwidth, 12 vertices) and task03 (matroid) were
submitted. Their verdicts decide the next design: 5/5 means the local single-run screens are representative
and the family is too easy at any size; cut-offs mean the solve length is the problem; 1 to 4 means the
band is reachable by run-to-run variance and more instances of the same shape are worth making.

## Folder layout for a task

```
AQ_Summit/tasks/taskNN-slug/
  task.json            Summit package, schema summit-task-package-v1
  image.png            the figure, 300 dpi, drawn by code
  image.pdf            vector version of the same figure
  draw_figure.py       the script that produced it
  reference.txt        verification notes uploaded as the References file: both routes, embedded programs, outputs
  verify_*.py          scripts that compute the key independently
  README.md            human-readable copy of every field, the screen tally, and the paste-ready text for the References box
  <slug>.zip           task.json + image.png + reference.txt at the top level, for Import .zip
```

Build task.json with a small Python script rather than by hand so LaTeX escaping stays right. Validate before zipping: rubric points sum to 10, exactly one final-answer criterion that states the key, no common wrong answer equal to the key, answerPrecision matches the stem wording, domain is mathematics.

## Workflow for a new session

1. Read this file, domains-for-new-task.md, instruction.md, submission-guide.md, ../Humanize.md.
2. Pick a subfield from domains-for-new-task.md and design the trap first: the step where the natural approach gives a plausible wrong number. Choose parameters so the correct and trap answers differ at the requested precision.
3. Compute the key by two routes. Compute the common wrong answers by running the wrong methods, not by guessing.
4. Draw the figure. Every number the solver needs is in the figure and nowhere in the text. Labels must not overlap. Check the PNG by eye.
5. Write stem, solution, rubric, reference.txt. Run the humanize detector. Read aloud.
6. Build and validate the package.
7. Search the web for the stem and the key.
8. Screen (rule 6). Report to the owner with the tally and the paste-ready References text. The owner submits.

## Task log (this account)

| Folder | Topic | Answer key | Status |
|---|---|---|---|
| task01-plane-tree-field-of-moduli | Shabat polynomial of a 9-edge plane tree (passport 4,2,1,1,1 / 2,2,2,2,1), normalised by two vertex positions. v1 asked for the leading coefficient of the decomposable tree (key 1/256): screen Opus 1/1 and Sonnet 1/1, both by the derivative identity P' = 9c x^3 (x-r) Q plus the rational root, 5 and 9 minutes; too easy, archived in work/. v2 asks for the position of the valency-2 black vertex of one of the two chiral trees of the same passport: same derivation, but the answer is one of two conjugate roots and only the drawn orientation decides | v2: 0.1399 + 2.699i (4 s.f.) | v2 built 2026-10-16, key by three routes (symbolic derivation, dessin tracing for all four roots against the figure, random-start Newton). Screen v2: Opus 1/1 correct (same derivation, then edge directions at the centre from the local coefficient to pick the conjugate; 8 min, 77k tokens); Sonnet 0/1, cut off at the 64k output ceiling with no answer. Not submitted: Opus solves it on the first try and the token cost makes Summit cut-offs likely. Package complete, kept for reference |
| task02-composite-tree-twelve-edges | Degree of the field of moduli of a 12-edge plane tree that is a composition Q(R) of the 3-edge path Q = 3y^2-2y^3 with a quartic R whose critical values are the path vertices 0, 3/2, 1; the inner parameter satisfies 3s^4-6s^3+4s-2 = 0, irreducible, and the four roots give four non-isomorphic trees (two symmetric, one chiral pair), so the orbit has size 4. Derivative identity at degree 12 leaves 11 unknowns, so the only short route is the composition | 4 | Built 2026-10-16, key by three routes (symbolic derivation + irreducibility, dessin tracing of all four roots against the figure, PSLQ orbit recognition at 60 digits). Findability: nothing. Screen: Opus 1/1 correct in 10 min and 85k tokens (found the composition from the valencies, counted the quartics by a Hurwitz count, derived a quartic in p^2 via power sums of the critical values, proved irreducibility mod 5); Sonnet 0/1, answered 3 by an invented recollection of a 'known worked example', no computation. Held back |
| task03-matroid-smallest-field | Smallest prime power q over which the rank-3 matroid of a drawn 9-point, 8-line configuration (one 4-point line) is representable. The coordinatisation has a free parameter and no equation; what fails over GF(2), GF(3), GF(4), GF(5) is degeneracy: t must avoid 0, 1, 2, 1/2 and the roots of t^2-3t+1, and over GF(5) the fifth element t = 4 is a root of the quadratic | 7 | Built 2026-10-16, key by two routes (symbolic coordinatisation with full degeneracy list; brute-force search in PG(2,q)). Screen: Opus 1/1 correct in 5 min and 59k tokens (sent the 4-point line to infinity, one parameter c with c^2-c-1, checked GF(2), GF(3), GF(4), GF(5) element by element, explicit GF(7) representation); Sonnet 1/1 correct in 42 min and 104k tokens (frame C, I, B, A, parameter u, same five obstructions). Too easy; held back |
| task05-bandwidth | Bandwidth of a drawn 12-vertex, 20-edge graph. Trivial bounds 3, every Cuthill-McKee numbering 5 to 7, true value 4; certificates: an 8-vertex induced subgraph of diameter 2 (density bound 4) and an explicit numbering of width 4. task04 (treewidth) was abandoned before packaging: at 12 to 14 vertices min-degree and min-fill heuristics find the optimum, so no overshoot trap exists | 4 | Built 2026-10-16, key by two exact methods. Screen: Opus 1/1 correct in 10 min and 85k tokens (did not use the density bound; excluded width 3 by a case analysis on the position of the degree-5 vertex, then found a width-4 numbering); Sonnet 0/1, cut off at the 64k output ceiling with no answer. SUBMITTED 2026-10-16; Summit: Model A 3/3 in 2.5 to 8.5 min, two short lower-bound arguments (the unique diameter-4 pair {7,5} must take the ends; the adjacent degree-5 vertices 1 and 4), width-4 numbering written down directly; returned as too easy. Summit's own suggestion: ask for the number of optimal numberings (6, 3 up to reversal), which no short argument gives. Built as v2-count/ (same figure, key 6, two independent counts, search tree in the notes); screen: Sonnet 0/1 cut off at 64k output tokens; Opus 1/1 correct but only after 46 min and 79k tokens, via a distance-3 graph on the end positions and a six-case analysis, the longest run of the day. Summit verdict on v2: 5/5 as well, the count needs only about five short cases once the ends are forced; the graph is the problem, not the question |
| task05-bandwidth/v3-graphA | Revision of task05 (SUM-MVB7DTW7): bandwidth of the 13-vertex, 22-edge graph proposed by the Summit reviewer after task05 came back 5/5 on v1 and v2: no short lower bound (density bound over all connected induced subgraphs 4, diameter bound 4, degree bound 2), 176 optimal numberings with nine end pairs, Cuthill-McKee 6 to 8; the lower bound needs the exhaustive placement search (1612 nodes) | 5 | Built 2026-10-16, key by two exact methods, reviewer's claims re-verified. Not submitted: the SUM-MVB7DTW7 slot was used on 2026-10-17 by the 16-vertex instance (task06 v3-sixteen). Screen: Opus run 1 correct in 7 min and 71k tokens, by a prefix-boundary chain argument (every prefix of a width-b numbering has at most b outside neighbours; all admissible 2-sets and their extensions die by size 5), a short proof the reviewer's analysis missed; Opus run 3 correct in 10 min by the same lemma applied at k = 6 (the two non-boundary vertices of the first six must have at most 4 neighbours; all twelve such pairs fail on the complement side); Opus run 2 correct in 20 min by a 2-ball argument (an end vertex of a width-4 numbering has at most 9 vertices within distance 2; only 5 and 6 qualify, so the ends are forced and die in two lines). Opus 3/3; Sonnet 0/1, cut off at 64k output tokens. Lesson: the reviewer's filters (density bound, end pairs of OPTIMAL numberings) do not measure what matters; the width-(b-1) impossibility proof is short whenever balls or prefix boundaries force the ends. Next filter: the width-(b-1) search tree must survive deep (dead ends only at depth >= n-3) and every vertex must pass the 2-ball end test |
| task05-bandwidth/v4-deep | Revision candidate for SUM-MVB7DTW7 chosen by the new filter: 14 vertices, 25 edges, bandwidth 5; width-4 search has 2471 nodes with twelve branches surviving to depth 11; density bound 4, diameter bound 4, degree bound 3; six vertices pass the 2-ball end test and 18 pairs the prefix-boundary test, so no two-line end argument exists; 23616 optimal numberings | 5 | Built 2026-10-16, key by two exact methods. Screen: Opus run 3 correct in 21 min by the boundary lemma applied to a 7/7 split (both halves need three interior vertices with closed neighbourhoods inside; only three splits qualify, each killed in a few lines); Opus run 2 correct in 35 min via the four distance-4 pairs that can occupy the ends of a width-4 numbering (ceil(13/4) = 4), each killed by a short case split; Opus run 1 correct in 39 min by the same 7/7 boundary split as run 3. Opus 3/3 (21, 35, 39 min); Sonnet 1/1 correct after 81 min and 139k tokens (misread one edge, gave a width-5 numbering and a hand-waving pigeonhole argument for the lower bound, no proof). Family verdict: four graphs, nine Opus runs, nine solves; at 12 to 14 vertices the width-(b-1) impossibility always has a hand proof via ends, 2-balls, prefix boundaries or a middle split. Stop the bandwidth family |
| task05-bandwidth/v5-crack-growth-pore | ENGINEERING replacement for SUM-MVB7DTW7 after the domain change (owner: use the task05 folder). Summit type 4: self-drawn log-log da/dN plot of MIM Ti-6Al-7Nb at R = 0.1 with a Klesnil-Lukas fit (threshold 4.0 stated) and its Paris asymptote through the gridline points (10, 1e-8) and (100, 1e-5), so C = 1e-11 and m = 3 are read exactly. Text gives the smooth fatigue limit (500 MPa range), the applied range (420 MPa), a 60 um surface pore, Y = 0.65, El Haddad threshold with a0 fixed by consistency. Question: propagation life from the pore to 1.0 mm, two significant figures. Decisive step: Delta K at the pore (3.75) is below the long-crack threshold, so the naive law predicts arrest; a0 = 48 um puts the pore threshold at 2.98, the crack grows, and the integral has no closed form (Simpson in ln a). Wrong routes: pure Paris 1.7e5, long-crack start at 68 um 1.1e6, a0 from amplitude 1.9e5 | 2.3e5 | Built 2026-10-17, key by two routes (quad and Simpson in ln a, 228653 cycles). Screen a (asymptote through the decade crossings (10, 1e-8) and (100, 1e-5), key 2.3e5): Opus 3/3 correct in about 2 min and 45k to 48k tokens each (all read the two decade crossings, derived a0 = 48 um, Simpson in ln a or panel-wise, converged to 2.29e5); Sonnet 1/1 correct too (58k tokens). Far too easy, every step spelled out and the reading trivial. Screen b (anchors (5, 1e-9) and (50, 2e-6), m = 3.30, C = 4.93e-12, key 2.6e5): Opus 3/3 (all used the near-coincidence of the line with the (10, 1e-8) crossing and the right-axis value 2e-5 at 100, m = 3.3, C = 5e-12, N = 2.58e5), Sonnet 1/1 (same reading via the data points at 10 and 20 which sat on gridline crossings). Lesson: any decade crossing or data point near a decade crossing is read exactly. Screen c (anchors on minor gridlines only, (7, 3e-9) and (70, 3e-6), m = 3, C = 8.75e-12, key 2.6e5; stem says the asymptote passes through two gridline crossings; misreads give 2.3e5, 2.0e5, 2.9e5 or 3.9e5): Opus 0/3 (two read the line at (10, 9e-9) and gave 2.5e5, one took the decade crossings and gave 2.3e5), Sonnet 0/1 (read (5, 1e-9), 2.9e5): nobody found the crossings at 7 and 70. Screen d (same figure, stem names the abscissae 7 and 70): Opus 3/3, all read 3e-9 at 7 exactly. Screen e (anchor moved to (7, 7e-9), the crowded top of the decade; stem names 7 and 70; Delta sigma 410, a_f 0.8 mm, key 1.2e5): Opus 3/3, every run cross-checked with the data point sitting at (10, 2e-8) and the line leaving the frame at (100, 2e-5), which a straight asymptote with m = 3 always offers; Sonnet 0/1 (read 6e-9, gave 1.4e5). Screen f (asymptote removed; the curved fit itself passes through (7, 8e-9) and (30, 6e-7), m = 2.809 solved from the ratio 75, C = 4.27e-11; Delta sigma_w 480, Delta sigma 400, pore 50 um, a_f 0.5 mm, key 1.0e5 at 3.1 percent from both bin edges; every one-minor-line misread lands outside the bin; stem names 7 and 30): Opus 3/3 in about 3 min each, all read 8e-9 at 7 and 6e-7 at 30 and solved m by iteration; Sonnet pending. Lesson across c to f: once the abscissa is named Opus reads any minor gridline exactly; without it Opus does not look for the crossing at all. Screen g (figure f, stem says only that the crossings are at two of the labelled Delta K values): Opus 0/3; two runs declared (5, 2e-9) and (20, 2e-7) (curve 9 and 5 percent off those lines) and gave 9.3e4, one declared (10, 3e-8) and (100, 2e-5) (10 and 13 percent off) and gave 8.8e4. With minor lines at every integer the near misses are within a millimetre on the print, so that stem is unfair to a person too. Screen h (rate axis with minor gridlines at 2 and 5 only; curve through (6, 2e-9) and (20, 1e-7), m = 2.959, C = 1.43e-11, every other labelled abscissa at least 17 percent of a step from a line; Delta sigma_w 500, Delta sigma 450, pore 50 um, a_f 0.5 mm, key 1.4e5; stem as g): Opus 0/3 (all three took the true crossing at (20, 1e-7); two then claimed a crossing at (40, 8e-7), a gridline that does not exist on the 1-2-5 axis, and gave 1.5e5; one claimed (100, 1e-5), where the curve is 18 percent above the line, and gave 1.2e5; none looked at 6), Sonnet 0/1 (same (20, 1e-7) and (40, 8e-7), 1.5e5). These misses are model errors a person with the figure would not make (a non-existent gridline, an 18 percent gap), so the version is fair but past the band. Screen i (figure h, stem adds that one of the two crossings lies below 10 MPa m^1/2, which narrows the search to 5, 6, 7, 8 where the curve is 24, 0, 37 and 17 percent from the nearest line): Opus 3/3 (all found (6, 2e-9) and (20, 1e-7), rejected 5 and 8 as near misses, solved m = 2.96 by iteration, 1.41e5). Screen j (figure h, stem says both crossings lie below 30 MPa m^1/2, leaving 10 and 20 as the tempting pair): Opus 2/3 (two found (6, 2e-9) and (20, 1e-7), one of them explicitly rejecting (10, 1e-8) because it would put the curve at 1.9e-5 at 100 instead of the drawn 1.2e-5; the third took (10, 1e-8) and (20, 1e-7), m = 3.25, and gave 2.0e5). FINAL WORDING: this one. Package rebuilt 2026-10-17 with the final stem, zip pore-crack-propagation-life-mim-titanium.zip, pushed to the repo as the task05 replacement. Sonnet probe on the final wording: 0/1 (took (5, 1e-9), where the curve is 24 percent below the line, with (20, 1e-7); m = 2.77, C = 2.5e-11, answered 1.1e5). Final tally on the shipped wording: Opus 2/3, Sonnet 0/1 |
| task06-bandwidth-fourteen | Same family as task05 at 14 vertices and 27 edges: trivial bounds 3 and 4, every Cuthill-McKee numbering 6 to 9, true value 5; certificates: a 10-vertex induced subgraph of diameter 2 and an explicit width-5 numbering | 5 | Built 2026-10-16, key by two exact methods. Screen: Opus 1/1 correct in 8 min and 77k tokens (width-5 numbering, then a window argument around the clique {1,4,11,14} with a short case split); Sonnet 1/1 correct by luck (37 min, misread four edges, no proof of the lower bound). Lesson: a bigger instance did not help, Opus found a different short lower-bound argument |
| task06-bandwidth-fourteen/v2-count | Counting version of task06 (Summit's suggestion on task05): number of numberings of width equal to the bandwidth. The task06 graph has 248 optimal numberings (124 up to reversal), too many for any hand route, so two edges were added (67 and 6-10, 29 edges): bandwidth still 5, degree bound 3, diameter bound 4, Cuthill-McKee 7 to 9, exactly 6 optimal numberings in three structurally different classes (the position of 10 and the 1/11/4 block move). New figure (9 crossings, bends at least 15 degrees) | 6 | Built 2026-10-16, key by two routes (backtracking enumeration, DP count). Hand-checkable structure: the ends must be 2 and 5 (distance-2 ball of an end vertex fits in 11 positions; only 2 and 5 have balls of at most 11), 8 next to 2 and 9 next to 5 by the same count. Screen: Opus 1/1 correct (6) but only after 64 min and 112k tokens, the longest run so far: it found the same distance-2 ball argument for the ends, derived 9 and 12 next to 5 by a count, then split on the vertex x in positions 4 to 7 and listed the three classes; it read a phantom edge 6-13 (30 edges instead of 29) and said so, the count survived it. Sonnet 0/1, cut off at the 64k output ceiling with no answer, as on task05 v2. Same regime as task05 v2 (Opus 46 min, 79k): a single Opus solve at the edge of the token budget, so Summit outcomes are solves or cut-offs; the owner decides |
| task11-renewal-residual-life | Mathematics, probability (renewal theory). Summit type 4 with the plot-reading lever from the Engineering detour: the survival function S(t) = 1/(1 + (t/lambda)^k) of a log-logistic inter-arrival time drawn on log-log axes with a 1-2-5 grid and labels at 1, 2, 3, 5, 10, 20, 30, 50, 100; the curve passes exactly through (2, 0.2) and (5, 0.02) (k = 2.734, lambda = 1.205) and is at least 24 percent of a step from every other crossing at a labelled t. Question: limit of E[residual life]/E[X], two significant figures. Decisive steps: find the two crossings; know the limit is E[X^2]/(2 E[X]) (inspection paradox) and that it needs k > 2; log-logistic moments through the Beta function. Key (k/2pi) tan(pi/k) = 0.9696, independent of lambda. Near misses give 0.65, 0.83, 1.4, 0.98 or an infinite limit; naive 0.5 and 1 | 0.97 | Built 2026-10-17, key by four routes (closed form, quadrature, Beta function, equilibrium density). v1 figure (9 labels, 3 decades, crossings (2, 0.2) and (5, 0.02), near misses 24 percent off or more): Opus 3/3 with the hint 'both at t <= 10' in about one minute each, and Opus 3/3 without any hint (one run also read the tail slope, about -2.74 per decade, as a check on k). Too few decoys, none tempting. v2 figure (16 labels 1 to 100, 4 decades, crossings (5, 0.05) and (30, 0.0005), k = 2.599, lambda = 1.610, key 1.0927 -> 1.1, bin margin 0.85 of the half-width; near misses at 3, 4 and 10 are 17, 14 and 14 percent off; 63 decoy pairs, two of them land in the key bin by luck): screen without hint: Opus 2/3 but both solves came through the lucky pair (4, 0.1) and (10, 0.01), two decade-line near misses 14 percent off that give 1.07 and round to the key; the third run invented gridlines at 1.5 and gave 1.2. Lesson: Opus goes for decade lines at labelled abscissae first, so no decade-line near miss may land in the key bin, and the scan must reject any decoy pair that does. v3 figure (same axes and labels, crossings (6, 0.02) and (20, 0.0005), k = 3.080, lambda = 1.696, key 0.7980 -> 0.80, bin margin 0.60; nearest misses t = 1 and 10 at 16 percent, t = 8 at 17 percent; 43 decoy pairs, none in the key bin; decade lines are crossed between labels only): screen without hint Opus 0/3 (every run invented gridlines that are not drawn: (1, 0.8)+(10, 0.004) gave 0.83, (4, 0.06)+(20, 0.0005) gave 0.83, (2, 0.4)+(10, 0.004) gave 0.77), Sonnet pending. Past the band without a hint, and the misses are model errors (lines that do not exist). Screen with the hint 'one of them t = 6' (the other crossing must then be found among 8 at 17 percent, 10 at 16 percent, 15 at 21 percent and the true 20; (6, 0.02)+(8, 0.01) gives 1.3, +(10, 0.005) gives 0.96, +(15, 0.001) gives 0.74): Opus 1/3 (one run found (6, 0.02) and (20, 0.0005) and gave 0.80; two runs paired 6 with an invented crossing (10, 4e-3) and gave 0.77). FINAL WORDING: this one. Package built 2026-10-17 with the final stem, zip renewal-residual-life-log-logistic.zip, pushed to the repo as task11. Sonnet probe on the final wording: 0/1 (claimed the rate axis carries decade lines only, read (6, 0.01) and (15, 0.001), k = 2.52, answered 1.2). Final tally on the shipped wording: Opus 1/3, Sonnet 0/1. SUMMIT v4 CONSISTENCY CHECK FAILED 2026-10-17 with 5 blocking problems, all fixed the same day: (1) the References field still held the bandwidth text from v1 to v3 because the revision editor will not let it be changed, so this task must go in as a NEW submission by Import .zip, never as another revision of SUM-MVB7DTW7; (2) the stem asked for lambda and k as well as the ratio while the key held only the ratio, so the stem now reads 'reading those two crossings fixes lambda and k' and 'Using the lambda and k fixed by the figure, find ... Give only this number as the answer'; (3) rubric c1 now says 'as the final answer' and c2 calls lambda and k intermediate values; (4) the solution said the third moment does not exist, which was wrong: E[X^r] is finite for r < k and k = 3.080, so E[X^3] = 182.5 is finite and the fourth is the first divergent integer moment (verified by quadrature); (5) verify_key.py claimed the residual-life variance is infinite because k - 1 < 2, also wrong: k - 1 = 2.080 > 2 and the equilibrium variance is 27.341 (verified). The aside was replaced by printed moments. The key 0.80 was confirmed by Summit's own check. Re-screen of the reworded stem (3 Opus): 2/3 correct, one miss paired the named crossing at 6 with an invented crossing (2, 4e-1), where the curve is 12 percent from the nearest line; the rewording did not move the difficulty. Lesson for every future task: never state a moment or variance condition in the notes without computing it, and check the References field after any revision. Sonnet on the same figure without the hint: 0/1 ((15, 1e-3) and (30, 1e-4), 0.73) |
| task06-bandwidth-fourteen/v3-sixteen | Revision of task06 for Summit, replaces the 14-vertex entry field by field: bandwidth of a 16-vertex, 27-edge graph chosen so that no degree, diameter or density bound reaches the answer (all three give at most 4; checked over every connected induced subgraph), the lower bound needs the prefix-boundary chain (57 sets, dies at six vertices, printed in full in the notes), and the optimal numbering is unique up to reversal and heuristics miss it (Cuthill-McKee 7 to 10, annealing 0 of 16, width-5 prefix chain 4455 sets). Expected wrong answer 6 | 5 | Built 2026-10-16 (evening), key by two exact methods plus the written chain proof. Screen: first pass (figure plus stem, no code): Opus cut off at the 64k output ceiling with no answer and no visible text beyond the opening line (the budget went into thinking), the first Opus cut-off in this project; Sonnet cut off the same way. Staged re-screen of Opus (write stages, provisional answer early) running; re-screen attempts with a staged write-up were refused by the model's safeguards (reasoning_extraction flag) twice; a second plain run of Opus answered 5 correctly in 25 min and 103k tokens, with the unique numbering found and a new lower-bound proof (width 4 would put the first four and last four positions at distance 3 or more from each other, a K4,4 in the far graph, and the far graph has no K4). Local tally: Opus 1/2 with one cut-off, Sonnet 0/1 cut-off. First instance in this project where a single Opus run failed outright. SUBMITTED 2026-10-17 about 04:43 as the revision of SUM-MVB7DTW7 (the task05 entry, the only bandwidth entry on Summit; there is no task06 entry there), after an independent exact check of the key from the 27-edge list (width 4: 0, width 5: 2, width 6: 224554). Fields replaced: classification, image, question, answer and variants, solution, rubric, common wrong answers, reference file, explanation box. Known blemish: the read-only 'Legacy reference text' box still carries the 12-vertex wording with 'width 4'. RETURNED 2026-10-17: too easy, Model A 5/5 in 8 to 13 min (93k tokens on run 0), rubric 9.4/10, weaker-model probe passed (85 min, not solved). Model A's route: all 27 edges read; lower bound by the forced-ends squeeze (with width 4 the two end vertices are at distance 4, only four pairs are, {1,5}, {1,16}, {4,14}, {5,10}; a vertex at distance 2 from both ends must sit in position 8 or 9, and each pair has three or more such vertices); upper bound by fixing 1 and 16 at the ends and searching with distance limits. The prefix chain was not needed and fixing the ends shrank the construction search |
| task07-crossing-number | Crossing number of a drawn 10-vertex, 21-edge graph (3-connected, Euler bound useless, skewness 2: only the edge pairs 1-2/6-7 and 1-5/6-7 can be deleted to leave a planar graph, both 19-edge planar subgraphs 3-connected with both missing edges at dual distance 2, greedy insertion gives 4, true value 3, four optimal crossing patterns all with 3-8 crossing 6-7). v1 stem gave no facts and a circular figure; v2 (packaged) gives a clean 4-crossing straight-line figure and states the two planarity facts, so the question is whether skewness 2 means crossing number 2 | 3 | Built 2026-10-16, key by two routes (exhaustive planarization enumeration with networkx; library-free DMP planarity plus the four-pairs argument and an integer straight-line drawing). v1 screen: Opus 0/1 cut off at the 64k ceiling twice, Sonnet 0/1 (2, three edges misread). v2 screen: Opus 1/1 (3, four-pairs argument plus a hand-built 3-crossing drawing, 28 min, 119k tokens), Sonnet 1/1 (3, one edge misread, false upper-bound argument). Held back; erased from the folder on 2026-10-17 by the owner's decision (Mathematics closed), package kept only in the repo history |
| task07-crossing-number (folder reused, Engineering) | Fatigue life from a self-generated log-log da/dN plot at R = 0.1 and R = 0.5 (shape 1 of domains-for-new-task.md): Paris fits through gridline anchors (n = 3, C = 8e-12), closure factor U(0.1) = 0.5 from the factor-2 shift, U linear in R so U(0.3) = 0.75, edge crack a0 = 0.6 mm in a 20 mm plate at 250 MPa range, R = 0.3, SENT polynomial Y, failure at K_max = 60; wrong routes 3.7e5 (R = 0.1 line as is), 4.6e4 (R = 0.5 line), 2.0e5 (Elber's U), 1.3e5 (Y constant) | 1.1e5 cycles (exact 110212, 4.3 percent from the rounding edges) | Built 2026-10-17, key by two routes (scipy quad; mpmath tanh-sinh plus Simpson with Richardson). Screen: Opus 3/3 correct in about 2 min each (45k tokens, anchors read exactly, closure interpolated, u = a^(-1/2) substitution, Simpson), Sonnet 1/1 correct. Too easy; held back. Variant 2 (same figure with closure that disappears above K_max = 20, the R = 0.1 points joining the solid line from dK = 20, K* fixed in the stem, split integral, key 1.3e5, wrong routes 1.9e5 / 1.6e5 / 8e4 / 6.4e5 / 1.4e5): Opus 1/1 correct in 3 min (split at a = 1.097 mm, both stages by Simpson in t = x^(-1/2)). Not pushed; the engineering package was also removed from the repo on 2026-10-17 because it had failed the local screen |
| task07-crossing-number (folder reused again, Biology) | Length of the most parsimonious unrooted tree for a 9-isolate x 18-character binary matrix (presence/absence of gene families), the colleague's task10 shape rebuilt with an own generator: unique optimum 36, 77 trees at 37, four 3-step characters, max compatible set 5 (bound 31), NNI descent 1/40 and stepwise addition 6/40 reach 36, clique trees 37 to 40 | 36 | Built 2026-10-17, key by two routes (exhaustive Fitch over 135135 trees; independent Sankoff DP over bipartitions). Screen: Opus 0/3 and Sonnet 0/1, all four cut off at the 64k output ceiling with no answer. Pure length; not pushed |
| task08-fractional-chromatic-number (folder reused) | Mathematics: smallest covering array avoiding forbidden pairs (chart figure). v1 five ternary columns, seven forbidden pairs, unique optimum; v2 five ternary plus one binary column, ten forbidden pairs, two optima. Earlier contents (fractional chromatic number; engineering versions) archived under work/ | v1 10, v2 10 | Local screens: v1 Opus 3/3 (4.5 to 10 min); v2 Opus 3/3 (2.5 to 5 min), Sonnet 1/1. Family closed: when the bound is a short count, the tight count forces the structure and the unique array follows; six full ternary columns give cut-offs instead. Not submitted |
| task09-pebbling-number | Rooted pebbling number pi(G, r) of a drawn 10-vertex, 14-edge planar graph (diameter 3, 2-connected), target r = vertex 3 double-circled. Bounds n = 10 and 2^3 = 8; the textbook pile-of-seven configurations give 11; the unique failing 12-pebble configuration is five pebbles on each of the adjacent degree-2 vertices 9 and 10 plus one on 4 and one on 7 (7 + 3 on the same pair reaches r). Other targets: 12 or 10, so 3 also realises pi(G) = 13. Full-graph version archived in work/full (cut-offs) | 13 | Built 2026-10-16, key by two exact routes (layer recursion over unreachable configurations; direct search), hand proof of the lower bound via the No-Cycle Lemma with every bound machine-checked, all 590 reachable configurations listed. Screen (rooted, figure plus stem, staged notes): Opus 0/1 (11 in 38 min, linear weight relaxation as a proof), Sonnet 0/1 (10 in 19 min, tree formula as an upper bound), no cut-offs. Full version: Opus 0/2 both cut-offs, Sonnet 0/2 (cut-off, 12). SUBMITTED 2026-10-16 as SUM-MVBG0GO3; returned the same day as too easy: Model A 5/5 (13 to 16 min, about 110k tokens each, rubric 8.2/10), weaker-model probe passed, consistency 0 blocking 1 advisory (not yet read). Route: neighbours of 3 hold at most one pebble in a failing configuration, so the game collapses to the 6-vertex piece {4,6,7,8,9,10}, where the unique failing configuration is guessed and the upper bound is a small hand count. Revision in progress (see the task09 revision section) |
| task09-pebbling-number/v2-thirteen | Revision of SUM-MVBG0GO3 after the 5/5 return. Rooted pebbling number of a 13-vertex, 19-edge planar graph, target 9 double-circled, eccentricity 4, residual piece of 10 vertices after the neighbours-hold-at-most-one reduction. Trivial bounds 16 and 13; one pile of fifteen plus singles stops at 21 (lazy answer 22); 28 failing configurations of 24 pebbles, all with two odd piles, one in each far part (11+11+1+1, 9+3+9+3, 11+1+5+7 and so on) | 25 | Built 2026-10-17, key by two implementations of the layer recursion plus direct search on all 28 maximal failing configurations, their 311 extensions and 60,000 random configurations; lower-bound certificate by exhaustive enumeration of the 61,608 configurations reachable from 11+11+1+1. Screen: Sonnet 0/1 (27 in 39 min), Opus run 1 cut off at 64k output in one reply, run 2 with a one-idea-per-reply protocol pending at the time of the push. Edit sheet paste-for-edit.md for the field-by-field revision |
| task09-pebbling-number/v3-kitagawa-internal-pore | ENGINEERING replacement for SUM-MVBG0GO3 after the domain change (owner: use the task09 folder). Summit type 4: self-drawn Kitagawa diagram of MIM Ti-6Al-7Nb (0.20 wt% O, 320 HV, surface drilled holes, R = -1), eight points generated from the small-defect law 1.43(HV+120)/sqrt(area)^(1/6) and a long-crack branch fixed by the gridline point (640 um, 150 MPa), knee near 220 um. Question: fatigue limit of a component from a 0.38 wt% O, 372 HV lot with an internal pore of sqrt(area) 600 um, same long-crack threshold, two significant figures. Decisive steps: the pore is in the long-crack regime so the hardness drops out, and the internal factor 0.50 replaces 0.65. Wrong routes 150, 230, 260, 240, 220, 170 | 200 MPa (201.4) | Built 2026-10-17, key by two routes (closed form; least-squares fit of the slope -1/2 branch plus regime check). Screen: Opus 3/3 correct in 73 to 132 s and 42k to 46k tokens, every run named both traps; Sonnet 0/1 (210, reading slip on the right route). Not in band; package pushed for the owner's decision |
| task09-pebbling-number/v4-kitagawa-log-reading | Same question as v3 with the one lever left from the Lumiere record: standard logarithmic axes (decade labels, unlabelled minor gridlines at 2 to 9) and the four steep-branch points placed inside the 100 to 200 MPa interval, off every gridline, where linear interpolation on a log axis reads 3 to 6 percent high and gives 210; key fixed at exactly 200.0 MPa | 200 MPa (200.0) | Built 2026-10-17, key by two routes plus the reading-sensitivity table. Screen: Opus 3/3 correct in 62 to 115 s, readings within one percent; Sonnet 0/1 (240). Lever did not bite; not in band |
| task09-pebbling-number/v5-el-haddad-internal-pore | Third Engineering attempt in the task09 folder, on the sibling's crossing lever: El Haddad fit for MIM CP titanium (smooth limit 200 MPa, a0 = 66.7 um) drawn on a 1-2-5 log grid, passing exactly through (200 um, 100 MPa) and (1000 um, 50 MPa) with every other gridline miss at least 15 percent of a step; question: fatigue limit with an internal pore of 200 um, which needs a0 rescaled by (0.65/0.50)^2. Wrong routes 100, 130, 150; wrong crossings 130, 140, 100, 110 | 120 MPa (120.1) | Built 2026-10-17, key by two routes, decoy table in the notes. Screen: Opus 3/3 in 42 to 80 s, Sonnet 1/1. Out of band |
| task09-pebbling-number/v6-sn-haibach | Engineering, built to the sibling's crossing recipe on a new quantity: semi-log S-N curve of MIM Ti-6Al-7Nb (linear stress with 10 MPa gridlines, cycles with 1-2-5 gridlines), Basquin fit through the exact crossings (5e4, 310) and (2e6, 230), k = 12.36, knee at 1e7 with fatigue limit 201.9 MPa; tempting major-line pair (1e5, 290), (1e6, 240) misses by 19 and 24 percent of a step, every other miss at least 14 percent. Question: complete blocks survived under 5000 cycles at 320 MPa plus 5,000,000 at 180 MPa, linear damage with Haibach's extension (exponent 2k-1). Integer answer with 8 percent tolerance, robust to rounding k or the fatigue limit; major-line decoys give 4, Miner original 6, elementary rule 3 | 5 blocks (5.53) | Built 2026-10-17, key by two routes (closed form; numerical reconstruction of the curve with bisection), decoy and rounding tables in the notes. Screen: Opus 2/3 (one wrong, 4, from the misread pair (1e6, 240), (5e6, 210); one right by a benign misread), Sonnet 0/1 (3), no cut-offs, 2 to 7 min. First in-band screen in this folder; candidate for the SUM-MVBG0GO3 replacement, edit sheet paste-for-edit.md |
| task09-pebbling-number/v7-rainflow-miner | Engineering: one period of a 24-reversal stress history on 25 MPa gridlines, rainflow for repeating histories (ASTM E1049, rearranged at the largest peak, all cycles full), Basquin sigma_a = 450 N^(-1/8) stated, linear damage; twelve cycles, damage 0.1296 per period; wrong procedures give 8, 11, 5, 23, 25 | 7 periods (7.72) | Built 2026-10-17, key by two counters (ASTM three-point rule and a four-point algorithm). Screen: Opus 3/3 in 75 to 91 s, Sonnet 1/1. Out of band; the procedure is routine |
| task09-pebbling-number/v8-two-sn-curves | v6 extended with a second S-N curve at R = 0.1 (crossings (2e5, 240), (5e6, 190)) and a three-part block (5000 at 260 R = -1, 10,000 at 250 R = 0.1, 5,000,000 at 180 R = -1); key 7.58 blocks | 7 blocks | Built 2026-10-17. Screen: Opus 3/3, Sonnet 1/1, every run anchoring the curves on their frame ends (1e4, 350), (1e7, 200), (1e4, 300), (1e7, 180), which lie within one percent of the truth. Lesson: curves must not start on the frame and plateaus must sit mid-interval |
| task09-pebbling-number/v9-two-sn-curves-mid | v8 with the free anchors removed: curves drawn from 1.3e4 cycles, plateaus at 163.8 and 126.6 MPa (mid-interval); R = -1 through (1e5, 240), (5e5, 210), k = 12.05; R = 0.1 through (2e4, 200), (1e6, 150), k = 13.60; block 20,000 at 220 (R = -1), 10,000 at 170 (R = 0.1), 2,000,000 at 140 (R = -1, Haibach); nine of ten tempting misreads give 8, elementary rule 6; integer robust to rounding either exponent by 0.05 or either limit to a neighbouring line | 7 blocks (7.68) | Built 2026-10-17, key by two routes. Screen: Opus 1/3 (two runs took (2e4, 280), (1e6, 200) and (1e5, 180), (1e6, 150), answered 8; one run exact), Sonnet 1/1 (by a misread that stayed inside the integer), no cut-offs, 3 to 5 min. Strongest tally in this folder; candidate for the SUM-MVBG0GO3 replacement, edit sheet paste-for-edit.md |
| task09-pebbling-number/v10-fourteen | Mathematics again (the account offers only Mathematics, confirmed by the owner 2026-10-17; the Engineering versions v3 to v9 cannot be submitted). Revision of SUM-MVBG0GO3 built to the verdict's four demands plus a new proxy: rooted pebbling number of a 14-vertex, 20-edge planar graph, target 1 of degree 2 and eccentricity 4, residual piece 11 vertices; a far part {7,9,12,13,14} joined to the rest through two edges and a pocket {4,10,11} with 11 of degree 2 at distance 3. Trivial bounds 16 and 14; one pile plus singles stops at 22 (lazy answer 23); two piles stop at 25 (fifteen on 7, seven on 11, singles on 12, 13, 14; answer 26); the 20 failing configurations of 26 pebbles all need three or more piles (seven on 11 plus nineteen in the far part in twelve shapes: 15+3+1, 13+5+1, 11+5+3, 9+5+5, 7+7+5, ...). First instance found with pi - T2 >= 1 (one hit in about 250) | 27 | Built 2026-10-17, key by two implementations of the layer recursion, direct search on the 20 maximal failing configurations and their 253 extensions, 60,000 random configurations, enumeration of the 187,805 configurations reachable from 15 on 7, 7 on 11, 3 on 14, 1 on 13 (at most one pebble ever arrives at 2 and at most one at 3). Detector clean. Screen: pending (3 Opus, 1 Sonnet, notes-file protocol) |

## Session 2026-10-16: first Mathematics candidate, dessins d'enfants (task01)

Direction chosen: Galois theory of plane trees (Shabat polynomials). The decisive step is structural
(the tree is a composition of two smaller trees, so its monodromy group is imprimitive and the polynomial
is Q(R(x)) with cubics over Q), the hand route after the insight is a few lines, and without the insight
the degree-9 system is out of reach. The question asks for an exact value (leading coefficient 1/256 under
a two-vertex normalisation) rather than for the field degree, because "1" or "2" can be guessed.

Tools built, all in tasks/task01-plane-tree-field-of-moduli/work (venv python):
- trees.py: enumerates bicoloured plane trees with n edges up to isomorphism (ordered trees, canonical
  form by BFS relabelling), passports, automorphism count, monodromy group order and primitivity
  (sympy), mirror symmetry. Counts: n=7 63 trees, n=8 190, n=9 546, n=10 1708. Output trees{n}.txt.
- shabat2.py / shabat3.py: numerical Shabat polynomials for a whole passport (Newton from random starts
  and from planar-layout starts, b0 = 1 normalisation, then canonical rescaling by the first non-zero
  power sum of the white vertices), dessin tracing (follow the arcs P real in [0,1] from each white
  vertex) to identify which tree a solution belongs to, mpmath refinement.
- recog.py: Galois orbits by finding the smallest subset of solutions whose coefficient-wise elementary
  symmetric functions are rational (150 digits, PSLQ). Validated on the Lando-Zvonkin degree-7 example
  (passport 4,2,1 | 2,2,1,1,1: PSL(2,7) pair quadratic, A7 pair quadratic).
- draw.py (radial layout honouring cyclic orders, with a check that re-derives the permutations from the
  coordinates) and draw_figure.py (hand-placed coordinates for the final figure, same check).
- verify_key.py at the task root: standalone, embedded in reference.txt.
Traps met: Newton from random starts misses trees with small basins (the composite tree was found only
from starts near its true geometry); a tree with a rotational automorphism has vanishing white-vertex
sum, so the canonical scaling must fall back to a higher power sum; killing background python jobs with
pkill -f or ps|grep kills the calling shell too (use ps -eo pid,comm,args and filter on comm == python).

Field results so far (degree 9): passport (6,1,1,1 | 2,2,2,1,1,1): the Z/3-symmetric tree is over Q, the
three S9 trees form one cubic orbit (so a mirror-symmetric tree can sit in a cubic orbit with a conjugate
pair: "real tree, so alone" is a false inference). Passport (4,2,1,1,1 | 2,2,2,2,1): the composite tree is
over Q, the three A9 trees form a cubic orbit. Passport (4,2,1,1,1 | 4,2,1,1,1): 16 trees, the composite
one (Q(Q(x)) with Q = 3x^2 - 2x^3) over Q, the other 15 presumably one orbit (15 found, one solution
still missing). A batch over every degree-9 and degree-10 passport containing a decomposable tree is
recorded in work/recog_*.txt for future tasks.

Lesson from the v1 screen (decisive for this family): the derivative of a Shabat polynomial is fixed by the
valencies, P' = n c prod (x-a_i)^(alpha_i - 1) prod (x-b_j)^(beta_j - 1), so both models bypass any composition
insight and solve the system directly when one side of the passport is "square times linear" (here P - 1 =
c(x-1)Q^2 made Q linear in one parameter and left a quartic in r). A rational answer is then found by the
rational root test, and Sonnet even picked the root by "the tree is mirror-symmetric so the root is real".
Two consequences: a tree over Q is not safe in this family; and the chirality of a chiral tree is the one
step that this derivation does not settle, since conjugate roots give mirror images. v2 uses exactly that.

Batch over the degree-9 and degree-10 passports that contain a decomposable tree (work/recog_*.txt; the
solver misses some solutions, so a passport with fewer solutions than trees is incomplete): complete and
useful results are (6,2,2 | 2,2,1^6): the two mirror-symmetric decomposable trees with group order 14400 form
one real quadratic orbit, the 7200 tree and the Aut=2 tree are over Q; (6,1,1,1,1 | 2,2,2,2,1,1) and
(6,1,1,1,1 | 3,3,1,1,1,1): the chiral pair is quadratic, the symmetric decomposable tree over Q; (8,1,1 | 2,2,1^6):
three primitive trees in a cubic orbit, the Aut=2 tree over Q; (4,3,3 | 2,2,1^6): same pattern, cubic plus Q;
(4,2,2,1,1 | 3,3,1,1,1,1): the two Aut=2 decomposable trees form a quadratic orbit, the 14 others unresolved.
The (6,2,2) passport is the one to use for a decomposable tree with an irrational answer: P = R^2 with R a
quintic, the decomposition is visible from the even black valencies, but the answer lives in a real quadratic
field, so the rational-root shortcut fails and the derivative identity leaves a genuine small system.

Family verdict after three variants (2026-10-16): Opus 5.5 solves Shabat-polynomial questions on trees of 9 to 12
edges on the first attempt, by three different routes (derivative identity plus rational root; derivative
identity plus chirality from edge directions; composition plus Hurwitz count plus power sums of critical values).
Each solve costs 50k to 85k tokens, so at Summit the realistic outcomes are 5/5 or cut-offs, neither in band.
Do not build more dessin tasks at this size. The ingredients that would be needed and were not found: a question
whose only short route is a judgement no computation can replace, or an instance whose hand computation stays
under ~20k tokens while the model's first instinct is wrong.

Matroid representability (task03) verdict: a one-parameter coordinatisation with a degeneracy check is a
standard routine for both models; Opus 1/1 in 5 min, Sonnet 1/1 in 42 min. The "small field runs out of
elements" trap did not bite. If the family is reused, it needs at least two free parameters with a non-trivial
incidence equation, which pushes the hand computation toward the token ceiling and the "unfair" verdict.

Day summary 2026-10-16: four packages built (task01 v1/v2, task02, task03), all keys verified by two or three
routes, every one solved by Opus on a single run (5 to 10 min, 50k to 85k tokens). Sonnet failed two of four.
What has not been tried in Mathematics: a hard-to-find construction with a short certificate at a size just
beyond hand reach (the shape of the archive's accepted task08). Everything computational at "small instance"
size is inside Opus's reach.

Ideas kept for later tasks in this family: (a) a decomposable tree whose inner factor has a quadratic
field, asked as an exact algebraic value; (b) the "real tree in a cubic orbit" trap, but only if a
hand-reachable route exists; (c) degree 10 with 2 x 5 blocks (P = Q(R), Q quadratic, R quintic).

## Session 2026-10-16 (evening): task06 counting version (v2-count)

Continuation of task06 after the task05 return. The lever Summit named for task05 (count the optimal
numberings) was tested on the task06 graph first: 248 numberings of width 5, 124 up to reversal, so the
question would be a long search and nothing else (the "unfair" shape). Searched single and double edge
additions to the 27-edge graph (scratchpad t06count/search_add.py, search_pairs.py): a single added edge
gets the count down to 8 at best (5-10, 9-10 or 10-12), but those 8 are one numbering times two
independent swaps (7/8 and 6/14) times reversal, which a solver can read off after finding one numbering.
Pairs that keep diameter 4 (the diameter bound must stay below the answer) and maximum degree 6: many
give count 2 (unique up to reversal, guessable), a few give 4, and 67 plus 6-10 gives 6 in three classes
that differ in structure, like task05 v2. That pair was taken.

Figure: the parent layout plus the two edges had 18 crossings, so the drawing was redone by simulated
annealing over positions (work/layout_search.py, layout_refine.py, layout_refine2.py: crossings plus
penalties for vertex distance under 0.32, edge-to-vertex clearance under 0.2 and two-edge paths bending
less than 25 degrees). Result 9 crossings, smallest bend 15 degrees; the first draft had 1-11-13 almost
straight, which reads as a single edge, hence the bend penalty. Lesson: check near-collinear paths in
every graph figure, not only crossings and label overlap.

Solution structure (new, hand-checkable, and put into the notes so the consistency check has a written
argument rather than only the program): a vertex in position 1 has its whole distance-2 ball in positions
1 to 11; the ball sizes are 9 (vertex 2), 7 (vertex 5) and 12 to 14 for every other vertex, so the ends
are 2 and 5. With 1 in position 2, thirteen vertices are forced into positions 1 to 12, so 8 is in
position 2. The vertex in position 13 has its ball plus vertex 5 inside twelve positions, which leaves
only 9. The rest (1 in position 4 or 5, 3 in 7, 6 in 8, 12 in 12, three arrangements) is the finite check,
with the enumeration and an independent DP count in verify_key.py. The window argument from task05 v2
(H fills 10 or 11 consecutive positions) does not by itself force the ends, because the window may start
at position 1; the first draft of Step 3 said it did and was corrected before packaging.

Also fixed in the parent task06 package while here: the image-necessity text said "the twenty edges"
(copied from task05) and the References text said "numbering of width 4"; both rebuilt, zip refreshed,
README screen section filled in. Repo clone updated (v2-count folder, zips/, README table, link and
References text); commit and push pending the owner's token.

Verdict context learned after the screen, from the task05 v3 row written by the sibling session: task05 v2
(the 12-vertex counting version, key 6) came back from Summit 5/5, and the reviewer proposed a 13-vertex
graph instead (v3-graphA). task06 v2-count is the same counting shape one size up; the local Opus solve
took 64 min and 112k tokens, longer than task05 v2's 46 min, but the route (ball counts for the ends, then a
small split) is the same kind of short argument, so a 5/5 or cut-off outcome is the likely Summit result.
Hold it unless the owner wants a second calibration point on the counting shape.

Sibling sessions on 2026-10-16 evening built tasks/task07-crossing-number, tasks/task07-fractional-chromatic-number
(mirrored to the repo as task08-fractional-chromatic-number, key 13/4) and tasks/task09-pebbling-number;
none of them is in the task log above yet, and two folders share the number 07.

## Session 2026-10-16 (evening): graph pebbling, task09

New mechanism, not tried before in this account: the pebbling number (Chung 1989). A pebbling move takes two
pebbles off a vertex and puts one on a neighbour; pi(G, r) is the least k such that every configuration of k
pebbles reaches r, pi(G) the maximum over r. Why this family: the retrievable toolkit is weak (lower bounds n,
2^diam, the "7 on the farthest vertex plus singles" template; exact values only for named families: paths,
cycles, cubes, trees, diameter-2 graphs with the Clarke-Hochberg-Hurlbert characterisation, split graphs), the
upper bound cannot be proved by hand for an irregular graph, so a model answers with the best unsolvable
configuration it finds, and the answer is a construction. Linear weight arguments (sum of c(v) 2^{-d(v,r)})
are the natural tool and they are wrong here because the game is integral: this is exactly how Opus failed.

Tools in tasks/task09-pebbling-number/work (venv python): pebble.py (exact pi(G, r) by growing the layers U_k
of unreachable k-pebble configurations, each U_k a subset of U_{k-1} plus one pebble; C_4..C_8, Q3, Petersen
reproduced), search.py (random planar 2-connected diameter-3 graphs from Delaunay triangulations, n = 9 to 11,
six seeds, 3600 graphs, 1056 with pi >= n+2: a gap of two or more over n is the normal case for sparse graphs,
so the gap is not the lever), analyse_hits.py (the lever: graphs where the obvious targets, degree 2 and
eccentricity 3, have a smaller rooted value than the true worst target; 40 such graphs), look.py (per-target
maximal unreachable configurations), routeB.py (independent direct search), reach.py / dpmax.py / acyclic.py
(the certificate facts for the hand proof), draw_figure.py (hand-placed planar drawing).

Instance (seed 1, trial 375, relabelled): 10 vertices, 14 edges 12 13 16 23 28 35 46 47 57 67 69 78 8-10 9-10,
planar, 2-connected, diameter 3. Rooted values: 13 at vertex 3 (degree 3), 12 at 1, 2, 4, 5, 9, 10, 10 at
6, 7, 8. The single unreachable 12-pebble configuration for target 3 is five pebbles on each of the adjacent
degree-2 vertices 9 and 10 plus one on 4 and one on 7; the same twelve pebbles split 7 + 3 on the pair do
reach 3. Key verified by two routes (layers; memoised direct search over all 203,490 13-pebble configurations
per target and all 125,970 12-pebble configurations for target 3). Hand proof of the lower bound written with
the No-Cycle Lemma (Milans and Clark 2006): first neighbour of 3 to hold two pebbles, then a counting
argument on the pair {9, 10} and on {4, 6, 7, 8}; every bound used in it (at most 3 arrivals at 6 and 8, at
most 2 at 7, no pebble re-enters the pair, at most 4 leave it) was checked by enumerating all 206 acyclic
move sequences, and all 590 reachable configurations are listed in reference.txt. Findability: nothing.

Two stems were screened (figure plus stem only, one Read of the figure, no code):
- Full version, "find pi(G)": Opus cut off at the 64k output ceiling twice (plain and with a staged notes
  protocol, the second after 48 min), Sonnet cut off once and answered 12 once (24 min, 172k tokens: degree-2
  targets only, pile of seven plus singles). Opus 0/2, Sonnet 0/2, three of the four runs cut-offs. Archived
  in work/full/ with its own package; not shipped, because Summit tags cut-offs as "unfair" (archive, task06 v2).
- Rooted version, "find pi(G, r)" with r = 3 double-circled in the figure: Opus answered 11 after 38 min and
  91k tokens, no cut-off, wrong: it reduced reachability to "amass four pebbles on one of 6, 7, 8", built
  10-pebble unreachable configurations with a pile of seven on 4, and "proved" that no 11-pebble configuration
  fails by adding the three weight functions W_6, W_7, W_8 (a linear relaxation; the true maximum is 12 and
  needs the 5 + 5 split). Sonnet: answered 10 after 19 min and 79k tokens, no cut-off, wrong (it used the
  Chung tree formula on the BFS spanning tree as an upper bound). Tally Opus 0/1, Sonnet 0/1, no cut-offs.
  Shipped as task09 (zip graph-rooted-pebbling-number-ten-vertices.zip).

Lessons. (1) The full pebbling number of a 10-vertex graph costs Opus more than 64k output tokens of hand
search over targets; a rooted question keeps the decisive step and cuts the volume. (2) The failure mode is
the one predicted for the family: a linear weight argument presented as a proof of the upper bound. (3) The
staged notes protocol (agent keeps a notes file so its reasoning spans several replies) is the way to screen a
long question locally; a single reply dies at 64k. (4) Instances where the worst target is not a degree-2
vertex exist in about one of 25 random sparse planar graphs; keep analyse_hits.py for a second instance with
a different framing if this one lands in band.

## Session 2026-10-16 (night): a hard bandwidth instance, task06 v3 (first built as task10, moved under task06 at the owner's instruction)

Verdict (2026-10-17, same day): too easy, Model A 5/5, 8 to 13 minutes each. The short lower bound that was
missed: with width w the two end positions differ by n-1, so the end vertices are at distance at least
ceil((n-1)/w); here w = 4 gives distance 4, and only four pairs of vertices are that far apart. Fix such a pair
at the ends and every other vertex x is confined to positions between n - w d(x, end2) and 1 + w d(x, end1);
vertices at distance 2 from both ends get two positions (8 and 9), and each of the four pairs has three or
more of them, so width 4 dies in a few lines. The same forced-ends shortcut killed task05 v1 and v2. It also
shrinks the construction: with the ends fixed, the width-5 search is small, which is how Model A found the
unique numbering in ten minutes despite the 4455-set chain. Lessons, in order: (1) before trusting a prefix
chain, run the forced-ends squeeze: list the pairs at distance >= ceil((n-1)/(b-1)), and for each pair check by
matching whether the distance intervals admit a placement at all; if no pair survives, the instance has a short
proof and goes out; (2) the ends must not be forced, so the graph needs many far-apart pairs (small diameter
relative to n) and then the lower bound must come from somewhere else; (3) the construction must stay hard
even with ends fixed, so measure the fixed-ends search tree, not only the free prefix chain; (4) 16 vertices
is inside Model A's hand-search range, so the next instances go to 18 to 22 vertices.

Round 4 and 5 of the generator (2026-10-17, after the return). The squeeze test was added (gen3.py, gen4.py)
and it rejects the returned 16-vertex instance at once (4 far pairs, none placeable). The first 20-vertex
candidate that passed the loose filter (candE: 34 edges, bandwidth 6, 32 optima, annealer 0/12) turned out
to have the same weakness in longer form: 13 of its 16 possible end pairs die by a one-line Hall block and the
other 3 in under 64 search nodes. Reason: the squeeze intervals have slack w*diam - (n-1) with w = b-1, and
that slack was 1 (16 vertices: 4*4-15; 20 vertices: 5*4-19), so a far pair pins every vertex to one or two
positions. Sizes with slack: 22 vertices, bandwidth 6, diameter 5 give 5*5-21 = 4. gen5.py now requires
slack >= 3, at least 5 live end pairs for width b-1, and a fixed-ends search of at least 20000 nodes to
exclude width b-1, on top of the old tests. The v4-twenty folder holds candE with a full verify_key.py (its
end-pair proof is written out, 16 cases) as a fallback, not as a submission.

task06 v5-branching (2026-10-17): bandwidth abandoned for good after round 5. Rounds 4 and 5 showed the trade-off
in numbers: when the squeeze has slack the instance has hundreds of optimal numberings and a long annealer finds
one (21 vertices, bandwidth 7: 9 of 24 runs); when the optimum is rigid the squeeze or a short fixed-ends search
closes the lower bound. Every bandwidth design is a search problem, which the owner's rule ("difficulty from one
decisive step, not from length") excludes anyway. New design in the same task folder: Galton-Watson process with
negative binomial offspring, parameters read from a figure, question E[T | extinction] (decisive step: conditioned
on extinction the process is subcritical with offspring pgf f(qs)/q and mean f'(q)). Two figures screened:
- linear plot of f(s) on [0, 1] with a 0.1 grid, exact crossings (0, 0.4) and (0.4, 0.5), key 1.911: Opus and
  Sonnet both 1.9 within half a minute; a linear grid shows exact crossings at a glance.
- offspring pmf p_0..p_9 as stems on a log axis with 1-2-5 gridlines, exact p_0 = 0.5 and p_7 = 0.02, decoys 12 to
  35 percent off, key 1.838: Opus 1.83 and Sonnet 1.84, both correct; Sonnet measured pixel rows (715 px per decade)
  and read every point to 1 percent. Discrete markers are far easier to read than a continuous curve at labelled
  abscissae, so the task11 lever does not transfer to point plots.
The conditioning step itself is textbook for both models. Verdict: this family is solved; kept in
v5-branching/ (work/v1-linear holds the first figure and its three-route verifier) and not packaged.

Submission note (2026-10-17): Summit has no task06 entry, so the owner revised SUM-MVB7DTW7 (the task05 entry,
the only bandwidth question on the account) with this package, which also avoids a duplicate-check hit from a
second bandwidth task. Lesson for the README of any revision: name the Summit entry id, not the local task
number. The platform keeps a read-only 'Legacy reference text' box with the previous references wording;
it cannot be edited and here it still says 'width 4', so the new References text has to be the one that
states the answer clearly.


After task05 v1 and v2 came back 5/5 and the counting version of task06 screened as a single long Opus
solve, the design changed from "more vertices" and "count instead of value" to the shape of the archive's
accepted task08: a construction trap measured by a proxy before screening, no retrievable lower bound, an
instance just beyond hand reach. Random search over 16 and 18 vertex graphs (scratchpad hard/gen.py,
gen2.py, eval.py, copies in task06-bandwidth-fourteen/v3-sixteen/work): for each graph the exact bandwidth b (backtracking with per-vertex
room pruning, prefix-boundary pruning and the must-place-now rule; 1 to 3 s at 16 to 18 vertices), the easy
bounds, Cuthill-McKee from every start, the number of optimal numberings and the hit rate of a long simulated
annealing over 16 restarts. Two lessons from the first pass: a weak annealer makes every instance look hard
(the first filter passed 101 of 96 tried), and the "ball" density proxy is usually just the diameter bound;
the second pass demanded all easy bounds <= b-1, at most a handful of optimal numberings and at most 3 of 16
annealing hits. Candidates: A (16 vertices, 28 edges, unique optimum, 1 of 16 hits, but a 14-vertex
diameter-3 subgraph gives the density bound 5, a short certificate); B (16 vertices, 27 edges, unique
optimum, 0 of 16 hits, no density bound above 4 anywhere, width-4 chain 57 sets, width-5 chain 4455 sets);
C (17 vertices, 8 optima, 3 of 16). B was taken as task06 v3; A and C are kept in v3-sixteen/work as candA.pkl,
candC.pkl with their figures.

Why this shape should separate: the width-4 exclusion is a 57-set chain, the kind of argument Opus found on
its own for the reviewer's 13-vertex graph in 7 minutes, so the lower bound is fair and reachable; the
width-5 construction has no such short route (4455 prefix sets, no level structure of width 5, every BFS
numbering 7 or worse), so a solver that cannot find the unique numbering reports its best construction, 6.
A bug met on the way: the must-place-now rule compared positions with the unplaced marker -1, which made
every search return False; caught on P4 and C5 before any instance was trusted.

The prefix-boundary chain, as printed by verify_key.py, is the written lower-bound proof Summit's consistency
check asks for; it replaces the "search tree with dead branches" of the earlier bandwidth notes and is
shorter to check by hand.

## Session 2026-10-16 (evening) and 2026-10-17: crossing number, task07

Mechanism not tried before on this account: a topological invariant (crossing number) where the cheap bounds are all
useless (Euler bound negative, skewness 2) and the exact value needs a certificate on each side. Generator
(work/gen.py, crossing.py): random 3-connected graphs on 9 or 10 vertices, degrees 3 to 5, filtered for skewness 2
and crossing number 3 by exhaustive planarization enumeration (every set of k independent edge pairs, every order of
crossings along an edge, planarity of the planarized graph; validated on K5, K3,3, Petersen, K6, K3,4, K4,4). About
220 hits in 40 minutes on 7 cores; ranking (analyze3.py) by: every maximum planar subgraph 3-connected (unique
embedding, hand-checkable), both missing edges at dual distance 2 in it (greedy insertion overshoots to 4), few
maximum planar subgraphs. Chosen instance: 10 vertices, 21 edges, two planar pairs only, four optimal crossing
patterns, all with 3-8 crossing 6-7. Independent route B: DMP planarity written from scratch (agrees with networkx
on 3000 random graphs), faces of the planar subgraphs, straight-line drawings checked by integer orientation tests.
The lower bound has a three-line proof once the planar pairs are known: a two-crossing drawing gives four distinct
pairs whose deletion is planar (one edge from each crossing, four ways), but only two exist.

v1 (stem without facts, figure with vertices on a circle, 32 crossings): Opus cut off at the 64k output ceiling
twice with no answer (8 reads of the figure in run 2, the rest spent on embeddings), Sonnet answered 2 after
misreading three chords. The owner's verdict: that is length, not reasoning (instruction.md, difficulty target).
v2 (packaged): clean straight-line figure with four crossings (work/layout4.py: annealed layout with clarity
penalties, chosen so that moving one vertex gives the three-crossing drawing), and the stem states the two facts
(no single edge deletion is planar; exactly the pairs 1-2/6-7 and 1-5/6-7 are). Then the question is the one
decisive step, skewness 2 versus crossing number 2, with wrong answers 2 (trust the skewness) and 4 (trust the
figure). Screen v2: Opus 1/1 (3, 28 min, 119k tokens: four-pairs argument, then a three-crossing drawing built by
hand), Sonnet 1/1 (3, 31 min: four-pairs argument, upper bound by a false claim). Both solved.

Family verdict: the crossing number of a small graph has no middle ground for Summit. Without the planar-pair facts
the lower bound is a 210-subgraph enumeration that nobody does by hand, so the models burn the budget (cut-offs,
the unfair verdict). With the facts the lower bound is a three-line deduction and the upper bound is squeezed
between it and the drawn figure, so even Sonnet lands on 3 without a valid construction. A counting question
(how many optimal crossing patterns, or which pair crosses in all of them) would need the full enumeration
again. Do not build more crossing-number tasks unless a short, non-obvious lower-bound argument exists that is
not simply handed over in the stem (for instance a counting bound over edge-disjoint Kuratowski subgraphs that
is tight only after a non-trivial choice of subgraphs). Package kept in tasks/task07-crossing-number and in the
repo; the owner decides.

## Session 2026-10-17: task09 revision (v2, 13 vertices) after the 5/5 return

Summit returned task09 (SUM-MVBG0GO3) as too easy: Model A 5/5 in 13 to 16 minutes and about 110k tokens,
rubric 8.2/10, weaker-model probe passed. Every rollout used the reduction "a failing configuration has at
most one pebble on each neighbour of r", which leaves the 6-vertex piece {4,6,7,8,9,10}, guessed the unique
failing configuration (two piles on the adjacent pair 9-10) and closed the upper bound by a short hand count.
The local screen (Opus 0/1 with answer 11, Sonnet 0/1) did not predict this; a single local run is not a
calibration for Summit's five.

Revision rules taken from the verdict: keep the rooted question (the full pi(G) version cut off), move the far
side to distance 4, make the residual piece 9 to 10 vertices, and want many failing configurations that are
not one obvious pile. Tools in tasks/task09-pebbling-number/work/rev: pebble2.py (layer recursion with
integer-encoded configurations, 5 bits per vertex, pruned by the neighbour lemma; 1 to 4 s per target at
n = 13), search2.py (random planar 2-connected graphs, n = 12 to 14, targets of eccentricity 3 or 4 with
residual piece >= 9; about 2,100 graphs, 373 hits with pi >= bound + 2 and >= 8 maximal failing
configurations), eval_hits.py / layers.py (template bounds T1 = largest failing configuration with one pile
plus singles, T2 = with two piles), look2.py, draw_cand.py, relabel.py.

Finding: at eccentricity 4 the template "15 on the far vertex plus singles" is itself among the maximal
failing configurations for most graphs (the lazy route hits the key), so the gap over the trivial bound is
not the lever; the lever is pi - T1 >= 2, which holds for about one hit in forty. Chosen: seed 11 trial 2,
target of degree 2 and eccentricity 4, n = 13, m = 19, pi = 25, T1 = 21 (lazy answer 22), T2 = 24, 28
failing configurations of 24 pebbles, all with two odd piles, one in each far part (the pentagon 1-2-4-5-3
and the triangle chain 7-10-12-13), joined only through the middle {4,5,7,8}: 11+11+1+1, 9+3+9+3, 11+1+5+7,
10+2+3+9 and so on. Relabelled by position, target 9, folder tasks/task09-pebbling-number/v2-thirteen.

Verification (verify_key.py, 5 minutes): Route A (pruned integer layers) and Route B (plain tuple layers,
independent code) agree on all 26 layer sizes; direct search confirms the 28 maximal failing configurations
and their 311 one-pebble extensions, and 60,000 random configurations of sizes 23 to 25 agree with layer
membership; the configuration 11+11+1+1 has 61,608 reachable configurations, none with a pebble on 9, with
at most 3 pebbles ever on 5 and on 8. The written lower-bound argument in the solution is the reduction
(two moves 5->6 or 8->11 needed) plus the counting of what each far part can deliver; the formal proof is
the enumeration, embedded with the program. A full acyclic case analysis like task09 v1's was not written:
over all sequences the far parts can deliver 4 pebbles into the middle (re-entries), so the clean "at most
3" statement holds only for acyclic sequences and the piece is too large for a short hand proof.

Screen v2 (figure plus stem, staged notes): Sonnet 0/1, answered 27 after 39 min and 190k tokens (believed a
26-pebble configuration fails). Opus run 1: cut off at the 64k output ceiling in one reply, no answer; run 2
with a one-idea-per-reply protocol launched 2026-10-17 00:10, result to be added here.

Lessons. (1) Opus writes one reply of more than 64k tokens on this family whenever the piece is bigger than
task09 v1; local screening needs the strict one-idea-per-reply protocol, and a local cut-off says nothing
about Summit's 110k-token runs. (2) Summit's 5/5 on v1 means a single local Opus failure is not evidence of
difficulty; the structural proxy (pi - T1, size of the residual piece, number and spread of maximal failing
configurations) is the better predictor and is now computed for every candidate. (3) The lazy template at
eccentricity 4 is "2^4 - 1 on the far vertex plus singles"; a usable instance must have that template at least
two below the key, which is rare (about 1 in 40 hits).

## Session 2026-10-17: back to Mathematics, task09 v10 (14 vertices, three-pile failing configurations)

The owner reported that the account offers only the Mathematics category, so the Engineering versions
v3 to v9 in this folder stay as records and the SUM-MVBG0GO3 revision has to be a pebbling instance.
Summit's verdict on v1 asked for a target at distance 4, a residual piece of 9 to 10 vertices and many
spread failing configurations; v2 (13 vertices, key 25) has all three but its two-pile template already
reaches the key (T2 = 24, answer 25), so a solver who tries "fifteen on one far vertex, odd piles on two"
lands on the key without the hard step. New proxy for this family: pi - T2 >= 1, where T2 is the largest
failing configuration with at most two piles. Over the 243 evaluated hits of the search (seeds 11 to 17)
exactly one instance has it: seed 13 trial 11, n = 14, m = 20, pi = 27, T1 = 23, T2 = 26, 20 failing
configurations of 26 pebbles in 12 shapes, every one with three or more piles. Relabelled by rows and
drawn with the layout relaxed and nudged (no crossings, no two-edge path straighter than 162 degrees),
target 1 double-circled; folder v10-fourteen, package graph-rooted-pebbling-number-fourteen-vertices.zip.

Structure (new labels): target 1 with neighbours 2 and 3; left part L = {7, 9, 12, 13, 14} attached only
through 9-5 and 13-8; pocket {4, 10, 11} on the right with 11 of degree 2 at distance 3. Every maximal
failing configuration has seven on 11 and nineteen pebbles in L. The solution's configuration is fifteen on
7, seven on 11, three on 14, one on 13: the three on 14 with the one on 13 are a second small pile whose
single output pebble is stranded, which is exactly what the two-pile pattern cannot see. Verification took
four minutes (Route A 77 s, Route B 91 s, certificates 60 s); the move-count DP over the 187,805 reachable
configurations shows at most one pebble ever arrives at 2 and at most one at 3, which is the clean written
form of the lower bound. Decoys: 26 (two-pile pattern), 23 (one pile), 16, 14, 25, 28.

Further searches (seeds 18 to 21, 30 trials each) were launched for an instance with pi - T2 >= 2; the
evaluation runs in work/rev/eval2.py and writes to evaluated.json. One curiosity from seed 18: a 13-vertex
graph with pi(G, r) = 30 at eccentricity 4 and a unique maximal failing configuration, not usable here
(one configuration, nothing spread) but worth a look for a later instance.

## Session 2026-10-17: Engineering, Kitagawa diagram with an internal pore (task09 v3)

Owner's instruction: drop the pebbling revision, build an Engineering task in the task09 folder. Shape 1 of
domains-for-new-task.md (crack growth) was already taken by the sibling sessions (task05 v5, task08), so
shape 2 was built: a Kitagawa diagram generated from Murakami's model, with the expert decisions being the
regime of the component's pore (long-crack, so the hardness lever is a decoy), the hardness independence of
the long-crack threshold (stated as an assumption to keep the stem unambiguous) and the internal-defect
factor 0.50 against 0.65. Folder tasks/task09-pebbling-number/v3-kitagawa-internal-pore (verify_key.py,
draw_figure.py, build_package.py, paste-for-edit.md, zip kitagawa-internal-pore-titanium.zip).

Screen: Opus 3/3 in about 1 to 2 minutes and 42k to 46k tokens; every run fitted both branches, checked the
small-defect branch against 1.43(HV+120), took the threshold from the gridline points, applied 0.65/0.50, ran
the regime check and said the hardness drops out. Sonnet 0/1 by a reading slip. Same outcome as the sibling's
crack-growth shape (Opus 3/3). Lesson for the domain: any engineering question whose solution is "identify the
standard model from the figure, apply its named constants" is a formula sequence for Opus, exactly like the
clean mathematics derivations; the stem has to say which framework to use (otherwise the key is ambiguous),
and naming the framework hands over the constants. What has not been tried: a question whose decisive step
is a judgement with no named constant, for instance which of two competing mechanisms the drawn data
support, where the wrong mechanism gives a clean but wrong number; and the extreme-value extrapolation of
pore size to the component volume, which adds a convention (the inspection volume) that is easy to get
wrong but is also in Murakami's book.

## Session 2026-10-17: first Engineering candidate, crack growth with closure (task07 folder reused)

Owner's decision in domains-for-new-task.md: Mathematics closed, Engineering (materials, titanium) from now on, four task
shapes listed, screen with 3 Opus and 1 Sonnet. Built shape 1: a log-log da/dN plot generated from a stated model
(work/model.py, draw_figure.py), two load ratios, fit lines through crosses on gridline intersections so the reading is
exact, the component at a third load ratio so the closure factor has to be interpolated, varying Y(a/W), failure at
K_max = K_IC with sigma_max = dsigma/(1 - R). Parameters tuned (work scan) so the key sits 4.3 percent inside its
two-significant-figure interval and every wrong route lands on a different value. Two verification routes, program
embedded in reference.txt, detector clean, findability nothing.

Screen: Opus 3/3 and Sonnet 1/1, all by the intended route, Opus in about two minutes each. The lesson is the one
the archive already recorded for biology type-4 designs (24/24 solved): once the stem states the model (U linear in
R, R = 0.5 closure-free, the Y polynomial, the failure criterion), the task is a derivation, and Summit's one-answer
rule leaves no way to keep the modelling choice open. The plot-reading lever does not exist when the anchors are on
gridlines, and off-gridline anchors would only add reading noise, not reasoning. Shapes 2 to 4 in
domains-for-new-task.md have the same structure (a named correction plus bookkeeping) and would screen the same way.
What has not been tried in Engineering: a question whose decisive step is a judgement the stem cannot state without
giving it away, for instance which of two plotted regimes governs the component (and the stem gives both), or a
physical inconsistency planted in the figure that the solver must notice (a point that cannot belong to the stated
model). Variant 2 built and verified the same night (closure switched off above K_max = K*, read from where the R = 0.1
points join the solid line; the service integral splits at the depth where K_max reaches K*, and switching on dK
instead of K_max, or never switching, gives different lives): Opus 1/1 correct in 3 minutes, 53k tokens. Four
Opus runs over two variants, all solved in 2 to 3 minutes. Rule applied: a candidate that fails the local screen
is not pushed; the first variant was removed from the repo. Package kept locally in tasks/task07-crossing-number.

Follow-up (v4, same session): the one lever not yet tried in this domain was the log-axis reading that broke
both models on Lumiere (values between major gridlines, linear interpolation). v4 keeps the v3 question and
redraws the figure with standard log axes and the steep-branch points inside the 100 to 200 MPa interval,
off every gridline (true 172, 148, 129, 114 MPa; linear interpolation gives 178, 156, 137, 118 and the
answer 210). Opus read all of them within one percent, 3/3 correct in about a minute each; Sonnet 0/1.
Verdict for the Engineering direction after four shapes across the sibling sessions and this one (crack
growth with threshold, crack growth with closure, Kitagawa with internal pore, Kitagawa with log reading):
every design built on a standard model is solved by Opus 3/3 locally in one to two minutes, with the
reading, the model identification, the regime check and the named constants all retrieved. The mechanism
that produced Summit's in-band results (archive task08) and the only local Opus failures (pebbling v1
rooted, parsimony v2) is a construction or a search with a weak retrievable toolkit, and that does not
exist in a one-figure fatigue estimate. Stopped here per the owner's rule: say so when a direction fails.

Third attempt (v5): the crossing lever that gave the sibling Opus 2/3 on the crack-growth plot was transplanted
to an El Haddad fit (a curve, no straight-line cross-check, two exact gridline crossings, 1-2-5 grid). To keep
it fair every other gridline miss was held to at least 15 percent of a step, and the parameter search then
left only crossings on labelled lines. Opus 3/3 in under 90 s, Sonnet 1/1: the crossings were found at once and
cross-checked against the data points. The sibling's 2/3 came from misses of 17 to 18 percent of a step on a
curve whose crossings competed with a tempting pair on major lines; at my fairness threshold the trap is gone.
Verdict: the reading lever works only in the band between "unfair to a person" and "obvious", and the El
Haddad shape does not have room in that band. Three Engineering designs in this folder, all 3/3.

Fourth attempt (v6): the sibling's recipe applied to a new quantity. Semi-log S-N plot so that a Basquin fit is
curved and has no straight-line cross-check; exact crossings on minor lines (5e4, 310) and (2e6, 230); the
major-line pair (1e5, 290), (1e6, 240) at 19 and 24 percent of a step; integer answer (complete blocks under
a two-level block with Haibach's extension) chosen so the integer survives rounding of k and of the fatigue
limit but flips under the major-line decoys. Screen: Opus 2/3 (the miss took (1e6, 240) with (5e6, 210)),
Sonnet 0/1, runs of 2 to 7 minutes, no cut-offs. Lesson: the recipe transfers. The parts that mattered were
(1) a curved fit, (2) exact crossings on minor lines only, (3) every other crossing missed by 14 to 24 percent
of a step, (4) an answer that is sensitive to the pair chosen but tolerant of honest rounding; (5) the
integer-answer form gives that tolerance for free. The search scripts are in v6-sn-haibach/work (design.py
for the crossings, robust.py and the scan in the session log for the block).

Fifth to seventh attempts (v7 to v9, same session). v7 rainflow: Opus 3/3, the procedure is routine. v8 (two S-N
curves, three-part block): Opus 3/3 and Sonnet 1/1, all runs anchoring the fits on the frame ends and the
plateaus, which sat within one percent of gridline values; a free anchor anywhere defeats the crossing lever.
v9 (curves started inside the frame, plateaus mid-interval): Opus 1/3, both misses on the same tempting pair
(2e4, 280) and (1e6, 200) where the solid curve is at 273 MPa; Sonnet 1/1 by a benign misread. Two in-band
candidates now exist in the folder: v6 (Opus 2/3, Sonnet 0/1) and v9 (Opus 1/3, Sonnet 1/1). Rules distilled
from v6 to v9: (1) curved fit, exact crossings on minor lines only; (2) no curve end, plateau or data point
within 2 MPa or 10 percent of a step of any crossing; (3) tempting major-line pairs at 15 to 25 percent of a
step; (4) integer answer with a 3 to 5 percent margin, checked against rounding of every parameter; (5) two
curves double the chances of a misread without doubling the stem.

## Session 2026-10-17 (late): biology, maximum parsimony (task07 folder reused a second time)

Owner's instruction: no mathematics, no mechanics, work in physics or biology. Rebuilt the colleague's parsimony shape
(the only design in the record with a genuine Opus miss and no cut-off: his task10 v2, Opus 0/1 at 8 min): own
generator (work/gen_mp.py, mp.py: leaf-insertion enumeration, bit-parallel Fitch, NNI, stepwise addition, maximum
compatible sets), 210 hits in 25 minutes, ranked by uniqueness of the optimum, failure of the heuristics and the
number of trees one step above. Chosen 9 x 18, optimum 36, 77 trees at 37. Two routes agree. Figure: matrix grid.
Screen: Opus 0/3, Sonnet 0/1, every run cut off at the 64k output ceiling without an answer (the models read the
matrix two or three times and then search in text). Same verdict as the crossing-number v1: length, not reasoning.
The difference from the colleague's run (an answer after 8 min) is probably the output cap of his harness. Not
pushed. If the family is kept, the instance has to shrink until a search fits in about 30k tokens (8 x 14 was
solved by Opus with an exact accounting proof in the archive, so the window, if it exists, is 8 x 16 or 9 x 14 with
two or three 3-step characters); otherwise the family is closed too.
Owner's correction later that night: only the Mathematics category exists on the account (domains-for-new-task.md
updated by a sibling session). The same problem is a mathematics question as it stands: the minimum weight of a
binary tree with the given binary vectors at its leaves and free internal vectors, weight = total Hamming distance
over the edges (Steiner tree in the Hamming cube). build_package.py now uses that framing, subdomain "Combinatorial
optimization: minimum Steiner trees in the Hamming cube (maximum parsimony)", figure labels vector/coordinate with
the digit printed in each cell (the 9 x 18 cut-offs were partly re-reading). Smaller instances under screen:
9 x 14 (key 33, unique, 82 trees at 34, NNI 0/40, greedy insertion 2/40, compatible sets of size 3) and 8 x 15
(key 34, unique, 74 trees at 35, NNI 1/40, insertion 1/40).

## What the archive teaches, in short

The colleague ran about 150 model attempts over 17 designs in three days. Clean derivations of any length, coalescent casework, pedigree kinship, knot invariants to ten crossings, pixel-level reading of clean figures, chirality: all solved five out of five. The only accepted task (his task08) had a quantity with no retrievable characterisation, a construction trap measured by a proxy before screening, an instance just beyond hand reach, and a reference file with a written lower-bound proof plus embedded programs. Misses caused by the token ceiling count against the question. Read the archive sections "Summit verdict on task05", "Summit verdict on task06 version 2" and "task08 accepted" before designing.

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
Screen: Opus 1/1 correct (13/4, 10.5 min, 64k tokens; it read the figure correctly, proved alpha = 4 and chi = 4 by hand, refuted weight 3 by an
inconsistent linear system and produced both certificates). Sonnet 0/1: answered 3 after misreading the crossing of edges 1-5 and 3-6 as 1-3 and 5-6;
the swapped graph has a proper 3-colouring. Lesson: a crossing whose swapped reading is also a valid 4-regular graph is a reading trap for the weaker
model only; Opus traced the straight lines. Lever left if the family is reused: the instances with chi_f = 25/8 or 22/7 (seeds 125, 1222, 952 in
scratchpad fc/res2_12_4_0.pkl) have dual weights with denominator 8 or 7 spread over all twelve vertices, so the structured guess that gave Opus the
dual here (half on a triangle, quarter elsewhere) is not available; the hand proof in the solution then has to be the list of maximal independent
sets with their weights. Same pipeline (search2.py, verify_key.py, draw_figure.py), about two hours.

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
Screen of the revision: Opus 0/1, cut off at the 64k output-token ceiling with no answer (the cut-off signature that Summit tagged "unfair" on
the archive's task06); Sonnet 0/1, answered 19/6 after reading all 40 edges correctly and finding the vertex-deleted bound, 61 minutes,
135k tokens. The figure was read correctly by both, so the planar drawing did its job. Assessment: in band only if Opus sometimes finds
the 1/11-2/11 weighting within its budget; a 0/5 or cut-off verdict is at least as likely. Fallback at the next size down, same pipeline:
planar medial graphs on 18 vertices with chi_f = 19/6 or 16/5 (scratchpad fc/res_planar_18_0.pkl, seeds 138, 500), about 1100
independent sets, 107 to 129 maximal.

## Session 2026-10-17: domain change to Engineering, task08 rebuilt as a crack-growth question

The owner closed Mathematics (domains-for-new-task.md, decision of 2026-10-17) and asked for the task08 folder to be reused.
The two mathematics packages (fractional chromatic number 13/4 and the 35/11 revision) are archived in work/v1 and
work/v2-math, and in the repo under tasks/task08-fractional-chromatic-number/v1 and v2-math. The folder name is kept on
the owner's instruction.

New task (shape 1 of the domain file, Summit type 4): a self-drawn log-log da/dN against delta K plot for long cracks in
MIM Ti-6Al-7Nb at R = 0.1 and R = 0.7, dashed Paris fits, knee near threshold. Generated from the law
da/dN = 1e-12 dK_eff^3 (1 - (2.5/dK_eff)^4) with the closure model K_op = 0.30 K_max (no closure once K_min >= K_op), so the
R = 0.7 set is the intrinsic curve and the R = 0.1 set is the same curve displaced by 9/7 in dK. The R = 0.7 fit passes
exactly through the grid intersections (10, 1e-9) and (100, 1e-6), so C and m are read exactly. Question: cycles to
failure of a wide plate with an edge crack from a 0.20 mm pore, Y = 1.12, sigma_max 400 MPa, R = 0.4, K_IC 55, three
significant figures. The stem states the closure model and tells the solver to use the Paris fits throughout. First version (closure level 0.30): at R = 0.4 K_min = 0.40 K_max
exceeds K_op, so the crack is closure-free and the R = 0.7 fit applies unchanged; key 1.04e6. Screen: Opus 3/3 correct in
about a minute each, Sonnet 1/1 correct. Too easy: once the closure model is stated, "reuse the closure-free curve" is
one comparison. Second version (closure level 0.55, the R = 0.1 fit exactly a factor 2 to the right, through (20, 1e-9)
and (200, 1e-6)): at R = 0.4 K_min = 0.40 K_max is below K_op = 0.55 K_max, closure is still present, dK_eff = 0.75 dK,
and neither measured curve applies as it stands; key 2.47e6 by closed form, Simpson and scipy quad. The closure-free
answer 1.04e6 is now the main trap, and it is also what the common prior "no closure above R = 0.3 in titanium" gives.
Other wrong routes: R = 0.1 fit 8.33e6; log-linear interpolation 2.94e6; Elber's U = 0.5 + 0.4R 3.62e6; a_c from delta
sigma 2.72e6; sigma_max in place of delta sigma 5.33e5. The knee would move the third figure (2,505,221 against 2,466,809),
so the stem says to use the Paris fits throughout. Figure script and program embedded in reference.txt; the re-extracted program reruns to identical
output. Account check: Engineering was not in the Category dropdown on 2026-10-16; the owner said he will change the
domain. task.json carries "engineering"; the Physics fallback needs only the domain and subdomain fields changed.
Screen of the closure-0.55 version (3 Opus + 1 Sonnet): Opus 3/3 correct in 39 to 58 seconds, Sonnet 1/1 correct in two minutes. Every run
read C and m from the gridline points, the factor-2 displacement, derived K_op/K_max = 0.55, saw that K_min < K_op at R = 0.4 and
integrated with delta K_eff = 0.45 K_max. Verdict for the shape: a type-4 plot whose model is stated in the stem is a clean derivation,
solved as surely as the mathematics tasks were; the closure prior (no closure above R = 0.3 in titanium) never competed with the stated
model. The lever the domain file hoped for (the expert picks the relation) cannot coexist with Summit's demand for an unambiguous key when
the relation is named in the stem. What is left to try in Engineering: shape 3 (space-holder composition to modulus, where the hydrogen
loss of TiH2 and the residual strut porosity are facts the solver must supply, not assumptions the stem names) and shape 2 with the
internal-defect constant; both carry the same risk unless the decisive fact is one the models do not retrieve.

Third version, constant K_op (the two data sets converge and merge near delta K = 54 instead of running parallel): K_op = 6 read
exactly from equal-rate pairs placed on grid lines (4 against 9, 14 against 18, 24 against 27, 34 against 36, 44 against 45). At
R = 0.4 closure is present from a0 (K_min = 4.49) and disappears at K_max = 15 (a_t = 0.357 mm), so the life is a two-stage integral
with two closed forms, 4.85e5 + 7.12e5 = 1.2e6 (two significant figures, because a K_op misread by 0.5 moves the third figure). Wrong
routes: closure ignored 1.0e6, transition ignored 8.9e5, K_op as a fraction 2.2e6, parallel-line reading 8.3e6, a_c from delta sigma
1.3e6. Screen: Opus 3/3 in 78 to 89 s, every run with the transition and the two-stage integral; Sonnet 0/1 (ignored closure after
reading the last stem sentence as permission to do so; sentence reworded afterwards). Family verdict after three versions and 12 runs:
any stated closure model turns the type-4 plot into a derivation that Opus finishes in under two minutes. Not submitted.

## Session 2026-10-17 (later): construction shape in Engineering, task08 rebuilt as a constrained test matrix

The owner rejected the crack-growth versions after three local 3+1 screens were all solved, and asked for a hard task.
The only shape with Opus misses on record is construction plus a short certificate with a non-tight natural bound
(archive task08). Engineering framing: the smallest pairwise-covering fatigue test programme (a strength-two covering
array with forbidden level pairs). Instance search (scratchpad ca/search_ca.py, search_ca2.py; exact minimum by
scipy milp, all optimal designs by no-good cuts, LP dual as certificate, randomised greedy as the construction proxy):
random forbidden sets on five three-level factors give a gap above the trivial 9 in most cases, almost always with an
integral LP dual, i.e. a set of N pairwise incompatible level pairs that proves the bound by hand. Most instances have
hundreds of optimal designs (construction easy); the chosen one (3^5, five forbidden pairs A0C1, A0C2, A1D0, A2B1, B0D1)
has minimum 11 against the bound 9, only 24 optimal designs (4 up to renaming the free factor), and a certificate of 11
pairs in which six couples are incompatible only because all three levels of A are blocked. Randomised greedy never
reaches 11 (sizes 12 to 16 in 200 runs). Framing: powder, specimen geometry, space-holder content, oxygen, load ratio;
the figure is a table of levels and unavailable combinations. Key verified by the certificate checks (standard
library) and by the integer programme; the embedded program reruns identically. Findability: constrained covering
arrays are a known topic, this instance is not tabulated.
Screens. v1 (five unavailable, key 11): Opus 3/3 in 2.5 to 4.5 minutes, every run with the same proof (two unavailable combinations on one
powder level force every TiH2 specimen into one space-holder level, so that level needs 5 specimens, 5 + 3 + 3 = 11) and a construction;
Sonnet cut off. The search filter was then extended (search_ca3.py): no level with two unavailable partners in one other factor, and the
minimum must beat a level-counting bound with forced-level propagation. v2 (seven unavailable, unique optimal programme among C(105,10),
47 ten-pair certificates, key 10): Opus 3/3 in 5.5 to 9 minutes, each run proving the bound by a counting or permutation argument on the
unconstrained factor pairs and then finding the unique programme by hand; Sonnet cut off. v3 (six factors, ten unavailable, 223 admissible
specimens, 125 pairs, pair bound 9, incompatible-pair bound 10, key 11 proved only by a half-integral weighting of total 21/2, four
optimal programmes): Opus 0/3, all cut off at the 64k output ceiling; Sonnet 13 (construction overshoot).
Verdict for the family: at five three-level factors Opus constructs even a unique optimal programme within its budget (65 to 80k tokens);
at six factors it never finishes. The in-band window, if it exists, lies between (a 4-level factor among five, or six factors with a
less constrained optimum); the local 64k output ceiling and Summit's cut-off tagging make the upper side of that window unusable.

## Session 2026-10-17 (night): Mathematics only; task08 becomes a covering array avoiding forbidden pairs

The owner confirmed that only the Mathematics category is open; domains-for-new-task.md was rewritten by a sibling session
to say so, and a section on constrained covering arrays was added. The test-matrix question is pure combinatorics
(covering arrays avoiding forbidden edges, Danziger, Mendelsohn, Moura and Stevens, TCS 2009), so the verified instance
was restated with no setting: an N x 5 array over {0,1,2}, seven forbidden symbol pairs shown as a 15 x 15 chart,
covering condition on every admissible pair, smallest N. Instance: the unique-optimum one (forbidden (x1=0,x5=1),
(x1=1,x2=0), (x1=1,x3=2), (x1=2,x2=1), (x2=1,x3=1), (x2=1,x4=1), (x4=0,x5=0)); key 10. The key must differ from the
retrievable unconstrained value CAN(2,5,3) = 11, which it does; 11 is listed as a common wrong answer. Package in the
task08 folder (zip covering-array-forbidden-pairs-five-columns.zip), earlier versions under work/.
Instances with an LP integrality gap (minimum 12 with every fractional certificate below 10.8, scratchpad
ca/search_ca5.py) exist at five columns, but each has sixty or more optimal arrays and no written lower-bound proof
short of the integer programme, which the consistency check has refused before; kept for later.
Screen (3 Opus + 1 Sonnet): Opus 3/3 correct in 4.5 to 10 minutes; Sonnet run lost to a session restart. The gap-two
five-column instance (engineering wording, key 11, unique) was also Opus 3/3, in 22 to 32 minutes. Five columns of three symbols
are inside Opus's reach whatever the gap; six are beyond it (cut-offs). Next size tried: six columns with one binary column.

Task08 v2 (six columns, one binary, key 10, two optimal arrays): Opus 3/3 in 2.5 to 5 minutes, Sonnet 1/1 in 8 minutes. The
uniqueness of the optimum does not make construction hard: the counting proof of the bound is tight, and tightness pins the column
group sizes, from which the array follows in a few lines. Covering arrays with forbidden pairs are closed for this account unless the
lower bound itself needs a non-counting argument (LP gap), and those instances had sixty or more optimal arrays.

---

# Archive: colleague's log, Biology/Medicine account, 2026-10-10 to 2026-10-12

Everything below is copied unchanged. Paths, scripts, the task folders and the summit-task skill it mentions are on his machine, not this one.


## Hard constraints learned from the account

- **Category is Biology/Medicine only.** The Category dropdown in the Summit submit form shows a single option. task.json must use `"domain": "biology_medicine"`. A mathematics draft (knot signature) was written on 2026-10-10 before this was known; it is kept in `tasks/task00-archived-knot-signature-mathematics/` for reference only and must not be submitted.
- **All submitted text must read as written by a person, not an AI.** Question, solution, rubric descriptions, image-necessity box, references. Plain prose, the voice of a researcher writing a problem for a lab meeting or a graduate exam. No boilerplate openers, no "Note that", no bullet-list solutions, no meta-remarks about models or about the question itself, no "Remark (not needed)". Numbered steps in the solution are required by Summit, but each step should read like a sentence a person wrote.
- **One folder per task** under `tasks/`, named `taskNN-short-topic-slug` (two-digit running number, then a slug that says what the question is about). Never mix two tasks in one folder.

## Folder layout for a task

```
tasks/taskNN-slug/
  task.json            Summit package (schema summit-task-package-v1)
  image.png            the figure, 300 dpi, made by code (TikZ or Python)
  image.pdf            vector version of the same figure
  image_source.tex     or .py: the source that produced the figure
  reference.txt        verification notes uploaded as the References source file
  <slug>.zip           task.json + image.png + reference.txt at top level, for Import .zip
  README.md            human-readable copy: settings, image, stem, answer, solution, rubric
  verification_*.py    scripts that compute the answer key independently
```

`tools/example_build_package.py` is the builder used for task01 (writes task.json, README.md, the zip). Copy and edit it for a new task rather than hand-writing JSON, so LaTeX escaping stays correct.

## Workflow that has worked

1. Pick a biology/medicine subfield where the answer key can be computed exactly: evolutionary genetics, phylogenomics, coalescent theory, pedigree/kinship, pharmacokinetics, epidemic models, cable theory, enzyme kinetics. Avoid anything whose ground truth needs a lookup I cannot verify.
2. Design the trap first: a step where the natural approach gives a plausible but wrong number. Then choose parameters so the correct and trap answers differ at the requested precision.
3. Verify the answer key by at least two independent routes (closed form, independent algorithm, simulation). Put the results in reference.txt.
4. Make the figure in TikZ (pdflatex and pdftoppm are installed) or Python. Check it visually: every number the solver needs must be in the figure and nowhere in the text, labels must not overlap, tubes/lines must meet at nodes.
5. Compute the common wrong answers by actually running the wrong methods, not by guessing.
6. Build the package, validate: rubric points sum to 10, exactly one final-answer criterion that states the key, no wrong answer equal to the key, answerPrecision matches the stem wording.
7. Search the web for the stem and the key before finishing.

## Form settings and dropdown mapping

See `submission-guide.md` for the field-by-field guide. Short version:

| Form field | Dropdown options | task.json |
|---|---|---|
| Category | Biology/Medicine | `biology_medicine` |
| Modality | Multimodal (image preferred); Text-only | `image_reference`; `text_only` |
| Image reasoning pattern | Quantitative derivation from image-sourced data; Classification or identification from visual evidence; Multi-step discrete reasoning over image content; Figure/plot extraction with quantitative computation; Other image-grounded pattern (admin approval required) | `image_quantitative_derivation`; `image_classification_identification`; `image_multistep_discrete_reasoning`; `graph_extraction_computation`; `other_admin_approved` |
| Answer format | Exact-match / short answer; Multiple choice | `exact_match`; `multiple_choice` |
| Answer precision | Not set; No precision stated; Significant figures; Decimal places | `{"kind":"none"}`; `{"kind":"significant_figures","digits":n}`; `{"kind":"decimal_places","digits":n}` |

The References explanation box is locked until a source file is uploaded; a self-written reference.txt unlocks it.

## Environment

- Python venv with numpy, sympy, scipy, matplotlib, snappy lives in the session scratchpad and is not persistent. Recreate with `python3 -m venv venv && ./venv/bin/pip install numpy sympy scipy matplotlib` when needed.
- TeX Live with TikZ is installed system-wide; `pdftoppm -r 300 -png` converts to PNG.

## Task log

| Folder | Topic | Answer key | Status |
|---|---|---|---|
| task00-archived-knot-signature-mathematics | Signature of a knot from a closed 3-braid diagram (10_149) | −4 | Archived, wrong category, do not submit |
| task01-coalescent-gene-tree-concordance | v1: gene tree / species tree concordance probability (key 0.3538); v2: anomaly-zone threshold for the upper branch (key 4270 generations) | 0.3538 / 4270 | Both versions solved 8/8 in local blind tests (Opus 5/5, Sonnet 3/3). Too easy. Not submitted; kept for reference |
| task02-x-linked-inbreeding-mz-twin-pedigree | X-linked inbreeding coefficient of a proband in a six-generation pedigree with MZ twins, a first-cousin mating and a shared father | 19/64 | Built and tested: Opus 5/5, Sonnet 2/3 (one 9/32). Too easy for the band; held back |
| task03-two-locus-autozygosity-pedigree | Probability that a proband is autozygous at two linked loci (theta = 0.2) in a five-generation pedigree with four identity paths | 0.00633 (3 s.f.) | Built and tested: Opus 5/5, Sonnet 3/3. Too easy; held back |
| (scratchpad only, no task folder) | Seven hybridization-number / temporal-network drafts, see session notes below | 3, 3, 4, 4, 4, 5, 6 | All blind-tested 2026-10-10 evening; Opus 5/5 on all but one (4/5); not built into packages |
| task04-inheritance-mode-imprinting-pedigree | Multiple choice: which of nine inheritance modes fits a four-generation disease pedigree (paternally imprinted dominant allele; mitochondrial and X-linked look-alikes) | option 1 (maternally expressed, paternally imprinted) | Built and tested: Opus 5/5, Sonnet 3/3 (on a first figure with an ambiguous marriage line, since fixed). Too easy; held back |

| task05-temporal-hybridization-number-two-gene-trees | Two gene trees for nine species; minimum number of hybridization events in a tree-child, time-consistent network (temporal hybridization number; forest bound 4 is the trap) | 6 | Submitted 2026-10-11. Summit verdict: too easy, Model A 5/5 (band 1-4), rubric avg 9.2/10; duplicate, findability and weaker-model probe all passed; consistency check gave two advisory edits (say "no nontrivial proper cluster" instead of "no cluster of two or more species"; call the file verification_notes.txt, not reference.txt, in the references text). Local test had said Opus 4/5 |

| task07-minimum-recombination-events-haplotype-matrix | Exact minimum number of recombination events ($R_{\min}$, Hudson-Kaplan 1985) for eight haplotypes at eight SNPs shown as a base matrix; four-gamete and haplotype bounds 2, history bound 3, true value 4 | 4 | Built 2026-10-11; screen Opus 1/1 and Sonnet 1/1 both correct (4); not in band; held for the user's decision |
| task08-protein-backbone-knot-type | Knot type of a protein backbone from an irregular nine-crossing planar projection (closure outside the drawing); determinant 7 leaves 5_2, 7_1, 9_42, the Alexander polynomial decides | 5_2 | Built 2026-10-11; screen Opus 1/1 and Sonnet 1/1 both correct; not in band; held. Follow-up with a determinant-and-Alexander-blind pair (6_1 vs 9_46, DNA knot) in progress as task09 |
| task09-dna-knot-type-em-trace | Knot type of a knotted DNA circle (phage capsid, RecA-coated EM trace) from an irregular ten-crossing drawing; Alexander polynomial 2t^2-5t+2 and determinant 9 shared with 6_1, separated only by Fox 3-colourings (27 vs 9) or the Jones polynomial | 9_46 | Built 2026-10-11; screen Opus 1/1 correct (Gauss code, Alexander polynomial, 27 three-colourings, 2 minutes); Sonnet 1/1 correct (same polynomial, then H1 of the double branched cover Z3+Z3 against Z9, 4 minutes); not in band; held |
| task10-parsimony-length-deceptive-matrix | Length of the most parsimonious unrooted tree for a binary morphological matrix. v1: 8 species x 14 characters, answer 25 (archived in v1-eight-taxa/; screen Opus 1/1 by an exact hand proof, Sonnet 0/1). v2: 9 species x 18 characters, unique optimum 34 with three 3-step characters, six clique trees at 35 to 38, SPR descent 35 percent, stepwise addition 13 percent | 34 | v2 built 2026-10-12; screen: Opus 0/1 (answered 35: found the length-35 clique tree, proved 35 optimal only among trees containing one of the four-taxon splits 3, 8, 9, 13, 16 by a split-and-add bound, checked the rest by local search; about 8 minutes); Sonnet 0/1 (answered 35, the best clique tree, after a hand search of about ten topologies) |
| task11-tree-child-hybridization-number-five-events | Same stem as task06 on a new instance (H3): tree-child hybridization number of three 7-taxon gene trees; pairwise 3/3/3, three-tree forest bound 4, restriction count gives 5 on paper, two optimal sequences (A/B mirror), G the only final species | 5 | Built 2026-10-12; screen: Opus run 1 wrong (6, valid weight-6 sequence plus a false partner-ordering exclusion of 5, 41 min, no cut-off), Sonnet wrong (4, forest estimate); Opus runs 2 and 3: correct (5, mirror sequence, 19 min) and wrong (6, no proof, 27 min); tally Opus 1/3, Sonnet 0/1, no cut-offs; package ready, user decides on submission |

| task06-tree-child-hybridization-number-three-gene-trees | Three gene trees for seven species; minimum number of hybridization events in a tree-child network, no timing assumption (forest bound 4 and counting bound 5 are the traps; the unique optimal sequence makes construction hard) | 6 | Submitted 2026-10-12 (user's call after Opus 3/8 locally). Returned the same day: consistency check FAIL, 1 blocking: the exclusion of 5 rested on an exhaustive search that was asserted but not included. Fixed: reference.txt now embeds the complete self-contained search program tcsearch.py, its output, a counting reduction to 16 configurations with full state tables, and the network check; Step 5 rewritten. Resubmission pending |

| task08-minimum-recombination-events-ten-haplotypes | Same family as task07 at larger size: ten haplotypes, nine SNPs; four-gamete bound 2, haplotype and history bounds 4, best tree-plus-mosaic construction 6, true $R_{\min}$ 5 | 5 | ACCEPTED, in band (2026-10-12). Screen Opus 0/1 (6), Sonnet 1/1 (5). First submission failed the consistency check (3 blocking: lower bound only asserted from unattached code, scripts not in the notes, rubric c3 method-restrictive); revised the same day with a hand-checkable proof, embedded sources and a method-neutral rubric, edited field by field on the platform, then passed |
| task12-minimum-recombination-events-eleven-haplotypes | Same family as task08 (accepted) on a new instance and framing: eleven haplotypes of a 7,940-bp animal region drawn as filled/open circles at physical positions; four-gamete bound 3, haplotype and history bounds 4, tree-plus-mosaic construction 6, true $R_{\min}$ 5 | 5 | Built 2026-10-12; screen Sonnet 1/1 correct (5, marginal-tree SPR path, lower bound admitted unproven); Opus 1/1 correct (5, haplotype bound on S2,S4,S6,S7,S8 plus a four-case tightness argument and a five-crossover history, 20 min); package ready, user decides on submission |

Add a row here whenever a task is created, and update its status after Summit returns a verdict (accepted, too easy, too hard, flagged) together with the reason given.

## Local blind test before submitting (do this every time)

Summit runs Opus 5.5 (high effort) five times and Sonnet 5 three times. Imitate it before submitting: copy the
figure alone into an isolated folder (never the task folder, which holds the key), spawn five Opus and three
Sonnet subagents with the stem verbatim, tell them to use only the Read tool on that one file, no web, no
code, and to end with "FINAL ANSWER: ...". Grade against the key. Accept only if Opus gets 1 to 4 of 5 and
Sonnet at most 1 of 3. Record the tally in the task README and in the task log below.

Lesson from task01 to task03 (four designs, 32 attempts, one failure): any question that reduces to a
well-defined derivation gets solved by Opus 5.5 at high effort, no matter how many rules are stacked
(coalescent casework, anomaly-zone threshold, X-linked kinship with MZ twins, two-locus identity by descent).
The local "opus" subagent is the same Opus 5.5 that Summit uses, so this is a real signal; the local
"sonnet" is Sonnet 5.5, stronger than Summit's Sonnet 5, so Sonnet failures here are a lower bound.
Next direction: Summit's own difficulty examples are expert-judgment questions (classification with
near-neighbour exclusion, interpretation of experimental evidence), not derivations. Try those.

## Session 2026-10-10 (evening): hybridization-number designs, nine blind tests, none in band

After the user asked for harder questions, I built and blind-tested a family of phylogenetic-network
questions: gene trees in the figure, ask for the minimum number of hybridization events. Ground truth from
brute-force agreement forests (hybrid2.py), rSPR by BFS (spr_bfs.py), exhaustive enumeration of networks with
k reticulations (netcheck.py, net_multi.py, net_temporal.py), and for the temporal variant the cherry-picking
characterization of Humphries, Linz & Semple 2013 (cps.py, cps_build.py), validated 12/12 against
enumeration. Scripts live in the session scratchpad; copy them into tools/ if this family is ever reused.

| Instance | Key | Trap | Opus | Sonnet |
|---|---|---|---|---|
| 2 trees, 6 taxa, rSPR 2 | 3 | 2 | 4/5 | 3/3 |
| 3 trees, 6 taxa, pairwise 1,1,2 (forest bound 2) | 3 | 2 | 5/5 | 3/3 |
| 2 trees, 8 taxa, rSPR 3 | 4 | 3 | 5/5 | 1/3 |
| 2 trees, 8 taxa, swapped caterpillar halves, rSPR 2 | 4 | 2, 3 | 5/5 | 2/3 |
| temporal (tree-child + time-consistent), 7 taxa, h 2 | 4 | 2, 3 | 5/5 | 0/3 |
| temporal, 7 taxa, six cherries, two outgroups, h 3 | 5 | 3 | 5/5 | 3/3 |
| temporal, 9 taxa, no outgroups, h 4 (now task05) | 6 | 4, 5 | 4/5 | 0/3 |

Lessons. (1) Opus 5.5 at high effort retrieves the exact theorem (acyclic agreement forests; cherry-picking
sequences) and then runs a complete case analysis or state search by hand, even for 9 taxa. Its single
failure in 42 runs was a casework slip. (2) Sonnet 5.5 fails as soon as the instance is irregular, so the
Sonnet criterion is easy to meet once the structure is unstructured. (3) Making instances larger does not
move Opus; making the answer differ from every computable bound does not either, because Opus computes the
right quantity. (4) The one design that landed in band (task05) combined a research-level characterization (temporal
hybridization number via cherry-picking sequences), a nine-taxon instance with no outgroups so the search
has many branches, and a free move that is easy to overlook; Opus missed it once in five. If this family is
reused, keep those three ingredients. Verification scripts are copied into the task05 folder.

If task05 comes back too easy, next direction to try: Summit task type 4, figure extraction with computation, where a plot
generated by code must be read precisely and the trap is in choosing the right segment or model (flip-flop
pharmacokinetics, Scatchard plot with two binding classes, non-linear Arrhenius). Vision precision is the
one capability where Opus runs vary from attempt to attempt. Place data points on gridlines so an expert with
a ruler reads them exactly, and state the precision.

## Summit verdict on task05 (2026-10-11) and what it teaches

Pipeline order as shown by Summit: Duplicate check, Consistency check (advisory notes on the solution text,
written automatically), Findability (web search for the question and key), Weaker-model probe (3 attempts),
Rollouts (Model A, high reasoning effort, 5 attempts, 3 to 5 minutes and about 24k tokens each; a judge
reads the final answer and an LLM grades the rubric), Trajectory QA (skipped). The returned item can be
revised and resubmitted ("Strengthen the question and submit again").

All five Summit trajectories retrieved the Humphries-Linz-Semple cherry-picking theorem from memory and ran
the search by hand, exactly as the local Opus runs did. The local blind test (4/5) was therefore well
calibrated but slightly optimistic; treat a local 4/5 as "will probably return 5/5" and aim for local 2/5
or 3/5 before submitting.

Rule going forward: a question whose answer is "known theorem plus a finite search" will not pass, no
matter how wide the search. Difficulty has to come from something the models cannot retrieve: precise
reading of a generated plot (Summit type 4), a judgment that needs an empirical fact from the user's own
field, or a model choice where the standard framework is wrong and the correct one is not a named theorem.

## Ideas not yet used

Kept here so future tasks do not repeat task01's framing.

- Flip-flop pharmacokinetics: oral and IV curves on one semi-log plot, ask for the absorption rate constant (the terminal slope is absorption, not elimination).
- Fixation probability of a mutant on a small drawn graph under the Moran process (the large-N star-amplifier formula is the trap; exact answer from the Markov chain).
- Anomalous gene trees: most probable gene-tree topology for a caterpillar species tree inside the anomaly zone (multiple choice).
- Rall's 3/2 rule on a drawn dendritic tree: input resistance when the equivalent-cylinder condition fails on one branch.

## Session 2026-10-11 (option 1: figure extraction with computation)

User chose direction 1 (Summit type 4). First family tried: fluorescence anisotropy titration where the
bound probe is three times brighter than the free probe (so the anisotropy midpoint is not the Kd) and the
probe is at 20 nM against Kd 30 nM (so protein is depleted). Answer asked as the standard free energy of
association at 25 C to the nearest kJ/mol (-43), which tolerates Kd readings from 24 to 36 nM while the
quantum-yield-blind routes give -45 or -47 and the depletion-blind route gives -42.

Draft A (lifetimes 1.2/3.6 ns and "radiative rate unchanged" stated in the stem, single panel):
local tally Opus 5/5, Sonnet 3/3. Stating the lifetimes hands over the correction; every solver wrote the
intensity-weighted formula and the quadratic. Not submittable.

Draft B (no lifetimes; panel B shows emission spectra of free and saturated probe, 1.0 vs 3.0): under test.
Figure scripts: scratchpad fp/drawfp.py, fp/drawfp2.py (matplotlib in scratchpad venv), fp/model.py,
fp/verify_fp.py. Blind-test folders scratchpad/blindtest/fp and fp2.
Draft B result: Opus 5/5, Sonnet 3/3. Every solver read the 3x peak ratio from the spectra panel and applied
the intensity weighting; the easy correct route (use the intensity itself as the binding signal) also exists.

Draft C (burst kinetics, acyl-enzyme, k_obs 0.80 given, burst amplitude 2.25 uM and v_ss 0.60 uM/s read
from the curve, A280 concentration 5.00 uM as the trap, answer k3 = 0.20 s^-1): Opus 5/5, Sonnet 3/3. All
eight wrote pi = E(k2/(k2+k3))^2 from memory and cancelled E. One Opus run called the trap "well signposted".
Scripts: scratchpad burst/model.py, burst/drawburst.py.

Lesson from A, B, C (24/24 solved): any "known correction" in a standard assay, however rarely applied in
practice, is retrieved instantly by both models; the stem that makes the question unambiguous is the cue.

Draft D (linkage, type 4 reading): 18-person three-generation pedigree, autosomal dominant, one
microsatellite with genotypes given only as stacked electropherogram traces (peaks on 4-bp gridlines).
Traps: phase-unknown sibship from I-1 (3 meioses), II-1 phase-known 5 meioses with one recombinant
(III-5), II-3 homozygous 212/212 so his 3 children are uninformative, II-2 unaffected so his 2 children
are uninformative. Z(0.05) = 0.6503 -> 0.65; Zmax = 0.80 at theta 0.126. Wrong routes at 0.05: gen I as
phase-known 0.95, II-3's children counted 1.49, recombinant missed 1.93, II-2's children counted -0.07.
Scripts: scratchpad link/ped.py, link/lod.py, link/drawlink.py. Under test.
Draft D result: Opus 5/5, Sonnet 3/3. All five Opus runs transcribed all
36 peaks correctly, recognised the phase-unknown sibship, the homozygous parent and the unaffected parent,
and computed 0.65. Clean code-generated figures do not produce vision errors at this density; the
"vision precision" lever noted earlier does not exist for Opus at gridline-aligned figures.

Day summary (2026-10-11, option 1): four designs, Opus 20/20, Sonnet 12/12.
Combined with earlier sessions: roughly 125 Opus attempts over 17 designs, 3 wrong, all three in the
task05 search. What remains untested: (i) questions whose answer depends on an empirical fact from the
user's field that the model cannot derive; (ii) combinatorial problems with no retrievable reduction
theorem where the only route is direct reasoning (candidate: tree-child hybridization number for three
trees, Linz and Semple 2019 characterisation, verified by enumeration); (iii) multiple-choice type 2/3
items built on research-grade nuance. Do not spend more runs on standard-assay corrections or on
reading-precision designs.

## Session 2026-10-11 (option 2: tree-child hybridization number of three trees)

Theory (Linz & Semple 2019, Adv. Appl. Math. 105:102-129; formalised in van Iersel et al. 2019
arXiv:1907.08474): the tree-child hybridization number h_tc of a set of trees equals the minimum weight of
a tree-child cherry-picking sequence of ordered pairs (x,y): picking (x,y) deletes x from every current
tree in which {x,y} is a cherry; a leaf once picked may never again be a second element; all trees must end
as the same single leaf; weight = number of pairs + 1 - |X|. For two trees h_tc = h; for three or more
h_tc can exceed h (known 8-taxon example in that paper, h = 3, h_tc = 4). Every network (tree-child or
not) has at least |MAF| - 1 reticulations, where MAF is a maximum agreement forest common to all trees.

Tools (scratchpad tc/): tccps.py (exact h_tc by memoised search; validated 60/60 against hybrid2 on
two-tree pairs, cross-checked memo-free), tc_build.py (network from a sequence, Linz-Semple
construction, verified by netcheck), net_tc.py (exhaustive enumeration of binary networks with k
reticulations built from tree 1, classifies tree-child), maaf3.py (MAF/MAAF for three trees),
search_tc.py / search_tc2.py (random instance search).

Draft C2 (7 taxa, h_tc 4, pairwise h [2,2,3], temporal 5, but three-tree MAF has 5 components):
Opus 5/5 so far all 4 (forest lower bound |MAF|-1 = 4 is immediate), Sonnet 2/3. Rejected: the naive
forest count equals the answer.

Drafts D1, D3 (7 taxa): h_tc 4, three-tree MAAF has 4 components (naive answer 3), pairwise h
[2,2,3] / [2,3,2], temporal 5 / 6, optimal sequences pick no leaf more than twice (so a binary
four-reticulation tree-child network exists; built and verified). Enumeration at k = 3 running to learn
whether a non-tree-child network with 3 reticulations exists (h = 3). Blind tests launched on both.
D1 = (((G,E),B),((C,D),(F,A))) | (F,((B,((E,G),D)),(C,A))) | (((F,B),(C,D)),(A,(E,G)))
D3 = ((((G,D),E),F),(B,(A,C))) | ((((G,A),D),(E,F)),(C,B)) | (((C,F),(D,(A,(G,E)))),B)
Results: D1 Opus 5/5 Sonnet 3/3; D3 Opus 5/5 Sonnet 2/3; C2 Opus 3/5 Sonnet 2/3. Opus cites the
Linz-Semple sequence characterisation by name and searches with it; a "parity" bound (sum of the three
pairwise h divided by 2, rounded up) also reaches 4 on D1/D3. Both C2 misses were false impossibility
proofs after failing to construct the 4-reticulation network: Opus's weakness here is construction, not
proof. Gap-two instances (h_tc two above every cheap bound) exist on 7 taxa but all need a leaf picked
three times (a three-parent hybrid), which no binary tree-child network realises; unusable.
Drafts F2, F3 (7 taxa): h_tc 5 = three-tree MAAF bound, every pairwise h <= 3, five hybrids over the
two-leaf backbone {A,B}, so the optimal network is necessarily chained; temporal None.
F2 = (((C,F),(B,E)),(G,(A,D))) | ((B,(D,C)),((E,(F,G)),A)) | ((D,((C,F),G)),((A,B),E))
F3 = ((((D,(G,C)),(E,F)),B),A) | ((G,C),((E,(D,A)),(F,B))) | (((F,(A,D)),C),(B,(E,G)))
Results: F2 Opus 5/5 Sonnet 0/3; F3 Opus 5/5 Sonnet 0/3. Opus proved the bound 5 three different
ways (root-split signature: every pair split by some root so at most one leaf can be a single pick;
singles counting; a "switching" argument that two displayed trees must differ at >= h(Ti,Tj)
reticulations, then case analysis at k = 4) and built the Linz-Semple sequence each time. Sonnet
cannot do these at all. Verdict: when the cheap bound is tight, Opus is 5/5; its only failures so far
(C2, 2 of 5) came from failing to construct an optimal network and then "proving" impossibility.

Lever found afterwards (search_tc4, analyze4.py): 116 seven-taxon instances have h_tc two or three above
the three-tree MAAF bound and still admit a binary optimal sequence (no triple pick), but the parity
bound ceil(sum pairwise h / 2) is always within 1 of h_tc on them, so the bound gap is not exploitable.
What is exploitable is construction difficulty: number of optimal binary sequences (count_opt_binary)
for the tested instances is C2 852, D1 5192, D3 2692, F2 902, F3 1102, and C2 was the only one Opus
missed. New drafts chosen for minimal count:
G1 = (((A,(F,(D,G))),E),(C,B)) | (((D,F),(B,A)),((G,E),C)) | (F,((G,(((A,B),C),E)),D))
  h_tc 5 (= MAAF bound, pairwise [3,3,3], temporal None), only 2 optimal sequences, final leaf F.
G2 = ((G,B),((F,((E,A),C)),D)) | (((B,A),(F,G)),((D,E),C)) | (A,(F,((B,D),(G,(E,C)))))
  h_tc 6 (MAAF bound 4, parity 5), exactly 1 optimal binary sequence, final leaf G; every other leaf
  is picked twice. Both networks built with tc_build and verified (binary, tree-child, display all
  three). Figures fig/g1-1.png, fig/g2-1.png; blindtest/tc_g1, tc_g2 launched (5 Opus + 3 Sonnet each).
Results G1: Opus 4/5 (one miss: a false "no 5-network" proof followed by a 6-network), Sonnet 2/3 (both
guesses "5", one from "no common triple so at most two non-hybrids"). Too easy on the Sonnet side.
Results G2 (answer 6): Sonnet 0/3 (4, 5, 4). Opus: of the five original runs, one answered 6 with a
correct network, four died at the 128k output-token ceiling with no answer; a replacement run answered
"no such network exists" (wrong: its lemma assumed a hybrid leaf's sister clade in each tree must
contain a leaf from the parent's component, which ignores hybrids hanging below the reticulation).
Tally so far Opus 1/6 answered correctly. In band but at the floor; a 0/5 at Summit is plausible.
G3 (calibration between G1 and G2, answer 6, 14 optimal binary sequences, temporal None, unsplit pairs 4):
G3 = ((G,B),(F,(E,(C,(A,D))))) | (E,(((B,A),D),(C,(F,G)))) | (((E,((C,G),F)),(D,B)),A)
  network built and verified (6 reticulations, binary, tree-child); fig/g3-1.png; blindtest/tc_g3
  launched (5 Opus + 3 Sonnet).
Results G3: Sonnet 0/3 (5, 5, 5); Opus 4/4 so far with one run pending (all with Linz-Semple sequences
or component case analyses). Fourteen optimal sequences is already enough for Opus to construct;
G2 with its single optimal binary sequence is the only instance in the family that defeats Opus.
G2 final tally: Opus 2 correct of 7 runs (4 ran out of output tokens, 1 "no such network"), Sonnet 0/3.
User instruction (2026-10-11): from now on screen with ONE Opus agent; solved = stop, unsolved = report
and the user submits. Single screen launched on G2. Package built meanwhile:
tasks/task06-tree-child-hybridization-number-three-gene-trees/ (task.json, image.png, reference.txt,
zip tree-child-hybridization-number-question.zip, README.md, verification/ with g2_cert.py reproducing
every number; rerun from the folder matches the saved output).
G3 final: Opus 5/5, Sonnet 0/3. Rejected.
Single-agent screen on G2: Opus SOLVED (6, found the unique optimal binary sequence). Per the user's rule,
stopped; G2 not submitted. Overall G2 record: Opus 3 correct of 8 runs (4 no answer at the token
ceiling, 1 wrong), Sonnet 0/3. The task06 package stays in tasks/ in case the user decides to submit.
Family verdict: tree-child h_tc of three 7-taxon trees. Opus knows the Linz-Semple characterisation and
three independent lower-bound techniques; its only weakness is constructing an optimal sequence when
very few exist. Even the unique-sequence instance gets solved about 3 times in 8.

Rule (2026-10-11): every package must come with paste-ready text for the Summit References box
"Please explain where to find or verify the answer" (theorem with number, where in reference.txt, which
script reproduces it). Added to task06 README under "Verify field".

Skill (2026-10-11): `.claude/skills/summit-task/SKILL.md` holds the whole workflow (read-first list, hard
rules, what fails, build, single-agent screen protocol with the agent prompt, package checklist,
hand-over items including the verify-field text). Invoke with /summit-task in any session in this repo.
Screening rule updated (2026-10-11): after creating a task, test with one Opus 5.5 high agent and one
Sonnet agent, report both results to the user, who decides on submission. Written into the skill.

## Session 2026-10-11 (late): minimum recombination events, task07

New family, same lever as task06 (construction plus an unprovable-by-hand lower bound), but with a smaller
retrievable toolkit: R_min of a binary haplotype matrix (unknown ancestral alleles, infinite sites, single
crossovers). Opus knows the four-gamete bound R_m, the haplotype bound R_h and the history bound, all of
which are known to be non-tight; the exact value needs the Lyngso-Song-Hein backward search.
Tools (scratchpad rmin/, copied into task07/verification/): rmin.py (exact search with wildcards, two
variants: with and without the two eager rules; validated 80/80 against each other on random 6x6 matrices
and never below the three bounds), arg_cert.py (rebuilds the explicit ARG from the optimal history and
checks it by forward simulation from the root), cert.py (recomputes everything), gen5.py (generator:
random tree with mutations on internal edges, k recombinants from pool sequences forced into the sample,
keep only informative distinct columns). A bug found on the way: the search returned True for an empty
state before checking the budget, so a final split that empties the state was free; the ARG certificate
caught it (5 recombinations against a claimed 4). Fixed; all candidates rechecked with certificates.
Instance chosen: h1 00001000, h2 10110101, h3 00000100, h4 01111010, h5 10111010, h6 01111000,
h7 00011001, h8 10111101 (shaded allele = 1). R_m 2, R_h 2, history bound 3, leave-one-out 3 (2 without
h3), R_min 4. Six instances with this bound profile exist among 105 R_min-4 hits; this one has the fewest
optimal histories (4,905 move orderings). The optimal ARG needs an unsampled recombinant ancestor u that
carries the rare S5 allele of h2 together with the S6 allele before the S8 mutation; h3 is a double
recombinant. Backup R_min-5 instances (8x8, bounds 2/4/3) are in scratchpad rmin/g5_k5_*.out.
Screening rule now: one Opus 5.5 high run plus one Sonnet run, report both, user decides.
Screen results for task07: Sonnet (local Sonnet 5.5) answered 4, correct: four-gamete bound 2, a hand case
analysis over breakpoint placements ruling out 2 and 3 (self-described as "likely rather than proven"), and
an explicit four-recombination ARG. Opus result pending.
Opus (high) answered 4, correct: bounds 2, then a tree-chain argument (each site's marginal tree contains
its split; adjacent marginal trees at most k SPR moves apart; TBR via maximum agreement forests as a valid
lower bound) checking every placement of a third breakpoint, then an explicit four-recombination ARG
(h5 one crossover from h8|h4, h7 one, h3 two: h1 prefix, h2 at S5-S6, h1 suffix).
Lesson: the R_min family does not escape Opus either. Opus converted the problem into marginal trees and
SPR/TBR distances, a reduction it retrieved and ran by hand on 8 taxa, and even Sonnet constructed the
four-event graph. The gap of two above the four-gamete bound did not matter because both models construct
first and then argue the lower bound. If the family is reused, the only lever left is instance size
(R_min 5 or 6 on 9 to 10 sites, where the marginal-tree chain has more breakpoints and the hand case
analysis explodes); backup R_min-5 instances are listed in scratchpad rmin/g5_k5_*.out and the generator is
in task07/verification/gen5.py.

## Session 2026-10-11 (night): knot-type identification from a backbone projection, task08 and task09

Direction: Summit type 2 (classification from visual evidence) in structural biology / DNA topology. The
figure is an irregular planar projection of a knotted closed curve drawn by code (gaps at under-crossings);
the solver must identify the knot. Ground truth: the curve is generated with its knot type guaranteed
(braid closure or pretzel, then an isotopy-preserving random walk on a polygon: a vertex move is accepted
only if the swept triangles meet no other edge, plus a thickness constraint so corner-cutting smoothing is
safe), projected along a random direction, and the drawn diagram is verified by SnapPy census
identification of the link exterior and by my own Wirtinger/Fox Alexander polynomial from the crossing
data. Tools in task08/verification: knot3d.py, polywalk.py, draw.py, search5.py, neighbours.py (table of
determinants and Alexander polynomials, all knots to 9 crossings; table to 10 crossings in scratchpad
knot/table10.txt), jones.py (Kauffman bracket Jones polynomial and Fox colouring counts).

task08 (5_2 drawn with nine crossings, no Reidemeister I/II move available; determinant 7 shared with 7_1
and 9_42): Opus 1/1 (read the Gauss code perfectly, re-routed a strand that passes under four crossings in
a row to get a six-crossing diagram, determinant 7, done in 2.5 minutes); Sonnet 1/1 (Alexander polynomial
from the 9x9 matrix in one minute). Lesson: both models read a clean nine-crossing diagram without error and
compute a 9x9 Alexander determinant reliably; the determinant-collision trap (7_1) never bit because the
polynomial or a quick simplification settles it. Crossing-reading errors do not happen at this density.

task09 (built: tasks/task09-dna-knot-type-em-trace): same figure style but a knot whose determinant AND Alexander polynomial coincide with
a neighbour's: 9_46 (pretzel 3,3,-3) versus 6_1, both 2t^2-5t+2, both signature 0, both Arf 0; through ten
crossings no other knot shares the polynomial. Separation needs the Jones polynomial, the Fox 3-colouring
count (9 for 6_1, 27 for 9_46) or a reduction that cannot exist. Framed as a knotted DNA circle from phage
capsids (RecA-coated EM trace), so no "common protein knot" prior helps. Diagram target: 10 to 11 crossings,
no Reidemeister I/II move, well separated crossings; 9_46 is compact (three twist strips) so the search needs
a loose embedding and a self-repelling walk (polywalk.walk_repel).

task09 result: Opus 1/1 (10-crossing Gauss code read correctly, Alexander polynomial 2t^2-5t+2 by Fox
calculus on a 9x9 minor, recognised 6_1 versus 9_46, solved the Fox 3-colouring system by hand: 27
colourings, H1 of the double branched cover Z3+Z3, answer 9_46; 2 minutes). Sonnet 1/1 (same polynomial, then the homology of the double branched cover, Z3+Z3 against Z9 for 6_1; 4 minutes).
Lesson for the whole knot family: Opus 5.5 does invariant calculus on 9- to 10-crossing diagrams without
error and knows which invariant separates which pair (determinant collisions, Alexander collisions,
colouring counts). The remaining pairs it could not separate by hand (mutants such as Conway versus
Kinoshita-Terasaka, which share Alexander, Jones, HOMFLY and colourings) are not separable by any hand
method either, so the family is closed for Summit's band. Three screens in one evening (task08, task09)
cost about 40 minutes each; do not build more knot-identification items.

## Summit return of task06 (2026-10-12) and the fix
Consistency check failed with one blocking item: "the decisive minimality step is only an assertion that an
exhaustive search visited 64,987 states"; the uploaded notes had no program, no complete case analysis, no
independently checkable certificate. Suggestion offered: attach the actual search program with inputs and
output and the state representation, or give a complete combinatorial proof.
Lesson: whenever the answer key rests on a computation, the uploaded reference file must contain the program
itself (self-contained, standard library only) plus its full output, and the solution must describe the state
representation and transitions. Add a hand-checkable reduction if possible.
Fix done: tcsearch.py (scratchpad tc/ and task06/verification/) recomputes agreement forests by partition
enumeration, h_tc by memoised search (maxpick 3: 6, 151,752 states; maxpick 2: 6, one optimal sequence,
65,497 states), the network check, and a certificate: a weight-5 sequence must have pick counts (2,2,2,2,2,1)
or (3,2,2,2,1,1); restrictions to pairs plus the pairwise maximum forests (3, 1 and 1 of them) leave 16
configurations, all shape (2,2,2,2,2,1), each searched in full (10 to 48 states, all dead ends, tables printed).
Control: the shape of the true weight-6 sequence completes. Validated on C2, D1, F2, G1, G3 (4, 4, 5, 5, 6 and
the known sequence counts). reference.txt (70 kB) embeds program and output; extracted program reruns to the
same output. Zip rebuilt. Question, figure and answer unchanged, so no new screen was run.

## Session 2026-10-12: task07 declined, task08 built

The user declined task07 (both screening agents solved it) and asked for a new task. Lesson applied: both
models construct first (a tree-compatible core plus each remaining haplotype as a mosaic of tree lineages
and earlier haplotypes) and then argue the bound. New proxy mosaic2.py computes that natural-construction
bound U exactly (all maximal compatible cores, all orders, all segmentations, tree segments checked jointly
for a perfect phylogeny; copies only from haplotypes added earlier, since mutual copying was found to give
invalid cycles). Generator gen6.py (chains of recombinants, some intermediates unsampled) with filters
R_m, R_h, H_b <= k-1, U >= k+1, R_min = k, certificate OK. About one hit per 2,000 unique instances; some
twenty hits with k = 4 and six with k = 5, all U = k+1.
Chosen: 10 haplotypes x 9 sites, R_m 2 (unique hitting set S4|S5, S6|S7), R_h 4, H_b 4, U 6, R_min 5
(236,061 states with eager rules, 5,510,018 without; ARG forward-checked). The saving over the mosaic
construction: the S5 and S7 mutations sit on a lineage below the recombinant ancestor of h7, and h6, h9,
h10, h5 inherit from it. Package in tasks/task08-minimum-recombination-events-ten-haplotypes/.

## Session 2026-10-12 (morning): maximum parsimony on a deceptive matrix, task10

User declined task08 and task09 (both screens solved). New family with the only structure that has ever
produced Opus misses (construction plus a lower bound that cannot be proved by hand) but without a
retrievable characterisation: the exact parsimony length of a binary character matrix. Opus's toolkit here
is heuristic (stepwise addition, NNI/SPR rearrangement, compatibility cliques) plus weak bounds (one step
per informative character; disjoint incompatible pairs); the exact value needs enumeration or branch and
bound over 10,395 trees (8 taxa), which cannot be done by hand.
Tools (scratchpad mp/, copied into task10/verification): mp.py (enumeration of unrooted trees by leaf
insertion, Fitch on bitmask characters, bounds, max cliques, NNI), mp2.py (independent route: recursive
rooted shapes + Sankoff), mp_exact.py (self-contained program embedded in reference.txt with its output,
after the task06 consistency-check lesson), search_mp.py (random and tree-structured matrices; metrics:
unique optimum, bound gap, clique-tree score, NNI local optima, NNI-descent and stepwise-addition success),
build_spr.py + reeval.py (SPR adjacency index over all 10,395 trees; SPR-descent and stepwise-addition-
plus-SPR success), analyze.py, drawmatrix.py.
Findings from 763 unique-optimum instances: random 14-character matrices are highly deceptive (NNI descent
1 to 5 percent, stepwise addition 3 to 10 percent) but homoplastic (13 to 19 extra steps, CI about 0.45);
tree-structured low-homoplasy matrices (extra 8 to 9) are much easier (NNI 0.2 to 0.4, SA 0.3 to 0.8). SPR
steepest descent is strong: 40 to 60 percent success on moderate instances, below 25 percent only at
extra >= 14. Chosen instance: extra 11 (length 25, CI 0.56), NNI 0.04, SA 0.14, SPR 0.42, SA+SPR 0.50,
three clique trees at 26 that are NNI and SPR local optima, 37 trees at 26, unique optimum.
Reasoning for the choice: Opus's by-hand search is weaker than a full SPR descent, so an instance where
SPR succeeds about half the time should put a single Opus run near 30 to 40 percent, which is the band
(Summit needs 1 to 4 of 5) while leaving a reasonable chance that the single screen misses. Backup
instances with SPR success 0.13 to 0.25 (all at extra >= 14) are listed in scratchpad mp/reeval.pkl.
Results: Sonnet 0/1 (26, the clique tree, after a hand search of a dozen topologies). Opus 1/1 (25): it
read the matrix correctly, re-expressed the length of any tree as 2m - n1 + (extra steps of characters
costing 3 or more), where n1 is the number of character bipartitions that are edges of the tree, found a
25-step tree by hand, then proved 24 impossible by listing every set of five mutually compatible
bipartitions (four sets, each forcing characters 2, 7 and 14 to cost 3) and every set of four with every
fifth edge (each forcing one of 2, 3, 7, 14 to cost 3). Four minutes.
Lesson: with 14 binary characters on 8 taxa the "which bipartitions are edges" casework is small enough for
Opus to do exactly; the heuristic-search framing (NNI/SPR local optima) never came into play. If the family
is reused, the lever is to make that casework infeasible: 9 to 10 taxa, 18 to 22 characters, an optimum on
which several characters cost 3 (so the 2m - n1 accounting no longer pins the answer), and many compatible
4- and 5-sets of bipartitions. The tooling (search_mp.py with n=9, build_spr.py) supports it; SPR index for
9 taxa (135,135 trees x 132 neighbours) takes a few minutes in 8 parts. Declined by the user's rule.

## Summit verdict on task06 version 2 (2026-10-12): "unfair"
Consistency check passed after the program was embedded. Rollouts: Model A 3/5 correct (in band 1-4),
rubric 4.8/10 average, but the two misses were "cut off at the token ceiling, no readable answer", 40 min
each. Verdict: "The difficulty check could not finish this question. More than one attempt ran the whole
way to the limit of what the models can write without ever reaching an answer, and did it again when asked
a second time. That usually means the question asks for more working than it looks like: an unstated
assumption, a compound ask, or a derivation with no closed form. Tighten the question so a single line of
reasoning reaches the answer, then submit again." Status: needs revision, tag "unfair".
Lesson (decisive for the whole strategy): Summit does not accept difficulty that comes from the volume of
search. A miss that is a cut-off counts against the question, not for it. The difficulty has to sit in one
decisive step that a model can reach in a few thousand tokens and still get wrong. The construction-
difficulty lever (few optimal sequences) is therefore unusable, and so is any brute-force family.
Screen results for task08: Sonnet (local Sonnet 5.5) answered 5, correct. It used a counting bound on
five sites (distinct types <= sites + R + 1 gives 4, then an argument that equality fails, giving 5) and an
explicit five-crossover construction that places the S5 mutation on a lineage below a recombinant, i.e. the
very trick the mosaic proxy said models would miss. Opus result pending.
Opus (high) answered 6, wrong: bounds 2 and 4, then a hand SPR case analysis on the local trees left and
right of S6 that "proved" five impossible, then a six-crossover tree-plus-mosaic history. Exactly the
overshoot the mosaic proxy U = 6 predicted. Sonnet, however, found the five-crossover graph (recombinant
followed by the S5 mutation) and answered 5. Tally Opus 0/1, Sonnet 1/1.
Lesson: the U > R_min lever does move Opus (first Opus miss outside the tree-child family), but Sonnet's
construction is not constrained to mosaics, so the proxy does not predict Sonnet. A single-run screen is
noisy either way; the user decides.

Standing instruction from the user (2026-10-12): do not recommend or ask for the user's own experimental
field. Topic choice, design, verification and testing are entirely my job. Never end a report with a
request for the user's expertise; propose and build the next candidate myself.

## Session 2026-10-12: new direction, visual identification (cytogenetics ideograms)
Reasoning: every clean-math design is solved; search-based difficulty is "unfair". Untested weakness: fine
visual comparison. Candidate karyo1: G-banded ideograms of both homologues of chromosome 7 (real hg38
cytoband coordinates from the UCSC API, 44 bands, ~550-band level), normal homologue labelled with leader
lines, other homologue carrying a paracentric inversion with breakpoints inside bands (q22.1 at 55 % of its
length, q32.1 at 45 %). Key: inv(7)(q22.1q32.1). The decisive step is recognising the reversed band order
from widths and shades alone (no arm-length cue). Scripts: scratchpad karyo/ideogram.py (split, invert,
delete, staggered labels), karyo/chr7.tsv, chr2 data also fetched. Screen launched: 1 Opus high + 1 Sonnet.
karyo1 result: Opus and Sonnet both solved inv(7)(q22.1q32.1) by measuring band heights in pixels (both
~25 s). Helix handedness probe (left-handed tube with depth cues): both solved with a correct rule.
Verdict: clean synthetic figures hold no visual difficulty for these models; chirality included.
Next screens (1 Opus + 1 Sonnet each): agt1, P(gene tree = species tree) for (((A,B),(C,D)),E) with
internal branches 0.5, 0.3, 0.2 coalescent units, key 0.0966 (exact coalescent-history enumeration,
scratchpad agt/msc.py, matches simulation 0.0970 at n=4e5; sum over 105 topologies = 1). star1: Moran
fixation of r=1.5 mutant placed at a leaf of a 4-leaf star, key 0.509 (exact 32-state chain, agt/star.py);
traps 0.384 (well-mixed), 0.565 (large-N amplifier r^2), 0.439 (uniform start).
agt1 and star1 results: Sonnet and Opus both exact on both (gene-tree probability 0.0966 by conditioning on
lineage counts; star fixation 0.509 by the 10-state reduced chain, Opus even in closed form). Six screens
today, six solved. Clean bounded computations of any size are out, as are clean visual tasks.
Next: G1-type instance (answer 5, <=3 optimal binary sequences, parity bound tight so Opus closes fast,
but with common triples so the Sonnet-accessible 'no common triple => 5' argument fails). search_tc7.py
running (seeds 81-86).
search_tc7 result (stopped 2026-10-12 after ~63 CPU-min per seed): four instances with h_tc 5, parity bound
tight, 2 optimal binary sequences each, 3 to 4 common triples, three-tree MAAF bound 4:
H1 ((D,F),(((G,A),E),(C,B)))|(A,((F,G),(B,(E,(C,D)))))|(((B,C),G),((D,(E,A)),F)) pairwise [4,2,3];
H2 ((F,(A,E)),(G,((B,C),D)))|(((F,D),B),(E,(A,(G,C))))|((G,((F,((A,E),C)),D)),B) pairwise [3,3,3];
H3 (((F,A),B),((G,E),(D,C)))|((((B,A),E),C),(G,(F,D)))|((F,((D,((A,B),C)),G)),E) pairwise [3,3,3];
H4 (((B,A),F),((D,C),(G,E)))|((F,B),((E,C),(G,(D,A))))|(C,(D,(G,((A,(E,B)),F)))) pairwise [3,3,3].
tcsearch.py (argv override) builds and checks the 5-reticulation network for each (binary, tree-child,
displays all three).
Screens (same stem as tc_f2, figure by drawtrees.figure): H1 Sonnet 4 (wrong); Opus run 1 "none" (false
impossibility lemma, 9.5 min, no cut-off); Opus run 2 lost to a session restart; run 3 relaunched.
H2 Sonnet 4 (wrong); Opus run 1 lost to the restart; run 2 correct, 5, in 18 min: explicit 5-reticulation
network with a reticulation above the (A,E) pair plus r_B, r_C, r_D, r_G, verified tree by tree, and a
lower-bound argument via the classes of leaves below each reticulation (|L0|=3 or {A,E} class cases).
H1 Opus run 3 correct, 5, in 20 min: found the exact optimal sequence (F,G)...(D,C) final C, built the
network, pairwise bounds 4/2/3 by forest shapes, then a saving-count argument (18 tree nodes into 10 picks
needs 8 shared picks, at most 7 achievable). H1 now Opus 1 of 2, no cut-off in either run.
H3 (figure rerendered with xleaf 7 so the deep caterpillar labels clear the lines): Sonnet 4 (wrong,
"estimate"). H4: Sonnet 5 (right by an admitted guess: "every pair needs at least 3 ... at least one
more", no network, no proof). Opus runs on H3 and H4 pending.
lb_cert.py (scratchpad tc/) written: per pair of trees lists the maximal agreement sets and every partition
into <= b agreement sets with the reason it fails (overlap of spanned subtrees in tree 1 or 2, or a cycle).
This is the hand-checkable form of the pairwise bounds; with the restriction counting (a species picked
once/twice/three times is counted 3/5/6 times over the three restrictions, weight 4 means ten picks,
best shape (2,2,2,2,1,1) gives 26 < 27 = sum of (h_ij + 6)) it proves h_tc >= 5 without any sequence search.
H4 Opus correct, 5, in ~25 min: valid weight-5 sequence (E,G)(E,C)(E,B)(A,B)(A,D)(F,B)(B,G)(D,G)(D,C)(C,G)(B,G)
final G, plus a partner-ordering lower-bound case analysis over the final species. With Sonnet also right
(by guess) H4 is dropped.
H3 Opus run 1 WRONG: answer 6 in 41 min, no cut-off. It built a valid weight-6 sequence and then "proved"
weight 5 impossible by a partner-ordering argument (every leaf's partner in each tree fixed by the pick order;
"a shared pair two trees need in opposite orders must be used twice") with casework over the final leaf.
Sonnet 4 (forest estimate). Two further Opus runs on H3 launched to estimate the rate before deciding.
H3 Opus run 2 correct, 5, ~35 min: pairwise 3/3/3 by hand case splits, then the lower bound 2k >= 9 by the
"two of three trees share a parent at every reticulation" argument (valid for all binary networks, checked
and added to the solution Step 5 and reference.txt Section 4(c) as a second proof), and the mirror optimal
sequence (D,F)(F,A)(B,A)(E,A)(A,C)(D,C)(C,G)(F,G)(E,G)(C,G)(A,G). H3 now Opus 1 of 2, no cut-offs.
Lesson: for [3,3,3] instances the tree-child condition does not change the answer (h = h_tc = 5); the
difficulty is the construction plus resisting the forest answer 4 and false impossibility proofs.
H3 Opus run 3 WRONG: 6 in 27 min, no cut-off; weight-6 sequence ending at D, lower bound "my strong
expectation, not a proof" (E and F each said to need 2 reticulations). Final H3 tally: Opus 1/3, Sonnet 0/1,
no cut-off in any run (runs took 41, 19 and 27 min). Package task11 handed over to the user.
Platform refused task11 as a duplicate of an already submitted task (2026-10-12): the stem is byte-identical
to task06. Decision: task11 goes in as the revision of task06 (which sits in "needs revision", tag "unfair"),
by editing the task06 entry field by field: new image, answer 5, variants, solution, references text,
reference file, verify box, rubric, common wrong answers; question text untouched. Edit sheet:
tasks/task11-tree-child-hybridization-number-five-events/paste-for-edit.md. Lesson: a new instance under an
unchanged stem cannot be submitted as a separate task; either revise the existing entry or write a new stem.

## Session 2026-10-12: task11 built (H3 instance, key 5)

Folder tasks/task11-tree-child-hybridization-number-five-events. Stem identical to task06; figure h3
(TikZ, xleaf 7). Lower bound now fully on paper: pairwise 3 each via lb_cert.py tables (maximal
agreement sets 12/9/8; partitions into <= 3 agreement sets 87/141/198, every one fails by overlapping
spanned subtrees, none by a cycle), plus the restriction/counting lemma 27 <= 2P+6 => P >= 11 => weight
>= 5. No shaped search or configuration tables needed (the task06 Step 5 machinery is dropped). Upper
bound: sequence (D,F)(F,A)(A,B)(E,B)(B,C)(D,C)(C,G)(F,G)(E,G)(C,G)(B,G) final G, network with
reticulations above B,C,D,E,F, edge list and per-locus parent choices written out and hand-traced in
reference.txt Section 6. reference.txt (65 kB) embeds tcsearch.py (trimmed: H3 default, prints both
optimal sequences and the state after every pick, network check) and lb_cert.py with full outputs;
programs re-extracted from reference.txt and rerun: outputs identical. Rubric c1 5 / c2 1 / c3 2 / c4 2,
method-neutral; common wrong answers 4, 6, 3, "no such network". Zip:
tree-child-hybridization-five-events.zip. If the extra Opus runs make H3 look like 0/5, fall back to H1
(same package shape; its loci 1,2 certificate needs 640 partitions into <= 4 agreement sets, program
output only).

Rule from the user (2026-10-12): when the single Opus screen solves a task but there is a plausible way to
change the task so that Opus could fail, keep working on it (improve and re-screen) rather than stopping;
if the direction does not succeed despite the effort, say so and stop. Applied first to task10: Opus's
proof depended on the casework over compatible 4- and 5-sets of bipartitions being small; the follow-up
scales the instance (9 taxa, 18 to 20 characters) so that the casework is infeasible by hand.

## Summit consistency check on task08 (2026-10-12) and the revision

Verdict: fail, 3 blocking, 3 advisory, before any model rollout. Blocking: (1) the exclusion of all
four-event histories rested only on reported search output, with no self-contained proof or checkable
certificate; (2) the notes cite scripts that were not attached (only a text file can be uploaded, so the
scripts must be embedded in it, with command lines, inputs and version); (3) rubric c3 was
method-restrictive ("exhaustive or structured case analysis ... rather than by appeal to a lower bound")
and not decidable. Advisory: calling the exact minimum "the quantity R_min of Hudson and Kaplan" conflates
it with their R_M lower bound; Step 3 called S7-S9 "outside" the S1-S7 span although they share S7; the
image was checked cell by cell and found consistent with the solution.
Revision: a hand-checkable proof of R_min >= 5 was found and written into Step 5: the pattern-counting
(haplotype-bound) argument on sites S1,S3,S6,S7,S8 gives R' >= 4, and its equality case needs a derivation
of all ten restricted patterns from a sampled root by five single-site mutations and four single crossovers
of present patterns; a four-observation case analysis (h2 has no crossover parents; h7 needs h6; h9 needs
h6 or the S6 mutation from h10; h6 needs h7 or h8 and h9) shows no such derivation exists. tight.py
enumerates all derivations (none), parents.py prints the one-step parent table; both outputs and the full
source of every script, with command lines and the Python version, are now inside reference.txt. Rubric c3
rewritten as method-neutral; stem now says "Call this exact minimum R_min ... their four-gamete statistic
R_M is only a lower bound on it"; Step 3 states the composition rule explicitly.
General lesson for every future package: Summit's consistency check reads the notes as the only
verification material. Any computational claim needs the source embedded in the uploaded text file, exact
commands and inputs, and ideally a short independently checkable certificate; a lower bound should have a
written proof, and rubric criteria must not prescribe a method.

## Session 2026-10-12 (midday): task10 version 2, nine species

Scaling up required three fixes to the search: (1) random 20-character matrices on 9 taxa carry 22 to 32
extra steps and almost never a unique optimum, so the generator now mixes 3 to 6 distinct splits of a random
tree with distinct random characters; (2) enumerating all cliques of the compatibility graph is exponential
(11-cliques appear), so compatible 5- and 6-sets are counted by direct combination; (3) a bit-parallel Fitch
with precomputed post-orders (fastmp.py) scores all 135,135 trees in 0.25 s (18x faster), and an SPR
neighbour array (spr9_idx.npy, 135,135 x 132) makes SPR descent cheap. The uniqueness filter was relaxed to
at most four optimal trees because the question asks only for the length. Yield is low: about 2 usable
hits per 48,000 matrices (most have many optimal trees or too much homoplasy). Chosen: 65,96,241,445,441,
97,384,333,225,222,287,268,57,13,251,285,12,492 (unique optimum 34, CI 0.53, NNI 0.07, SPR 0.35, SA 0.13,
SA+SPR 0.26, six 6-cliques with trees at 35 to 38). Why the proof route should close: the optimum spends
three changes on characters 5, 10 and 13, so the accounting length = 2m - n1 + extras leaves slack over
every tree with n1 >= 3, and there are 86 compatible 4-sets and 34 compatible 5-sets to examine.
Results v2: Sonnet 0/1 (35, clique tree, ten topologies by hand). Opus 0/1 (35): read the matrix correctly,
found the 35-step clique tree ((C,D),I),(B,(A,E)),((F,G),H), proved 35 optimal for every tree containing
one of the four-taxon character splits by a two-sided bound, and covered the remaining trees only by
local search (single-taxon reattachments on the best trees), never reaching the unique 34-step tree
(A,(D,(C,I)),(E,(B,((F,G),H)))). The proof route that solved v1 was not available: the optimum has three
3-step characters and accommodates only five, so the edge-count accounting does not bound it.
Both screens missed; whether Opus's true rate is in band (1 to 4 of 5) or 0 of 5 is unknown from one
run; the local metrics (SPR descent 35 percent from random starts) suggest a non-zero rate. Offered the
full 5 Opus + 3 Sonnet protocol to the user for calibration before submission.

## task08 accepted (2026-10-12): what worked, for reuse

First task of the series to pass Summit's full pipeline, after the revision. The ingredients, in order of
importance:
1. A quantity with a weak retrievable toolkit. R_min (exact minimum recombinations) has three named lower
   bounds (four-gamete, haplotype, history), none tight on the chosen instance, and no retrievable
   characterisation that turns the exact value into a hand search (unlike cherry-picking sequences for
   hybridization numbers). Opus has to construct and then argue.
2. A construction trap measured by a proxy before screening. mosaic2.py computes the best "tree-compatible
   core plus mosaics" construction; the instance was chosen so that this gives key + 1 (6 versus 5) while
   every bound gives key - 1 or less (2, 4, 4). The local Opus run did exactly that: bounds 2 and 4, a false
   hand proof that 5 is impossible, answer 6. Sonnet found 5 locally, so Sonnet is not predicted by the
   proxy; Summit still passed it, so one local Sonnet success is not fatal.
3. Instance size just beyond hand reach: 10 haplotypes x 9 sites, R_min 5, unique four-gamete hitting set,
   two maximum tree-compatible cores. The 8 x 8 instance with R_min 4 (task07) was solved by both models.
4. Verification as Summit wants it: a written proof of the lower bound (pattern counting on a site subset
   plus a case analysis of the equality condition, found by enumerating subsets with tight.py), the full
   script sources, commands, inputs and Python version inside reference.txt, an explicit certificate for the
   upper bound (the ARG, forward-checked), and a method-neutral rubric. The first submission lacked these
   and was returned before any rollout.
5. Platform mechanics: a returned submission is edited field by field (no zip re-import); keep paste-ready
   copies of each changed field in fields/ and tell the user exactly what to replace. The References file
   can be removed and re-uploaded in the edit view.
Generator and proxy are in task08/verification (gen6.py, mosaic2.py); the same pipeline can produce further
instances at R_min 5 or 6. Vary the biological framing (plant, animal, viral sequences; haplotype matrix
drawn differently) so the duplicate check does not flag the next one.

## Session 2026-10-12 (afternoon): task12, second R_min instance after the task08 acceptance

Reused the task08 recipe unchanged (gen6.py with filters R_m, R_h, H_b <= 4, mosaic U >= 6, R_min = 5, ARG
certificate), twelve generator processes over 10 x 9, 11 x 9-10 (k = 5) and 10-11 x 9-10 (k = 6) for about
25 minutes: three k = 5 hits, no k = 6 hit. New screener tightscan.py lists every site subset on which the
counting bound equals k - 1 and no tight derivation exists (the hand-proof lever of task08); it reproduces the
task08 subset {S1,S3,S6,S7,S8}. Of the three hits only the 11 x 10 one was proof-ready (subsets
{S1,S2,S5,S6,S8} and {S1,S2,S5,S6,S8,S10}); a 10 x 9 hit with bounds 2/3/3 against R_min 5 (gap two) had no
proof-ready subset and was dropped, because the counting argument only reaches bound + 1.
Chosen instance (figure order, filled = 1): 0000010000 0011100000 0000111000 1101111100 1001111000
0000000001 1011111110 0011100001 0000111110 1011101110 1101111000. R_m 3 (hitting sets {S1|S2 or S2|S3,
S5|S6, S6|S7}), R_h 4 (sites S2,S4,S6,S8), H_b 4, U 6, R_min 5 (236,580 states eager, 8,052,632 plain), ARG
checked twice (arg_cert.py from the search history; fwd_check.py replays the Step 6 narrative written by hand).
The written lower-bound proof is shorter than task08's: h10 = 10101 on the five sites has no crossover parents
and pins the S6 mutation to the pair h7/h10; the trio h6, h1, h2 (00000, 00010, 00100) then needs S5 twice or
a circular pair of crossovers, whether or not the root lies in the trio. parents2.py (generalised parent
table, any site subset) prints the facts the proof cites.
Figure: new drawing style (drawhap2.py): each haplotype a horizontal line, sites as filled/open circles at
their physical bp positions, bases in a two-line header; first render had legend collisions at close sites,
fixed by stacking the two bases. Framing changed from plant base matrix to animal long-read haplotypes.
Screen: Sonnet (local 5.5) answered 5 by the marginal-tree chain (SPR moves between compatible blocks) with an
explicit 1 + 3 + 1 path and an admitted unproven lower bound, 10 minutes. Opus (high) answered 5 in 20 minutes: R_m 3,
haplotype bound 4 on {S2,S4,S6,S7,S8}, then exactly the tightness argument of Step 5 (every event creates a new
sampled type; the single crossover between S2 and S4 must create the type of h4, h5, h7 or h11; four cases),
and a five-crossover history with two unsampled intermediates. Both screens solved it.
Lesson: the proof-ready subset that Summit's consistency check needs is also the route Opus can find; the
instance is in the same regime as task08 (which screened 0/1 locally and landed in band), so a single solve
does not place it out of band, but there is no instance-level lever left at key 5. Key-6 generators
(11-12 haplotypes x 10 sites) restarted in the background to look for a harder instance.
Lesson on tooling: `pgrep -f gen6.py` inside a Bash call matches the calling shell itself; kill by listed PIDs
from `ps aux | grep "[g]en6"` instead.
