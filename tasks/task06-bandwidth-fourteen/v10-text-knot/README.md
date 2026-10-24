# task06 v10: crossing number of a knotted backbone given as a crossing table (text-only)

Built 2026-10-24, the day Summit opened text-only submissions for Mathematics and Biology/Medicine (Diana's Slack post). No figure: the stem gives the thirteen crossings of a coarse-grained, projected and closed 184-residue backbone as a table (over residue, under residue, sign), which is a signed Gauss code and determines the knot. Question: minimal crossing number. Key 11.

Design. The knot is the alternating knot 11a246. Its Alexander polynomial (4t^4 - 10t^3 + 13t^2 - 10t + 4), determinant (41) and signature (4) coincide with those of the mirror image of 9_18, and 9_18 is the only knot with at most ten crossings having this Alexander polynomial (checked over the Rolfsen table). The table diagram has 13 crossings and no visible Reidemeister I or II move: a Reidemeister III move on the triangle of crossings 10, 11, 12 exposes the II pair 12, 13, and the resulting 11-crossing diagram is alternating and reduced, so the Kauffman-Murasugi-Thistlethwaite theorem gives 11. The trap is the standard pipeline Alexander polynomial, signature, table recall, which lands on 9_18 and answers 9.

How it was reached. Variant a (work/stem_a.txt) was a 13-crossing diagram of 10_132 with a kink and a visible II pair; Alexander and Jones polynomials equal those of 5_1 (trap answer 5), the honest route is the signature (0 against -4). Variant b (work/stem_b.txt) hid the reduction behind a III move. Both were too easy: every run computed the Gordon-Litherland signature unprompted and recalled that 5_1 and 10_132 are the only knots to ten crossings with that polynomial. Several runs wrote that an 11- or 12-crossing knot with the same Alexander polynomial and signature had not been excluded, and answered 10 anyway. Variant c (the shipped stem) was built to punish exactly that habit: the knot really is the larger one. work/scan11b.py lists the 122 eleven-crossing knots that share an Alexander polynomial with a smaller knot; 11a246 was chosen because its partner 9_18 is unique to ten crossings, the signatures agree up to mirror, and the knot is alternating, so the lower bound is a theorem rather than a table fact.

Verification. verify_key.py (numpy only): table to signed Gauss code to PD code, planarity by face count, Alexander polynomial by exact integer evaluation at t = 2, 3, 5, 7 (Bareiss), Gordon-Litherland signature from the Goeritz matrix (routine validated 84/84 against Seifert-matrix signatures of all prime knots to nine crossings, work/glsig.py), the III move and the II pair with the Gauss word after each, alternation and nugatory checks, Jones polynomials of both diagrams by the state sum (span 11). work/verify_snappy.py: SnapPy identifies the complement as K11a246 (volume 8.500584). Outputs in work/verify_key_output.txt and work/verify_snappy_output.txt and embedded in reference.txt.

Tools in work/: knotlib.py (copied from v5, PD crossing signs added), glsig.py, hidden.py (random Reidemeister moves until no I or II move is visible), make_variant.py (residue dressing and stem), r3.py (finds the III move that exposes the pair), reduce.py and solution_data_b.py (Goeritz data for the write-up), scan.py, scan_jones.py (Jones collisions to ten crossings with signatures), scan11.py, scan11b.py, scan12.py output pending, tables.py, bigdiag.py, inv_pair.py.

## Screen (Opus 5.5 high effort, Summit's setting; cap 100k tokens, text-only, no image)

Variant a: Opus 4/5 (the miss got the Goeritz correction term wrong and answered 5), Sonnet 2/2; 20-31k tokens, 3-4 min.
Variant b: Opus 5/5, Sonnet 2/2; 21-54k tokens, 3-7 min.
Variant c (shipped): Opus 1/5, Sonnet 1/2, no cut-offs. The four Opus misses all answered 9 in 83-150 s with 8-15k tokens: Alexander polynomial, determinant 41, recall of 9_18, two of them noting they had not found the reduction. The Opus solve (470 s, 48k tokens) found the III move, reduced to the alternating 11-crossing diagram, applied Kauffman-Murasugi-Thistlethwaite and checked the Seifert genus. The Sonnet solve (403 s, 54k tokens) recognised a 2-bridge structure and read the crossing number from the continued fraction of the reduced alternating diagram; the Sonnet miss (256 s) computed 41/17 for the 9-crossing 2-bridge knot and answered 9. In band, no cut-offs, every miss the designed trap.

## Question

See stem.txt (the table is part of the question text).

## Answer

11 (also accepted: $11$, crossing number 11, eleven)

## Solution, rubric, references

In build_package.py (Step 1 Gauss word and planarity; Step 2 Alexander, determinant, Goeritz signature and the 9_18 trap; Step 3 the III move and the II pair with Gauss words; Step 4 Kauffman-Murasugi-Thistlethwaite and the Jones span check). Rubric c1 5 points for 11, c2 2 points for the reduction to 11 crossings, c3 2 points for the lower bound (reduced alternating, or Jones span 11), c4 1 point for naming the 9_18 coincidence and why it does not decide. Common wrong answers 9, 13, 12, 10.

## How to submit

New entry. Classification Mathematics, Modality Text-only (no image, no image necessity box), subdomain as in task.json. Import backbone-crossing-table-crossing-number.zip, or paste question, answer and variants, solution, rubric, common wrong answers and references from task.json; upload reference.txt as verification_notes.txt. Check the LaTeX preview of the table.
