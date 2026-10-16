# Instructions

How to write a question that passes the checks.

## Overview

You're helping build a sample of graduate/PhD-level questions in your specific field. These samples will be used to probe the frontier of expert knowledge — questions a PhD in your field should be able to solve, but which today's strongest AI model gets right only some of the time.

Your job is to write one graduate/PhD-level question with a self-made image, a closed-ended answer, a detailed step-by-step solution, and a grading rubric. After you submit, Summit's automated checks test the question's quality and whether frontier AI models can solve it.

Create and submit the question in Summit. There are no automated checks to run before you submit: Summit's quality and difficulty checks run after submission, and a question they flag comes back to you with written reasons. Treat this page and the in-product checklist as your quality gate.

---

## Quality bar (read this first)

### Overview

We prioritize quality over quantity. A single excellent submission is worth more than five mediocre ones. If we cannot guarantee quality to our client, the project ends. Concretely:

### Graduate/PhD-level only

"Graduate-level" means the average person with a graduate degree in your subfield could solve it; the average person without one could not. If the content is taught in standard undergraduate courses (e.g., introductory organic chemistry, calculus, classical mechanics, general biology), it does not qualify, even if the calculation is long.

- **Too easy:** "Determine the hybridisation of the labeled carbon"
- **At the bar:** "Using Bent's rule, rank the s-character of the three C–C bonds at the bridgehead of the strained cage shown, and give the bond the largest s-character"

### Difficulty target

After you submit, Claude Opus 5.5 (high reasoning effort) attempts your question 5 times, independently. Your question is accepted only if it answers correctly on **1 to 4** of the 5 attempts.

- **5 of 5 correct:** too easy. It comes back to you to make harder.
- **0 of 5 correct:** too hard, or possibly a wrong answer key. It comes back to you to check.
- A weaker AI model, Claude Sonnet 5, also gets 3 attempts. If it solves the question on 2 or more of them, it comes back to you as too easy and for you to make it harder.

Difficulty must come from the reasoning, not from the length of the calculation. Bigger numbers, more algebra or more steps of the same kind do not make a question harder: the model either grinds through them reliably, or runs out of room and never answers. Neither measures what we want. The best questions have a step where the natural approach gives a plausible but wrong answer.

### One question, one answer

No compound questions ("compute X and Y"). No open-ended prompts ("explain why," "discuss," "provide a theory"). No subjective interpretation. The answer must be a single, objectively correct, unambiguous value, expression, or short string.

- **Wrong:** "Find the ground-state energy and sketch the wavefunction and comment on degeneracy"
- **At the bar:** "Give the first-order correction to the ground-state energy, in units of lambda/L"

If the same answer can be written in more than one form (e.g. an exact fraction and its decimal), list the other forms in **Also accepted**. If the question genuinely has more than one different correct answer, rewrite it so it has exactly one.

### Non-searchable

A determined searcher with Google, Wikipedia, and the standard textbook should not be able to find the answer in under 5 minutes. Build questions on top of recent research, niche specializations, multi-step synthesis of disparate facts, or your own research experience — not facts that exist verbatim on a webpage.

### Original work

Your own creation or a non-trivial synthesis of published material. No copying from textbooks, problem sets, exams, or online sources. Lightly reworded problems will be rejected.

### No prohibited content

No weapons of mass destruction (CBRN). No content requiring subjective or moral interpretation.

### Closed-ended and gradable

The answer must be checkable by comparing a string or a number. If grading it would require human judgement of an essay, it is out of scope.

### The image must be necessary

A diagram, graph, structure, or figure that is required to answer the question — not a screenshot of the question text, not a decorative illustration. If a reviewer can answer the question without looking at the image, the image fails.

Text-only submissions are allowed only when the stem stands alone and only within Summit's soft per-category no-image allowance. Prefer a necessary image whenever the domain calls for one.

---

## Submission components

### Overview

The Summit submission workspace asks for each of the following.

### Flow

