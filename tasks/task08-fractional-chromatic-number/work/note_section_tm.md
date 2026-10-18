
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
SCREEN_PLACEHOLDER
