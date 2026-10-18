# task06 v8: number of conformations consistent with distance data (three-helix bundle)

Built 2026-10-18 late evening after v5 and v7 (knot diagrams) were solved by Sonnet in minutes. Owner's constraints: protein structure, a complex protein image, mathematics core, solvable in under ten minutes when the right idea is seen.

Design: a 36-residue three-helix bundle (ideal helices 1-11, 15-25, 28-36; loops 12-14 and 26-27; work/gen4.py, seed 88) drawn as a rainbow tube with numbered C-alpha spheres (work/draw2.py). Known distances: every pair |i-j| <= 3 (chain geometry) plus 14 restraint pairs drawn as dashed lines and labelled with their residue pairs: (1,6) (3,8) (6,11) (8,13) (10,15) (13,18) (15,20) (17,22) (20,25) (22,27) (24,29) (27,32) (29,34) (31,36). Question: how many conformations (up to rotation and translation, mirror images distinct) have exactly these distances.

Decisive step: the quick model says each atom after the third has two mirror positions and each restraint removes one binary choice, giving 2^(33-14) = 524288. The correct reasoning: reflecting atoms v..36 through the plane of v-3, v-2, v-1 preserves all data unless a restraint pair (u,w) has u <= v-4 and w >= v. A restraint (u,w) therefore fixes every reflection vertex in (u+3, w], not just one. The free vertices are 4, 9, 16, 23, 30, and the count is 2^5 = 32 (Liberti, Lavor, Mucherino, Maculan, SIAM Review 2014; Liberti, Masson, Lee, Lavor, Mucherino, DAM 2014). Key: 32. Expected wrong answers: 524288, 2^33, 2, 1, 16 (forgetting the mirror pair).

Verification: verify_key.py rebuilds the coordinates from instance.pkl, runs branch and prune with all restraints (32 complete conformations, all pairwise different, every solution reproduces the data, smallest restraint violation of a rejected candidate 0.012 A so the instance is in general position), and lists for every vertex 4..36 which restraint fixes it; both routes give 32. Output in work/verify_key_output.txt.

Files: stem.txt, image.png (2400 x 2000), instance.pkl (coordinates, pairs), verify_key.py, work/bp.py (branch and prune, free-vertex rule), work/gen4.py (bundle builder and seed search), work/draw2.py (renderer, view 0.9 0.25 0.6), work/gen.py, gen2.py, gen3.py, draw.py (earlier smaller fragments, kept).

## Screen

2026-10-18 late evening. Sonnet 5.5 at high effort, figure plus stem only: 2/2 correct (32) in 38 s and 49 s, 4.5k and 5.6k output tokens. Run 2 split the 33 torsion signs into five blocks tied by the restraints and gave one free sign per block; run 1 counted four free relative signs times the mirror image. The matched Opus screen was stopped. Verdict: too easy, not submittable.
