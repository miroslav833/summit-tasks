# task08: number of Hamiltonian cycles of a drawn 28-vertex cubic graph

Mathematics, subdomain: Graph theory: enumeration of Hamiltonian cycles in a cubic graph. Earlier contents of this folder (fractional chromatic number, crack growth, test matrices, covering arrays, M/G/1 queue) are archived under work/.

## Question

Figure shows simple undirected graph on $28$ vertices, which are labelled $A$ to $Z$, $a$ and $b$, and its edges are straight segments drawn between circles. Where two segments cross, crossing point is not vertex, and those two edges do not meet there.

"Hamiltonian cycle" is cycle which passes through each vertex exactly once, and two Hamiltonian cycles are counted as same cycle when they use same set of edges, so starting vertex and direction of travel do not matter.

How many Hamiltonian cycles does this graph have? Give your answer as single integer.

## Answer

52

## Solution

Graph in figure has $42$ edges, which are $AG, AJ, AS, BK, BS, BV, CH, CL, CY, DI, DN, DW, EL, EP, EZ, FS, FX, FZ, GT, Gb, HJ, Ha, IM, Ib, JV, KQ, KU, LR, MO, MX, NT, NV, OQ, OZ, PU, PX, QY, RT, Ra, Ub, WY, Wa$, and each vertex has degree $3$, so graph is cubic, as $28 \cdot 3 / 2 = 42$. There are no triangles and no $4$-cycles in it, its girth being $5$, and it is not planar and has no symmetry except identity, so count cannot be shortened by faces or by symmetry and it has to be done as search.

Hamiltonian cycle uses two of three edges at each vertex, so edges which it leaves out form perfect matching, and perfect matching gives Hamiltonian cycle exactly when other $28$ edges close into one cycle and not into several. Search by hand runs on two rules, that when edge is left out the other two edges at both its ends are used, and that when two edges at vertex are used its third edge is left out, and branch is dropped when some vertex keeps fewer than two usable edges or when used edges close cycle shorter than $28$.

I split on edge which is left out at $D$, whose neighbours are $I$, $N$ and $W$, and then inside each case on edge left out at next vertex. When $DI$ is left out, so that $DN$ and $DW$ are used, split at $N$ gives $14$ cycles with $NT$ left out and $8$ with $NV$ left out, $22$ in all. When $DN$ is left out, split at $I$ gives $7$ with $IM$ left out and $7$ with $Ib$ left out, $14$ in all, and when $DW$ is left out, split at $I$ gives $9$ with $IM$ left out and $7$ with $Ib$ left out, $16$ in all. So graph has $22 + 14 + 16 = 52$ Hamiltonian cycles, and one of them, written from $A$, is $A\,G\,T\,N\,D\,I\,b\,U\,K\,B\,V\,J\,H\,C\,L\,R\,a\,W\,Y\,Q\,O\,M\,X\,P\,E\,Z\,F\,S$ and back to $A$, while verification notes list all $52$ of them.

As check, in cubic graph each edge lies on even number of Hamiltonian cycles (Smith's theorem, Thomason 1978), and here cycles through edges at $D$ number $52 - 22 = 30$ for $DI$, $52 - 14 = 38$ for $DN$ and $52 - 16 = 36$ for $DW$, which are all even and add up to $104 = 2 \cdot 52$, because each cycle uses two of three edges at $D$. Count was also done by two separate programs, depth-first search for cycles through $A$ and enumeration of all $98$ perfect matchings, and both of them give $52$.

So answer is $52$.

## Rubric

- c1 (5 pts, final answer): Final answer is $52$.
- c2 (1 pts): Response reads graph correctly, with $28$ vertices and $42$ edges and each vertex of degree $3$, and gives edge list or adjacency list which agrees with figure.
- c3 (3 pts): Response counts by exhaustive case split, either on edge which is left out at one vertex, for example $DI$, $DN$ or $DW$ at $D$, with forced edges carried through each branch, or on perfect matchings whose complement is one cycle, and each branch it reports ends either in full $28$-cycle or in contradiction.
- c4 (1 pts): Response counts each cycle once, and not once for each direction or each starting vertex.

Common wrong answers: 50, 48, 104, 51

## References box

Counting Hamiltonian cycles is #P-complete in general, so no formula is expected here and count is finite search, see L. G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8 (1979), 410-421. Parity check in solution, that each edge of cubic graph lies on even number of Hamiltonian cycles, is Smith's theorem, see A. G. Thomason, Hamiltonian cycles and uniquely edge colourable graphs, Annals of Discrete Mathematics 3 (1978), 259-268. Uploaded file verification_notes.txt gives adjacency list and counts cycles twice, by depth-first search and by perfect matchings, and both give 52, then it gives case split of solution, checks parity at every edge and lists all 52 cycles, while program and its full output come at end.

## Verify field

Section 2 of verification_notes.txt counts Hamiltonian cycles by depth-first search from A and finds 52 distinct edge sets, and section 3 counts them second way, as perfect matchings whose complement is one 28-cycle, where 52 of 98 perfect matchings are good. Section 4 gives case split of solution, 22, 14 and 16 when DI, DN and DW are left out, section 5 checks that each edge lies on even number of cycles and section 6 lists all 52 cycles, while program verify_key.py is embedded with its output.

## Image necessity

Text gives vertex labels, A to Z, a and b, but no edge, and adjacency of graph is given in figure only, so answer, which is property of that one edge set, cannot be found without reading all 42 edges from drawing.

## Screen

SUMMIT-MATCHING SCREEN (tools/summit_screen.py, Opus 5.5 at --effort max, 5 attempts, figure plus stem, 2026-10-18): 4/5 correct (52 in 10, 15, 16 and 30 minutes, 81k to 246k reported output tokens), 1 cut-off at the 128k output limit after 63 minutes. In band (1 to 4 of 5), one cut-off is below the unfair threshold of two. The max-effort runs counted by cutting the graph into two sides joined by six edges and pairing the crossings, with parity checks per edge.

Cheap subagent screen (figure plus stem, no tools), 2026-10-18. Family history in tasks/task13-hamiltonian-cycle-count/work/screen.md.

This graph (28 vertices, 42 edges, girth 5, not planar, trivial automorphism group, 14 crossings, key 52):
- Opus 0/3: 48 (DW 16, DN 12, DI 20), 50 (16, 12, 22), 51 (16, 14, 21). Every run read all 42 edges correctly and used the right method (edge left out at D, forced-edge propagation); the misses are cycles lost in the branches. 230 to 285 s, no cut-off.
- Sonnet 0/1: 50 (16, 14, 20), 240 s.

Size ladder (same family, non-planar, girth 5, trivial automorphism group):
- 18 vertices, key 21: Opus 2/2, Sonnet 1/1.
- 22 vertices, key 25: Opus 3/3, Sonnet 1/1.
- 24 vertices, key 38: Opus 3/3, Sonnet 1/1.
- 26 vertices, key 40: Opus 2/3 (40, 39, 40), Sonnet 1/1.
- 28 vertices, key 52: Opus 0/3, Sonnet 0/1 (this package).
Planar versions (16 and 20 vertices, fullerenes C26 and C28) were solved by face 2-colouring and symmetry and are not used.

