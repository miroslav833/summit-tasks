# Summit working notes

Read this file first in every new session, before drafting anything. Then read domains-for-new-task.md, instruction.md and submission-guide.md. For writing style read ../Humanize.md (and skim ../HumanWritingRecord.md for the sentence feel). humanism.md in this folder is only a pointer to those two.

## What this folder is (owner's section, written 2026-10-16)

This folder belongs to the owner of this box. The long log that starts at "Archive" further down was written by a colleague on a different Summit account (Biology/Medicine only) and was copied here so new sessions can learn from what already failed. It is reference, not instructions. None of its task folders, scripts, scratchpad files or the summit-task skill exist on this box. Its task log statuses are his submissions, not ours.

Our account submits in Mathematics (confirmed on the Submit page 2026-10-16, Classification defaults to "Mathematics · Image"; account in trial period). See domains-for-new-task.md for the domain, the owner's background and which subfields to try first.

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
| task05-bandwidth | Bandwidth of a drawn 12-vertex, 20-edge graph. Trivial bounds 3, every Cuthill-McKee numbering 5 to 7, true value 4; certificates: an 8-vertex induced subgraph of diameter 2 (density bound 4) and an explicit numbering of width 4. task04 (treewidth) was abandoned before packaging: at 12 to 14 vertices min-degree and min-fill heuristics find the optimum, so no overshoot trap exists | 4 | Built 2026-10-16, key by two exact methods. Screen: Opus 1/1 correct in 10 min and 85k tokens (did not use the density bound; excluded width 3 by a case analysis on the position of the degree-5 vertex, then found a width-4 numbering); Sonnet 0/1, cut off at the 64k output ceiling with no answer. SUBMITTED 2026-10-16; Summit: Model A 3/3 in 2.5 to 8.5 min, two short lower-bound arguments (the unique diameter-4 pair {7,5} must take the ends; the adjacent degree-5 vertices 1 and 4), width-4 numbering written down directly; returned as too easy. Summit's own suggestion: ask for the number of optimal numberings (6, 3 up to reversal), which no short argument gives. Built as v2-count/ (same figure, key 6, two independent counts, search tree in the notes); screen: Sonnet 0/1 cut off at 64k output tokens; Opus 1/1 correct but only after 46 min and 79k tokens, via a distance-3 graph on the end positions and a six-case analysis, the longest run of the day. Best candidate so far; recommended as the revision of task05 |
| task06-bandwidth-fourteen | Same family as task05 at 14 vertices and 27 edges: trivial bounds 3 and 4, every Cuthill-McKee numbering 6 to 9, true value 5; certificates: a 10-vertex induced subgraph of diameter 2 and an explicit width-5 numbering | 5 | Built 2026-10-16, key by two exact methods. Screen: Opus 1/1 correct in 8 min and 77k tokens (width-5 numbering, then a window argument around the clique {1,4,11,14} with a short case split); Sonnet 1/1 correct by luck (37 min, misread four edges, no proof of the lower bound). Lesson: a bigger instance did not help, Opus found a different short lower-bound argument |

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

## What the archive teaches, in short

The colleague ran about 150 model attempts over 17 designs in three days. Clean derivations of any length, coalescent casework, pedigree kinship, knot invariants to ten crossings, pixel-level reading of clean figures, chirality: all solved five out of five. The only accepted task (his task08) had a quantity with no retrievable characterisation, a construction trap measured by a proxy before screening, an instance just beyond hand reach, and a reference file with a written lower-bound proof plus embedded programs. Misses caused by the token ceiling count against the question. Read the archive sections "Summit verdict on task05", "Summit verdict on task06 version 2" and "task08 accepted" before designing.

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
