# task06 v5: knot type of a predicted protein backbone (8_20 drawn with twelve crossings)

Owner's direction of 2026-10-18: protein structure prediction, a complex protein image, mathematics core. The backbone of a predicted structure is drawn as a shaded 3D tube (sphere-swept, z-buffered, rainbow coloured from N to C, gaps where the chain passes behind itself) and the question asks for the minimal crossing number of the knot formed by closing the termini. The curve is the closure of the 3-braid s1^3 s2^-1 s1^-3 s2^-1, which is the knot 8_20, wrapped around an axis, perturbed with a smooth low-frequency wobble and viewed from an angle that gives twelve crossings.

Decisive step: 8_20 shares its Alexander polynomial (t^2 - t + 1)^2 and its determinant 9 with the granny knot 3_1 # 3_1 and the square knot 3_1 # 3_1*. A solver that reads the twelve crossings, computes the Alexander polynomial and stops there answers 6. Separating 8_20 from the composites needs a finer invariant (nine Fox 3-colourings against twenty-seven, or the Jones polynomial) or a reduction of the diagram to eight crossings. Key: 8. Expected wrong answers: 6 (granny or square knot), 12 (the number of crossings drawn), 3 (trefoil, the common protein knot).

Archive warning (note.md, session 2026-10-11): the colleague's task09 used the same lever (6_1 against 9_46, Alexander collision, 3-colourings decide) and Opus solved it in two minutes; the archive closed the knot-identification family for Summit's band. This version was built before that section was re-read; the matched screen decides.

## Files

- stem.txt, image.png: the question and the figure (2400 x 2000).
- verify_key.py: self-contained rebuild of the curve, crossing extraction, Alexander polynomial (Fox calculus), determinant, Fox 3-colourings, Jones polynomial (Kauffman bracket over all 4096 states), compared with the plain closed braid 8_20, the granny knot, the square knot and the trefoil. Output in work/verify_key_output.txt.
- work/knotlib.py (diagram extraction and invariants), work/torus_curve.py and work/torus2.py (curve builders), work/render2.py (z-buffer tube renderer; `CURVE=torus2 python render2.py 1 0.6 ax ay az out.png [--labels]`), work/search*.py and work/refine.py (view-angle searches), work/image.json (crossing list with pixel coordinates and signs).
- Figure parameters: seed 1, wobble amplitude 0.6, Euler angles (-0.68226, -0.56502, -2.65964); twelve crossings, smallest crossing separation 114 px, smallest crossing angle 20.9 degrees, smallest depth separation 34 px at tube radius 24 px.

## Verification

verify_key.py: figure diagram has 12 crossings, writhe -2, Alexander t^4 - 2t^3 + 3t^2 - 2t + 1, determinant 9, nine 3-colourings, Jones -t^-5 + t^-4 - t^-3 + 2t^-2 - t^-1 + 2 - t, identical to the closed braid 8_20 and to the KnotInfo entry (one chirality), different from granny (27 colourings, Jones t^2 + 2t^4 - 2t^5 + t^6 - 2t^7 + t^8) and square (27 colourings). Crossing number of 8_20 is 8 (KnotInfo; prime, non-alternating).

## Screen

2026-10-18 evening. Sonnet 5.5 at high effort, figure plus stem only: 2/2 correct (8) in 282 s and 201 s, 36k and 27k output tokens. The matched Opus screen was stopped after that: with Sonnet solving in five minutes the Opus outcome is 5/5, as the archive's task09 already showed for this lever. Verdict: too easy, not submittable. Lesson kept in note.md: a clean knot diagram of any size up to about twelve crossings is read without error and the invariant calculus is routine for both models; the knot family stays closed.