1. Pick one of your assigned subject domains and a specific sub-topic.
2. Draft the question and answer key in Summit.
3. Create the image yourself and upload a clean PNG or PDF when the question requires one.
4. Write the numbered step-by-step solution with every formula and unit shown.
5. Write the grading rubric.
6. Complete every required submission field and submit.
7. If the automated checks or a reviewer return the question, fix what they name and submit again.

### Importing from a zip (optional)

Instead of typing every field, you can fill the form from a zip file: press **Import .zip** on the Submit page.

- Importing only fills the form. Check every section, then press **Submit** yourself.
- Everything on this page still applies to imported content, and every automated check runs after you submit.
- The domain must be one of your assigned domains. If it isn't, Summit switches it to an assigned domain and warns you; check it before submitting.
- If the rubric in the zip can't be read, the rubric starts empty. Write it again before submitting.

**Zip layout.** Put the files at the top level of the zip. Zip the files themselves, not a folder that contains them.

```
my-question.zip
├── task.json       required
├── image.png       optional: image.png | image.jpg | image.jpeg | image.webp | image.gif   (max 5 MB)
└── reference.pdf   optional: reference.pdf | .png | .jpg | .jpeg | .webp | .txt         (max 10 MB)
```

Files with any other name are ignored.

**task.json:**

```json
{
  "schema_version": "summit-task-package-v1",
  "task": {
    "domain": "mathematics",
    "subdomain": "Group theory",
    "modality": "image_reference",
    "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "TikZ",
    "imageNecessityExplanation": "Why the question cannot be answered without the image.",

    "questionText": "Full question stem.",
    "answerType": "exact_match",
    "finalAnswer": ["42"],
    "acceptableAnswerVariants": ["forty-two"],
    "multipleChoiceOptions": [],
    "answerPrecision": { "kind": "none" },

    "solution": "Step-by-step reasoning to the answer key.",
    "references": "Author, Title, Journal (year).",

    "rubric": {
      "criteria": [
        { "id": "c1", "description": "Gives the final answer 42.", "points": 5, "isFinalAnswer": true },
        { "id": "c2", "description": "First key reasoning step.", "points": 3, "isFinalAnswer": false },
        { "id": "c3", "description": "Second key reasoning step.", "points": 2, "isFinalAnswer": false }
      ],
      "commonWrongAnswers": ["36"]
    },

    "image": { "entry": "image.png" },
    "referenceFile": { "entry": "reference.pdf", "fileName": "source.pdf" }
  }
}
```

**Allowed values:**

| Field | Values |
|---|---|
| `schema_version` | Exactly `summit-task-package-v1` |
| `domain` | `mathematics`, `physics`, `chemistry`, `biology_medicine`, `computer_science_ai`, `engineering`, `humanities_social_science`, `other` (must be one of your assigned domains) |
| `modality` | `image_reference` or `text_only` (for `text_only`, leave out `image`) |
| `taskType` | `image_quantitative_derivation`, `image_classification_identification`, `image_multistep_discrete_reasoning`, `graph_extraction_computation`, `other_admin_approved`, or `not_applicable` for text-only questions |
| `answerType` | `exact_match` or `multiple_choice` |
| `answerPrecision` | `{ "kind": "none" }`, `{ "kind": "significant_figures", "digits": 3 }` or `{ "kind": "decimal_places", "digits": 2 }` |

**Rules:**

- **Exact match:** put the answer key in `finalAnswer`, and equivalent forms in `acceptableAnswerVariants`.
- **Multiple choice:** give 5 to 12 `multipleChoiceOptions`, with the **correct option first**. `finalAnswer` is not used.
- **Precision:** if the question asks for a precision, set `answerPrecision` to match it.
- **Rubric:** 3 to 5 criteria; points add up to exactly 10; exactly one criterion has `"isFinalAnswer": true`, and it states the answer key; none of the `commonWrongAnswers` may be the answer key.
- **Length limits:** question up to 20,000 characters, solution up to 30,000, each answer up to 5,000.

### 1. Subject domain

