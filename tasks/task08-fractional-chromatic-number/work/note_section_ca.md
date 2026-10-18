
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
SCREEN_PLACEHOLDER
