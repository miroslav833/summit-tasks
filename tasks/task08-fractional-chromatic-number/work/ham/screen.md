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