Chemistry, Physics, Biology, or Mathematics.

### 2. Subject sub-topic

The specific subfield (e.g., "Quantum Field Theory," "Asymmetric Organic Synthesis," "Algebraic Topology," "Structural Biology"). Choose something where your own expertise is load-bearing.

### 3. The question

The full question text, including all assumptions, given values, and definitions of any non-standard terms or notation. The question must be non-searchable. After reading the question alone (plus the image), a domain expert should know exactly what is being asked.

**Formatting rules:**

- Write mathematical content, symbols, equations, units, and chemical formulas in LaTeX (e.g., `$\Delta G^\circ = -RT \ln K$`) and verify the rendered preview.
- Precise technical language. A single ambiguous word can change the answer; choose carefully.
- State all assumptions in the question itself. Do not bury them in the solution. (e.g., "Assume ideal gas" or "neglect spin-orbit coupling")
- If the answer is numeric, state the precision you want in the question (e.g. "to three significant figures"). Grading is strict at the precision the question asks for.
- If you use non-standard jargon, define it. Or don't use it at all.
- Reference the image explicitly ("In the diagram below..." or "Using the structure shown...").

### 4. Image upload

A single image file (PNG or PDF) that is required to answer the question.

**You must create the image yourself.** Acceptable tools:

- Domain-specific software: ChemDraw, Desmos, Mathematica, TikZ/LaTeX, BioRender, GraphPad Prism, PyMOL, etc.

- Code-generated images using Python/R/etc.

**Not acceptable:**

- Images copied from the internet, textbooks, or papers (copyright + originality requirements).
- Screenshots of the question text itself.
- Hand-drawn images photographed with a phone (too messy).

**Image quality requirements:**

- Clean, high-resolution, no blur, no shadows, no off-center cropping.
- All necessary elements visible: axes labeled with units, structures fully drawn, components identified, no overlapping text.
- Shapes are clean (no wobbly circles, crooked lines, uneven proportions).
- No extraneous decoration. The image should look like it belongs in a textbook or peer-reviewed paper.

**Per-domain:**

- **Chemistry:** ChemDraw for structures/mechanisms; show stereochemistry explicitly; label every atom the question refers to.
- **Physics:** TikZ or Python for circuits, potentials, and geometries; mark coordinate axes, signs and directions; give scales.
- **Biology:** BioRender or PyMOL for pathways/structures; label nodes, edges and directions; if it is a tree, show branch calibration.
- **Mathematics:** TikZ/Asymptote or Desmos for graphs, knots, complexes; label all vertices, orientations and marked points.

### 5. Final answer

The exact answer, with no surrounding prose.

- **Bad:** The free energy change is approximately -42.3 kJ/mol, which is favorable.
- **Good:** `-42.3 kJ/mol`

LaTeX for any non-text content. Give the answer at the precision the question asks for. Prefer exact forms (fractions, surds, closed-form expressions) where the question allows them. Use SI units unless the field convention requires otherwise (state which). One answer only — pick the canonical form, and list any equivalent forms in **Also accepted (optional)** so they are graded as correct.

Two answer formats are allowed:

- **Exact-match:** a single number, expression, or short string.
- **Multiple-choice:** five or more options, exactly one correct.

### 6. Step-by-step solution

A complete, sequential derivation showing how to arrive at the answer. Format it as numbered steps:

```
Step 1: [What this step does, one line]
[Equations, reasoning, calculations]

Step 2: [Next step]
[...]
```

**Requirements:**

- Every formula written out explicitly, with each variable defined the first time it appears.
- Every calculation shown, with intermediate values.
- Units carried through and consistent throughout (SI unless field convention dictates otherwise).
- All assumptions made in the solution that were not stated in the question — flagged explicitly. (Ideally, they should already be in the question.)
- Precise technical language; no colloquialisms.
- No meta-commentary about AI, models, or "what the model got wrong." Keep the solution purely scientific.
- LaTeX for all non-text content.
- If you cite a source for a non-obvious fact, cite a peer-reviewed paper. Do not cite blogs, Wikipedia, textbooks, or lecture notes.

