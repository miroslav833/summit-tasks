# task03: smallest field over which the matroid of a drawn configuration is representable

Domain: Mathematics. Subdomain: Matroid theory: representability of rank-3 matroids (point-line configurations) over finite fields

Modality: image. Pattern: multi-step discrete reasoning over image content.

## Image

image.png (300 dpi, matplotlib, source work/make_figure.py). Necessity: The matroid is given only by the figure: which triples lie on a common line, including the four-point line, is not stated in the text, and the answer depends on the exact incidence structure (one incidence more or less changes the degeneracy set and the field).

## Question

The figure shows nine points, labelled $A$ to $I$, and eight lines drawn as straight segments. Let $M$ be the simple rank-$3$ matroid on $\{A, B, \dots, I\}$ whose dependent $3$-element sets are exactly the triples of points lying on a common drawn line (the line through $D$, $G$, $E$, $F$ contributes all four of its triples); every triple of points not on a common drawn line is independent.

A representation of $M$ over the finite field $\mathbb{F}_q$ is an injective map from the nine points to the projective plane $\mathrm{PG}(2, q)$ such that three points are collinear in $\mathrm{PG}(2, q)$ if and only if they lie on a common drawn line.

What is the smallest prime power $q$ for which $M$ has a representation over $\mathbb{F}_q$? Give a single integer.

## Answer

7   (also accepted: $7$, q = 7, $\mathbb{F}_7$, GF(7))

## Solution

Step 1: Read the incidences off the figure.
The eight lines are $ABE$, $ACD$, $AFI$, $BCG$, $CEI$, $CFH$, $DEFG$ and $GHI$. No drawn line contains two of the points $A, B, C, F$ together with a third of them, so these four points form a basis-like frame: every three of them are independent.

Step 2: Normalise a representation and construct the remaining points.
In any representation over any field, $A, B, C, F$ are four points of the projective plane with no three collinear, so after a projectivity we may assume $A = (1,0,0)$, $B = (0,1,0)$, $C = (0,0,1)$, $F = (1,1,1)$. The point $D$ lies on the line $AC$ and differs from $A$ and $C$, so $D = (1, 0, t)$ for some $t \neq 0$. Every other point is now forced as the meet of two lines through points already known:
$$E = AB \cap DF = (1-t,\, -t,\, 0), \qquad G = BC \cap DE = (0,\, 1,\, 1-t), \qquad I = AF \cap CE = (t-1,\, t,\, t), \qquad H = CF \cap GI = (t-1,\, t-1,\, 2t-1).$$
The eighth line and the four-point line are then automatic: $G$ was put on $DE$, so $D, E, F, G$ are collinear, and $H$ was put on $GI$. So the eight incidences impose no condition at all: for every $t$ (and every field) these nine vectors satisfy all the drawn collinearities. Conversely every representation arises this way for exactly one $t$.

Step 3: What can go wrong is degeneracy, not incidence.
A representation also needs the nine points to be distinct and every triple that is not on a drawn line to be non-collinear. Checking the $36$ pairs and the $76$ undrawn triples of the vectors above (each is a polynomial condition in $t$; the full list is in the verification notes) gives exactly five obstructions:
$$t = 0 \ (D = A), \qquad t = 1 \ (E = B), \qquad 2t = 1 \ (A, B, H \text{ collinear}), \qquad t = 2 \ (B, D, I \text{ collinear}), \qquad t^{2} - 3t + 1 = 0 \ (B, D, H \text{ collinear}).$$
For instance $\det(B, D, H) = \det\begin{pmatrix} 0 & 1 & t-1 \\ 1 & 0 & t-1 \\ 0 & t & 2t-1 \end{pmatrix} = t^{2} - 3t + 1$. So $M$ is representable over $\mathbb{F}_q$ exactly when $\mathbb{F}_q$ contains an element $t$ with $t \notin \{0, 1, 2, 1/2\}$ and $t^{2} - 3t + 1 \neq 0$.

