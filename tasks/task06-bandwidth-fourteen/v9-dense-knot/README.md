# task06 v9: knot type of a dense 200-residue predicted protein fold

Built 2026-10-18 night after the owner rejected the clean diagrams of v5 and v7 ("your image was so simple"). Same question as v5 (minimal crossing number of the closed backbone) but the figure is a full protein cartoon: 200 C-alpha atoms, eleven helices, five strands and loops, drawn as a shaded rainbow tube with 41 crossings in the projection. The lever is dense topology: the chain has to be traced through a crowded fold, or coarse-grained (helices replaced by their axes) before any invariant can be computed.

Construction (work/): coarse.py, closure of the 3-braid s1^3 s2 s1^-1 s2 (the knot 5_2, Jones polynomial checked); tighten.py, rope-style relaxation to a compact axis curve with clearance 1 unit (length to clearance ratio 56); decorate.py, scale 9.2 A per unit and C-alpha placement along the axis (helix radius 2.3 A, rise 1.5 A, 100 degrees per residue; strands and loops within 1 A of the axis); search_view9.py, views where the straight closure between the termini carries no crossing and inter-element crossings are well separated; finalize.py, Alexander polynomial of the drawn chain by exact integer evaluation; render_dense.py, z-buffer tube renderer with gaps. Figure view (-0.2922, -2.2994, -0.6088), 41 crossings, 26 between parts more than six residues apart, smallest depth separation among those 7.0 A, smallest crossing angle 22 degrees, closure crossing-free.

Key: 5 (the knot is 5_2, as in the UCH-L3 family of real knotted proteins). Expected wrong answers: 3 (the usual protein knot), 0, 41.

Verification: verify_key.py. Axis curve is 5_2 by its Jones polynomial; chain stays within 2.3 A of an axis whose distinct parts are 9.2 A apart (isotopy margin 4.6 A); the drawn chain plus closure has the same Alexander polynomial as the axis up to a unit (exact evaluations at t = 2, 3, 5, 7) and determinant 7. Output in work/verify_key_output.txt.

## Screen