### 7. Grading rubric

Every question needs a rubric. It is used to grade AI responses to your question as correct, partially correct or incorrect, so it has to be objective: two experts applying it to the same response should always agree.

**Criteria (3 to 5, worth 10 points in total):**

- **Exactly one criterion is the final-answer criterion.** Tick it as the final answer. It must state the actual answer, e.g. "Gives $5/32$, or an exactly equivalent value". Do not write "gives the correct answer". Give it the most points (usually 5).
- **The other criteria are key intermediate results or decisive steps** from your solution, each one checkable: a specific value, identity, classification or choice. e.g. "Identifies the point group as $D_{3h}$", "Uses $F_A = 1/4$ for the common ancestor".
- Each criterion is one yes/no check, and criteria do not overlap.

**Not acceptable as criteria:**

- Subjective quality: "explains clearly", "good reasoning", "well organised".
- Things almost any attempt does: "attempts the problem", "shows some working", "uses perturbation theory".
- A vague final answer: "arrives at the right value".

**How a response is labelled** (the same rule for every question):

- **Correct:** right final answer (the final-answer criterion is met).
- **Partially correct:** wrong final answer, but at least one other criterion is met.
- **Incorrect:** wrong final answer and no other criterion met.

**Common wrong answers (optional, recommended):** the plausible wrong answers a strong solver would reach, e.g. by missing the key step. Each must differ from the correct answer. These are the traps that make the question hard, and reviewers use them when grading.

### 8. Automated checks

There are no checks to run in the editor. After you submit, Summit's automated checks:

- check the question isn't a duplicate of an existing one;
- review it for quality problems (ambiguity, answer-key alignment, missing information, image use);
- check the rubric: the final-answer criterion must match your answer, no common wrong answer may equal it, and criteria must be objective;
- check whether the question or its answer can be found online;
- test the question on AI models against the difficulty target.

A question the checks flag comes back to you with written reasons. Fix what they name and submit again.

You do not need to run models in separate consumer chats, upload model screenshots, or record model answers manually.

---

## Complete worked examples

### Overview

> *"About these examples: They show format, completeness, and submission structure only — not the difficulty bar. Your live submissions should be harder than these samples (deeper synthesis, less lookupable, more image-load-bearing)."*

### Physics

**Subject domain:** Physics

**Sub-topic:** Non-relativistic quantum mechanics / perturbation theory

**Task type:** #1 — image-anchored quantitative derivation

**Image** (described here; real submission uploads the file): A one-dimensional infinite square well of width $L$ on $[0, L]$, drawn with vertical walls, and a single narrow spike at $x = L/2$ labeled $V(x) = \lambda\,\delta(x - L/2)$ with $\lambda > 0$. The figure is required: the perturbation's location at the well centre is given only by the image.

**Question:** A particle of mass $m$ is in the infinite square well shown on $[0, L]$. A perturbation $V(x) = \lambda\,\delta(x - L/2)$, with $\lambda > 0$, is added at the position indicated in the figure. Working to first order in $\lambda$, give the energy shift of the $n$-th eigenstate for general integer $n \ge 1$. Express the answer in terms of $\lambda$, $L$ and $n$.

**Final answer:** $E_n^{(1)} = \dfrac{2\lambda}{L}$ for odd $n$, and $E_n^{(1)} = 0$ for even $n$.

**Step-by-step solution:**

