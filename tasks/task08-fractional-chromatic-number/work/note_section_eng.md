
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
SCREEN_PLACEHOLDER