View D (image.png, 41 crossings), 2026-10-18 night: Sonnet 5.5 high 1/2 (5 in 188 s by plausibility; 3 in 190 s after giving up on the dense regions); Opus 5.5 max effort 0/5, every run killed at the 600 s tool timeout (the tool now enforces the ten-minute rule). Sparser views of the same fold, image_F.png (31 crossings) and image_E.png (21 crossings), screened next. View F: Sonnet 2/2 in about 60 s (coarse-grained to six crossings, determinant 7, 5_2); Opus max effort 0/5 at 600 s. View E: Opus max effort 0/3 at 600 s. Longer Opus runs (1800 s; and high effort as on Summit) on F and D. View D, Opus high effort (Summit's setting), 1800 s cap: 2/3 correct (5 in 345 s and 629 s with 32k and 63k tokens; 3 in 280 s with 26k tokens), no cut-off; all under the owner's 100k token criterion. Five runs in total: 3/5 correct, 2 wrong (both 3), 0 cut-offs, 26k to 63k tokens, 5 to 11 minutes: in band at Summit's setting and under the owner's 100k token rule. The wrong runs assumed the orange helix cluster lies on top of the strands it crosses and reduced the diagram to a trefoil.

## Question

The figure shows the $C_\alpha$ backbone of a $200$-residue protein as returned by a structure prediction model, drawn as a smooth tube coloured from blue at the N terminus to red at the C terminus; helical segments appear as coils. The drawing is a projection of the three-dimensional structure. Where one part of the chain passes in front of another part, the part behind is interrupted. The two termini lie on the outside of the structure, and the dashed segment joins them; it closes the chain into a closed curve and adds no crossing.

The closed curve is a knot. What is the minimal crossing number of this knot, that is, the smallest number of crossings in any diagram of its knot type? Give a single integer.

## Answer

5 (also accepted: $5$, crossing number 5, five)

## Solution

Step 1: Reduce the drawing to the path of the chain.
The chain runs from the N terminus (blue) to the C terminus (red) through 8 helices and 5 strands joined by loops. Crossings between consecutive turns of one helix, and crossings of a loop with its own neighbouring residues, never change the knot type, because each helix is an unknotted coil that can be straightened to its axis without passing through any other part of the chain, because the chain never comes closer to another part than a helix diameter. So replace every helix by its axis and every strand and loop by a smooth line through it, and keep only the crossings between different parts of the chain. The dashed closure adds no crossing.

Step 2: Record the remaining crossings.
Following the chain from N to C in the drawing, 12 crossings between different parts remain, with the part in front read from the gaps in the tube. The yellow helix around residue 133 passes over the dark blue loop around residue 3, sign $+1$. The dark blue helix around residue 17 passes over the orange loop around residue 144, sign $+1$. The orange helix around residue 162 passes over the dark blue strand around residue 24, sign $+1$. The blue strand around residue 25 passes over the cyan strand around residue 67, sign $-1$. The red helix around residue 168 passes over the blue strand around residue 26, sign $-1$. The green helix around residue 81 passes over the blue loop around residue 30, sign $-1$. The green loop around residue 92 passes over the blue helix around residue 41, sign $+1$. The red helix around residue 175 passes over the blue loop around residue 47, sign $+1$. The cyan loop around residue 63 passes over the orange strand around residue 147, sign $+1$. The orange loop around residue 157 passes over the cyan loop around residue 65, sign $+1$. The orange helix around residue 164 passes over the cyan strand around residue 68, sign $-1$. The red strand around residue 192 passes over the yellow loop around residue 126, sign $+1$. Numbering the crossings in the order of the first visit gives the Gauss word 1U 2O 3U 4O 5U 6U 7U 8U 9O 10U 4U 11U 6O 7O 12U 1O 2U 9U 10O 3O 11O 5O 8O 12O (O over, U under), which is the diagram of a single closed curve with 12 crossings.

Step 3: Compute an invariant from the diagram.
Label the 12 arcs between consecutive undercrossings and write, for each crossing, the colouring relation $2a_{\rm over} = a_{\rm in} + a_{\rm out}$. Dropping one relation and one arc and taking the determinant gives the knot determinant $7$. The Alexander polynomial from the same crossing data (Fox calculus with the crossing signs listed above) is $\Delta(t) = 2t^2 - 3t + 2$.

Step 4: Identify the knot and its crossing number.
A knot with at most four crossings is the unknot, the trefoil or the figure-eight knot, with determinants $1$, $3$ and $5$. Determinant $7$ excludes all three, so the crossing number is at least $5$. The only knots with five crossings are $5_1$ (determinant $5$, $\Delta = t^4 - t^3 + t^2 - t + 1$) and $5_2$ (determinant $7$, $\Delta = 2t^2 - 3t + 2$), and the diagram of Step 2 reduces to the standard five-crossing diagram of $5_2$ (the Jones polynomial of the diagram, $t - t^2 + 2t^3 - t^4 + t^5 - t^6$, is that of $5_2$, and the Jones polynomial separates all knots with at most nine crossings). The backbone forms the knot $5_2$, the knot type of the ubiquitin hydrolase UCH-L3 family, and its minimal crossing number is $5$.

Answer: $5$.

## Rubric

- c1 (5 pts, final answer): Gives $5$.
- c2 (2 pts): Reduces the drawing to a knot diagram by replacing helices by their axes and keeping only the crossings between different parts of the chain, and computes an invariant of that diagram (determinant $7$, Alexander polynomial $2t^2 - 3t + 2$, or an equivalent) that shows the knot is not the unknot, trefoil or figure-eight knot.
- c3 (2 pts): Identifies the knot as $5_2$ (not $5_1$, not a trefoil) and justifies the crossing number, at least $5$ because the determinant is not $1$, $3$ or $5$, and at most $5$ because the diagram reduces to, or the invariants match, the five-crossing knot $5_2$.
- c4 (1 pts): States that crossings inside a single helix and the dashed closure do not affect the knot type.

Common wrong answers: 3, 0, 41, 6

## References box

For knot types of proteins and the reduction of a backbone to a knot diagram see W. R. Taylor, A deeply knotted protein structure and how it might fold, Nature 406 (2000), 916-919, and M. Jamroz, W. Niemyska, E. J. Rawdon, A. Stasiak, K. C. Millett, P. Sulkowski and J. I. Sulkowska, KnotProt: a database of proteins with knots and slipknots, Nucleic Acids Research 43 (2015), D306-D314. The $5_2$ knot of the ubiquitin hydrolase UCH-L3 is PDB entry 1XD3. Knot tables with determinants, Alexander and Jones polynomials are in D. Rolfsen, Knots and Links, AMS Chelsea, 2003, Appendix C, and the KnotInfo table (knotinfo.math.indiana.edu). Fox colourings and the determinant are explained in R. H. Fox, A quick trip through knot theory, in Topology of 3-manifolds, Prentice-Hall, 1962. The uploaded file verification_notes.txt gives the construction of the backbone (axis curve, helices, strands and loops with coordinates), the coarse-grained diagram in the view of the figure with every crossing located on the chain, the determinant, Alexander and Jones polynomials computed from that diagram, and an independent check from the full 200-residue chain in the same projection (its Alexander polynomial agrees with the axis curve's). The programs are embedded with their output.

## Image necessity

The structure exists only in the figure. The path of the chain, which parts pass in front of which, and the positions of the termini are not given in the text, and the knot type depends on them.

## Verify field

Section 2 of verification_notes.txt lists the twelve crossings of the coarse-grained diagram with the residues involved and the part in front, the Gauss word, the determinant 7, the Alexander polynomial 2t^2 - 3t + 2 and the Jones polynomial of 5_2. Section 3 checks the full 200-residue chain in the same projection independently (same Alexander polynomial up to a unit, determinant 7, no crossing on the closure). Section 4 embeds the standalone program with the coordinates and its output.

## How to submit

New entry, or the revision slot the owner chooses. Classification Mathematics, subdomain as in task.json. Upload image.png, paste the question, answer and variants, solution, rubric, common wrong answers and references, upload reference.txt as verification_notes.txt, and put the image necessity text in its box. Zip: knotted-protein-backbone-crossing-number.zip.