1. **Unperturbed eigenstates.** The normalised eigenfunctions of the infinite square well on $[0, L]$ are $\psi_n(x) = \sqrt{2/L}\cdot\sin(n\pi x/L)$, $n = 1, 2, 3, \ldots$
2. **First-order energy shift.** For a perturbation $V(x)$, non-degenerate first-order perturbation theory gives $E_n^{(1)} = \langle\psi_n|V|\psi_n\rangle = \int_0^L |\psi_n(x)|^2 V(x)\,dx$.
3. **Evaluate the delta integral.** With $V(x) = \lambda\cdot\delta(x - L/2)$, the integral collapses to the integrand at $x = L/2$: $E_n^{(1)} = \lambda\cdot|\psi_n(L/2)|^2$.
4. **Value at the centre.** $|\psi_n(L/2)|^2 = (2/L)\cdot\sin^2(n\pi/2)$. $\sin(n\pi/2) = \pm 1$ for odd $n$ and $0$ for even $n$, so $\sin^2(n\pi/2) = 1$ (odd $n$), $0$ (even $n$).
5. **Assemble.** $E_n^{(1)} = \lambda\cdot(2/L)\cdot\sin^2(n\pi/2) = 2\lambda/L$ for odd $n$, and $0$ for even $n$. Even states have a node at the well centre, so the centred delta does not shift them.

**Answer:** $E_n^{(1)} = 2\lambda/L$ (odd $n$); $0$ (even $n$).

**Rubric:**

| # | Criterion | Points |
|---|---|---|
| 1 (final answer) | Gives $E_n^{(1)} = 2\lambda/L$ for odd $n$ and $0$ for even $n$ | 5 |
| 2 | Uses the normalised eigenfunctions $\psi_n(x) = \sqrt{2/L}\sin(n\pi x/L)$ | 1 |
| 3 | Reduces the first-order shift to $\lambda\,|\psi_n(L/2)|^2$ | 2 |
| 4 | Shows $\sin^2(n\pi/2)$ is 1 for odd $n$ and 0 for even $n$ (even states have a node at $L/2$) | 2 |

**Common wrong answers:** $2\lambda/L$ for all $n$ (misses the node of the even states); $\lambda/L$ (normalises with $1/\sqrt{L}$ instead of $\sqrt{2/L}$).

### Chemistry

**Subject domain:** Chemistry

**Sub-topic:** Molecular symmetry / vibrational spectroscopy (group theory)

**Task type:** #2 — image-anchored classification/identification (discrete count)

**Image** (described here; real submission uploads the file): A three-dimensional structural drawing of a phosphorus pentafluoride ($\mathrm{PF_5}$) molecule in its trigonal-bipyramidal geometry: one P atom at the centre, two axial P–F bonds drawn vertically, three equatorial P–F bonds at $120^\circ$ in the horizontal plane, with axial and equatorial fluorines visibly distinguished. The figure is required: the specific geometry (which fixes the point group) is given only by the image, not stated in words.

**Question:** For the molecule shown, determine the number of fundamental vibrational modes that are active in both the infrared and the Raman spectra. Give a single integer.

**Final answer:** $3$

**Step-by-step solution:**

1. **Assign the point group.** The trigonal-bipyramidal $\mathrm{PF_5}$ shown belongs to $D_{3h}$ (a $C_3$ principal axis, three $C_2$ axes, $\sigma_h$, $S_3$, $\sigma_v$).
2. **Build the reducible representation of all $3N$ Cartesian displacements** ($N = 6$, so $3N = 18$). Counting unmoved atoms per operation and multiplying by the per-atom contribution gives the characters of $\Gamma_{\text{tot}}$ over the $D_{3h}$ classes.
3. **Reduce using the $D_{3h}$ character table** to obtain $\Gamma_{\text{tot}}$ (dimension check: 18).
4. **Remove translations and rotations.** Translations span $A_2'' + E'$; rotations span $A_2' + E''$. Subtracting yields the vibrational representation $\Gamma_{\text{vib}}$ (dimension 12).
5. **Apply the activity rules.** IR-active modes transform as $A_2''$ or $E'$. Raman-active modes transform as the quadratics: $A_1'$, $E'$, $E''$. The only symmetry species active in both is $E'$.
6. **Count the $E'$ modes in $\Gamma_{\text{vib}}$:** there are 3. Because $D_{3h}$ has no centre of inversion, the rule of mutual exclusion does not apply, so these three $E'$ fundamentals appear in both spectra.

**Answer:** 3