Step 4: Go through the small fields.
$\mathbb{F}_2$ and $\mathbb{F}_3$: every element is $0$, $1$ or $2$. $\mathbb{F}_4 = \{0, 1, \omega, \omega^{2}\}$: here $2 = 0$ and $2t - 1 = 1$ never vanishes, but $t^{2} - 3t + 1 = t^{2} + t + 1$ vanishes at $\omega$ and $\omega^{2}$, so nothing is left. $\mathbb{F}_5$: $0, 1, 2$ and $1/2 = 3$ are excluded, and the last element $t = 4$ satisfies $16 - 12 + 1 = 5 \equiv 0$, so it is a root of $t^{2} - 3t + 1$ and $B, D, H$ become collinear. Hence no representation over $\mathbb{F}_5$. $\mathbb{F}_7$: $0, 1, 2$ and $1/2 = 4$ are excluded; the discriminant of $t^{2} - 3t + 1$ is $5$, which is not a square modulo $7$ (the squares are $1, 2, 4$), so the quadratic has no root and $t = 3, 5, 6$ are all admissible.

Step 5: The representation over $\mathbb{F}_7$.
With $t = 3$: $A = (1,0,0)$, $B = (0,1,0)$, $C = (0,0,1)$, $D = (1,0,3)$, $E = (5,4,0)$, $F = (1,1,1)$, $G = (0,3,1)$, $H = (1,1,6)$, $I = (2,3,3)$. These are nine distinct points of $\mathrm{PG}(2,7)$; the eight drawn lines hold by construction, and the determinants of the undrawn triples are all non-zero modulo $7$ (the verification notes list them). So the smallest field is $\mathbb{F}_7$.

Answer: $7$.

## Rubric

- c1 (5 pts, final answer): Gives $q = 7$.
- c2 (2 pts): Normalises four points in general position (such as $A, B, C, F$) to the standard frame and expresses all remaining points in terms of a single parameter (such as $D = (1, 0, t)$), showing that the eight drawn incidences impose no equation on the parameter.
- c3 (2 pts): Finds the complete list of degenerate parameter values, $t \in \{0, 1, 2, 1/2\}$ and the roots of $t^{2} - 3t + 1$ (or the equivalent list for another normalisation), each coming from two points coinciding or from an undrawn triple becoming collinear.
- c4 (1 pts): Shows that every element of $\mathbb{F}_5$ is degenerate (in particular that $t = 4$ is a root of $t^{2} - 3t + 1$ over $\mathbb{F}_5$), and that over $\mathbb{F}_4$ the quadratic kills the two elements outside $\mathbb{F}_2$.

Common wrong answers: 5, 3, 2, 4

## References box

Representability of matroids over small finite fields and the role of degeneracy conditions in coordinatisations: G. Whittle, On matroids representable over GF(3) and other fields, Transactions of the American Mathematical Society 349 (1997), 579-603. Representability over fields of given characteristic as a question about solutions of polynomial systems: T. Lazarson, The representation problem for independence functions, Journal of the London Mathematical Society 33 (1958), 21-25. The uploaded file verification_notes.txt contains the symbolic coordinatisation (all points as vectors in the parameter $t$, with the incidences checked identically), the complete list of degeneracy conditions, the admissible parameters over $\mathbb{F}_q$ for $q \le 13$, an independent brute-force search for representations in $\mathrm{PG}(2,q)$ for $q \le 7$, and the explicit representation over $\mathbb{F}_7$ with every determinant; the program is embedded with its output.

## Verify field (paste into 'Please explain where to find or verify the answer')

Sections 1 to 3 of verification_notes.txt give the coordinatisation, the five degeneracy conditions and the admissible parameters over each small field; section 4 is an independent brute-force search in PG(2,q) for q up to 7; section 5 embeds the program verify_key.py with its output, including the explicit representation over GF(7) with all determinants.

## Screen

Opus 1/1 correct (5 min, 59k tokens). Sonnet 1/1 correct (42 min, 104k tokens). Too easy; held back.