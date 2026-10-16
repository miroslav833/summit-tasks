# Summit submission guide (field by field)

This maps the Submit page in Summit to the instructions and to the `task.json` used by **Import .zip**. Read it next to the form. The Progress box on the right counts six things: category & subject, image, question text (30+ characters), answer key, solution (50+ characters), rubric (3–5 criteria, 10 points). The form will not submit until all six are green.

## Before you open the form

- Pick a topic where your own expertise matters and where you can verify the answer key by two independent routes. If you cannot verify it, do not submit it.
- Test the difficulty bar honestly: a PhD in the subfield should get it, a strong generalist should not. Difficulty should sit in one decisive reasoning step, not in the length of the arithmetic.
- Google the question and the answer. If either is findable in five minutes, change the question.
- Make the image yourself (TikZ, Python, BioRender, PyMOL, ChemDraw). Keep the original source file.

## Quickest route: Import .zip

1. Build a zip with the files at the top level (not inside a folder): `task.json` (required), `image.png` (optional, max 5 MB), `reference.txt` or `reference.pdf` (optional, max 10 MB). Any other filename is ignored.
2. Press **Import .zip** on the Submit page. The form fills in. Nothing is submitted yet.
3. Open every section and check it. The category is forced to one of your assigned domains if the zip says something else, and a rubric that fails to parse comes back empty, so look at those two first.
4. Press **Show LaTeX preview** under the question, the answer and the solution. Fix anything that does not render.
5. Press **Submit question**. Track it under Previously submitted. If it comes back, fix exactly what the note says and resubmit.

## Section 1: Classification

| Form field | What to enter | `task.json` key and allowed values |
|---|---|---|
| Category | The dropdown only offers **Biology/Medicine** for this account, so every submission goes there. | `domain`: `biology_medicine` (other values are rewritten by Summit with a warning) |
| Raw subject | Free text, the specific subfield, e.g. "Evolutionary biology / phylogenomics (multispecies coalescent)". Be specific; "Genetics" is too broad. | `subdomain` |
| Modality | **Multimodal (image preferred)** for a question with a figure; **Text-only** only if the stem stands alone. The form says about 20% text-only is a sensible target, not a limit. | `modality`: `image_reference` or `text_only` (for text-only, leave out `image`) |
| Image reasoning pattern | One of five: **Quantitative derivation from image-sourced data**; **Classification or identification from visual evidence**; **Multi-step discrete reasoning over image content**; **Figure/plot extraction with quantitative computation**; **Other image-grounded pattern (admin approval required)**. Pick the one that describes what the solver does with the picture. | `taskType`: `image_quantitative_derivation`, `image_classification_identification`, `image_multistep_discrete_reasoning`, `graph_extraction_computation`, `other_admin_approved` (or `not_applicable` for text-only) |
| Upload image | A clean PNG or PDF you made. No screenshots of text, no photos of hand drawings, nothing copied from a paper. | `image.entry`: `image.png` |
| Image source | How you made it, e.g. "TikZ (original species-tree drawing)" or "Original pedigree drawn in BioRender". | `imageCreationTool` |
| Why the image is necessary | One or two sentences saying which facts exist only in the picture. If the question could be answered without looking, the image fails review. | `imageNecessityExplanation` |

## Section 2: Question & answer key

| Form field | What to enter | `task.json` key |
|---|---|---|
| Question text | The complete stem: every assumption, every given value, definitions of any non-standard terms, an explicit pointer to the figure ("the figure shows…"), and the precision you want for a numeric answer. Math in LaTeX with `$…$`. Check the preview. | `questionText` (up to 20,000 characters) |
| Answer format | **Exact-match / short answer** for a number, expression or short string. **Multiple choice** needs 5 to 12 options with the correct one first. | `answerType`: `exact_match` or `multiple_choice`; options go in `multipleChoiceOptions` |
| Correct answer | The bare answer, nothing else: `0.3538`, not "the probability is about 0.3538". | `finalAnswer`: `["0.3538"]` |
| Answer precision | **Not set** or **No precision stated** when the answer is exact (an integer, a fraction, a string). **Significant figures** or **Decimal places** with the digit count whenever the question asks for a rounded number; it must match the wording of the question. | `answerPrecision`: `{"kind":"none"}`, `{"kind":"significant_figures","digits":4}` or `{"kind":"decimal_places","digits":2}` |
| Also accepted | Equivalent forms graders should accept: the closed-form expression, a percentage, an unrounded value. Use **Add another accepted form** for each. | `acceptableAnswerVariants` |

## Section 3: Solution

Numbered steps ("Step 1: …"), each with the formula written out, every symbol defined the first time it appears, and every intermediate number shown. Units carried through. Any assumption not already in the question gets flagged here, though it should really be moved into the question. Keep it purely scientific: no remarks about AI models. Cite peer-reviewed papers only. Field: `solution` (up to 30,000 characters).

## Section 4: Grading rubric

- Three to five criteria, points summing to exactly 10. Each criterion is one yes/no check that two graders would agree on.
- Exactly one criterion carries the **Final-answer criterion** radio button. It must state the actual answer ("Gives 0.3538"), never "gives the correct answer". Give it the most points, usually 5.
- The other criteria are specific intermediate results or decisive choices: a value, a classification, a formula applied correctly. Not "shows working", not "explains clearly".
- Common wrong answers: list the numbers a strong solver reaches by making the natural mistake, each one different from the key. Use **Add wrong answer** for each.
- `task.json`: `rubric.criteria` entries have `id`, `description`, `points`, `isFinalAnswer`; wrong answers go in `rubric.commonWrongAnswers`.

Labels applied automatically: Correct if the final-answer criterion is met; Partially correct if it is not but another criterion is; Incorrect otherwise.

## Section 5: References (optional but worth filling)

The explanation box ("Please explain where to find or verify the answer") is locked until a source file is uploaded. Upload a file first; a short text file with your own verification notes counts, as does a PDF you are allowed to share. Then write where the answer can be verified and cite the papers. In `task.json`: `referenceFile.entry` (file in the zip) and `referenceFile.fileName` (display name), plus the free-text `references`.

## Last look before pressing Submit

- Category and raw subject right; modality and reasoning pattern match the question.
- Image uploaded, clean, labelled, and the necessity box explains what only the image carries.
- Stem contains every assumption and the requested precision; preview renders.
- Answer bare; precision dropdown matches the stem; equivalent forms listed.
- Solution in numbered steps with all numbers shown.
- Rubric: 3–5 criteria, 10 points, one final-answer criterion stating the key, no wrong answer equal to the key.
- You have searched for the question and answer and found neither.