**Rubric:**

| # | Criterion | Points |
|---|---|---|
| 1 (final answer) | Gives 3 | 5 |
| 2 | Identifies the point group as $D_{3h}$ | 2 |
| 3 | Identifies $E'$ as the only species that is both IR- and Raman-active, and finds 3 $E'$ modes in $\Gamma_{\text{vib}}$ | 2 |
| 4 | States that mutual exclusion does not apply because $D_{3h}$ has no centre of inversion | 1 |

**Common wrong answers:** $0$ (applies the rule of mutual exclusion as if there were a centre of inversion).

### Biology

**Subject domain:** Biology

**Sub-topic:** Population / quantitative genetics (pedigree inbreeding)

**Task type:** #1 — image-anchored quantitative derivation

**Image** (described here; real submission uploads the file): A standard pedigree chart (squares = males, circles = females, horizontal lines = matings, vertical drop-lines = offspring). Reading top to bottom: an unrelated founder couple produces two full-sib offspring who mate with each other to produce individual A; A then mates with two different unrelated, non-inbred partners to produce B and C; and B and C mate to produce the target individual X. The figure is required: the mating loop that makes A inbred, and the half-sib relationship of B and C through A, are shown only in the pedigree.

**Question:** Using the pedigree shown, and assuming all founders are non-inbred and unrelated, compute the coefficient of inbreeding $F_X$ of individual X. Give an exact fraction.

**Final answer:** $\dfrac{5}{32}$

**Step-by-step solution:**

1. **Identify the loop.** B and C share exactly one parent, A (their other parents are unrelated founders), so B and C are half-siblings and A is their only common ancestor.
2. **Wright's path formula.** $F_X = \sum (1/2)^{n_1 + n_2 + 1}(1 + F_A)$, summed over common ancestors, where $n_1$ and $n_2$ are the numbers of generational links from each parent of X up to the common ancestor.
3. **Count links.** From B up to A is 1 link; from C up to A is 1 link. So the path term is $(1/2)^{1+1+1}(1 + F_A) = (1/8)(1 + F_A)$.
4. **Correct for the ancestor's own inbreeding.** A is the offspring of a full-sib mating, so A is itself inbred with $F_A = 1/4$. The $(1 + F_A)$ factor is therefore $5/4$.
5. **Assemble.** $F_X = (1/8)\cdot(5/4) = 5/32$.

**Answer:** $5/32$

**Rubric:**

| # | Criterion | Points |
|---|---|---|
| 1 (final answer) | Gives $5/32$, or an exactly equivalent value | 5 |
| 2 | Identifies A as the only common ancestor of B and C, with path term $(1/2)^3$ | 2 |
| 3 | Uses $F_A = 1/4$ (A is the offspring of a full-sib mating) | 2 |
| 4 | Applies the $(1 + F_A)$ correction to the path term | 1 |

**Common wrong answers:** $1/8$ (omits the $(1 + F_A)$ correction).

### Mathematics

**Subject domain:** Mathematics

**Sub-topic:** Algebraic geometry (plane curve singularities, geometric genus)

**Task type:** #1 — image-anchored quantitative derivation

**Image** (described here; real submission uploads the file): The real locus of an irreducible complex projective plane curve $C$ of degree 6, drawn with its five singular points marked. Each singular point is labelled with its local analytic normal form: $P_1$ and $P_2$ are nodes ($x^2 - y^2 = 0$), $P_3$ is a cusp ($y^2 - x^3 = 0$), $P_4$ is a tacnode ($y^2 - x^4 = 0$), and $P_5$ is an ordinary triple point (three smooth branches meeting pairwise transversally). The figure is required: the number, and above all the analytic type, of each singularity is given only by the diagram, and the genus cannot be computed without it.

**Question:** Let $C$ be the degree-6 irreducible plane curve shown, whose only singularities are the five marked points with the indicated local types. Compute the geometric genus $g$ of $C$ (the genus of its normalisation). Give a single non-negative integer.

**Final answer:** $g = 2$

**Step-by-step solution:**

1. **Arithmetic genus.** For a plane curve of degree $d$, the arithmetic genus is $p_a = \binom{d-1}{2}$. With $d = 6$, $p_a = \binom{5}{2} = 10$.
2. **Genus drop from singularities.** The geometric genus is $g = p_a - \sum_p \delta_p$, where $\delta_p$ is the delta-invariant of the singularity at $p$. For a plane curve singularity with Milnor number $\mu$ and $r$ local branches, $\delta = \frac{\mu + r - 1}{2}$.
3. **Delta-invariants of the five points.** Node $A_1$ ($\mu = 1, r = 2$): $\delta = \frac{1+2-1}{2} = 1$; there are two, contributing 2. Cusp $A_2$ ($\mu = 2, r = 1$): $\delta = \frac{2+1-1}{2} = 1$. Tacnode $A_3$ ($\mu = 3, r = 2$): $\delta = \frac{3+2-1}{2} = 2$. Ordinary triple point $D_4$ ($\mu = 4, r = 3$): $\delta = \frac{4+3-1}{2} = 3$ (equivalently $\binom{3}{2} = 3$ for an ordinary triple point).
4. **Total delta.** $\sum_p \delta_p = 1 + 1 + 1 + 2 + 3 = 8$.
5. **Assemble.** $g = p_a - \sum_p \delta_p = 10 - 8 = 2$.

**Answer:** $g = 2$

**Rubric:**

| # | Criterion | Points |
|---|---|---|
| 1 (final answer) | Gives $g = 2$ | 5 |
| 2 | Uses arithmetic genus $p_a = 10$ for degree 6 | 1 |
| 3 | Uses $\delta = 2$ for the tacnode and $\delta = 3$ for the ordinary triple point | 3 |
| 4 | Finds total $\sum_p \delta_p = 8$ | 1 |

**Common wrong answers:** $5$ (treats all five points as nodes); $4$ (gives the tacnode $\delta = 2$ but the triple point $\delta = 1$).

---

## Difficulty flavour by task type

What a submittable hard question feels like:

- **#1 derivation:** a setup needing synthesis across two subfields, or a non-obvious framework choice — e.g. equilibrium conformer population from molecular-mechanics strain energies plus a Boltzmann factor, where models default to DFT ΔG values.
- **#2 classification:** an object where the answer turns on ruling out a near-neighbour category — e.g. the named vicariance event that fits an inferred divergence date from a calibrated molecular clock, not a one-glance label.
- **#3 reasoning:** a process with several plausible answers where the right one depends on research-grade evidence — e.g. the step with the most carbanion character in a catalytic cycle, triangulated from a Hammett ρ and a kinetic isotope effect given in the figure.
- **#4 graph extraction:** a plot where the reading is non-trivial and feeds a graduate computation — e.g. extract a rate from a non-linear Arrhenius plot you generated, then compute an activation entropy.

---



## Final checklist before submitting

- [ ] Question is at graduate/PhD level (not undergraduate)
- [ ] Difficulty comes from the reasoning, not from long calculation
- [ ] Single question, single answer, not compound
- [ ] All assumptions stated in the question, including the required precision for numeric answers
- [ ] Non-searchable (you Googled it yourself and confirmed)
- [ ] Original work, not copied or lightly paraphrased
- [ ] LaTeX used for all non-text content
- [ ] Image or text-only within the soft no-image allowance
- [ ] Image is clean, labeled, and necessary to answer the question (when used)
- [ ] Final answer is bare (no fluff); equivalent forms listed in Also accepted
- [ ] Solution has numbered steps with every formula and calculation written out
- [ ] Units are SI and consistent throughout
- [ ] Rubric: 3–5 objective criteria, 10 points total, one final-answer criterion that states the actual answer
- [ ] Common wrong answers listed, each different from the correct answer


Submit. Track the final status from Previously submitted.

Questions about the process go to the project lead. Questions about your subject matter — you're the expert.
