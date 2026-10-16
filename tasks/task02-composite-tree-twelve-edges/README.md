# task02: degree of the field of moduli of a composite plane tree (12 edges)

Domain: Mathematics. Subdomain: Dessins d'enfants: Galois action on plane trees and Shabat polynomials (Belyi maps on the sphere)

Modality: image. Pattern: multi-step discrete reasoning over image content.

## Image

image.png (300 dpi, matplotlib, source work/ radial layout). Necessity: The tree and its planar embedding are given only by the figure. The text states neither the valencies nor the shape; the block structure of the edges, the valencies lying over each vertex of the quotient path, and the identification of the figure with one specific root of the quartic all have to be read off the drawing.

## Question

The figure shows a plane tree $T$ with twelve edges. Filled discs are black vertices, open circles are white vertices, and the cyclic order of the edges around each vertex is the one drawn. $T$ is isomorphic to its mirror image, so nothing depends on the orientation of the page.

A Shabat polynomial for $T$ is a polynomial $P \in \mathbb{C}[x]$ all of whose critical values lie in $\{0, 1\}$ and for which the set $P^{-1}([0,1])$, with the points of $P^{-1}(0)$ coloured black and the points of $P^{-1}(1)$ coloured white, is a plane tree isomorphic to $T$; the valency of a vertex equals the multiplicity of the corresponding root of $P$ or of $P-1$. Such a polynomial is determined by $T$ up to an affine substitution $x \mapsto ax + b$ with $a \neq 0$, and it can be chosen with coefficients in $\overline{\mathbb{Q}}$. For $\sigma \in \mathrm{Gal}(\overline{\mathbb{Q}}/\mathbb{Q})$ let $T^{\sigma}$ denote the plane tree of the polynomial obtained by applying $\sigma$ to the coefficients of such a $P$. The field of moduli of $T$ is the fixed field of the subgroup $\{\sigma : T^{\sigma} \cong T\}$ of $\mathrm{Gal}(\overline{\mathbb{Q}}/\mathbb{Q})$, where $\cong$ means isomorphism of plane trees.

What is the degree of the field of moduli of $T$ over $\mathbb{Q}$? Give a single positive integer.

## Answer

4   (also accepted: $4$, four, degree 4)

## Solution

Step 1: Read the tree off the figure.
Name the white vertex of valency $4$ $W$ and the black vertex of valency $4$ $B$. They are joined by the spine $W, b_2, w_1, B$, where $b_2$ is a black vertex of valency $2$ and $w_1$ a white vertex of valency $2$. Above $W$ hangs a black leaf $b_0$; to its left and right hang the arms $W, b_1, w_3$ and $W, b_3, w_4$, with $b_1, b_3$ black of valency $2$ and $w_3, w_4$ white leaves. Below $B$ hangs the chain $B, w_2, b_5$ with $w_2$ white of valency $2$ and $b_5$ a black leaf, and two white leaves $w_5, w_6$. So the black valencies are $4,2,2,2,1,1$, the white valencies $4,2,2,1,1,1,1$, and $\deg P = 12$.

Step 2: The monodromy group is imprimitive, so $P$ is a composition.
Let $\sigma_{\mathrm{b}}$ and $\sigma_{\mathrm{w}}$ be the permutations of the twelve edges that rotate the edges counterclockwise around the black and the white vertices. Split the edges into three classes of four:
$$\mathcal{A} = \{b_0W,\ b_2W,\ b_2w_1,\ b_5w_2\}, \qquad \mathcal{B} = \{b_1W,\ b_3W,\ Bw_1,\ Bw_2\}, \qquad \mathcal{C} = \{b_1w_3,\ b_3w_4,\ Bw_5,\ Bw_6\}.$$
$\sigma_{\mathrm{w}}$ fixes $\mathcal{C}$ (each white leaf carries one edge) and swaps $\mathcal{A}$ with $\mathcal{B}$: around $W$ the four edges alternate $b_0W, b_1W, b_2W, b_3W$, and at $w_1$ and $w_2$ the pairs are $b_2w_1, Bw_1$ and $Bw_2, b_5w_2$. $\sigma_{\mathrm{b}}$ fixes $\mathcal{A}$ (at $b_2$ it swaps $b_2W$ and $b_2w_1$, and the black leaves carry one edge) and swaps $\mathcal{B}$ with $\mathcal{C}$: at $b_1$ and $b_3$ it exchanges $b_1W, b_1w_3$ and $b_3W, b_3w_4$, and around $B$ the edges alternate $Bw_1, Bw_5, Bw_2, Bw_6$. So the monodromy group of $T$ preserves a system of three blocks of four edges, and by Ritt's theorem $P = Q \circ R$ with $\deg Q = 3$, $\deg R = 4$. The dessin of $Q$ is the quotient: on the blocks $\sigma_{\mathrm{b}}$ acts as $(\mathcal{B}\,\mathcal{C})(\mathcal{A})$ and $\sigma_{\mathrm{w}}$ as $(\mathcal{A}\,\mathcal{B})(\mathcal{C})$, the path with three edges. Up to an affine change of $y$ its Shabat polynomial is $Q(y) = 3y^{2} - 2y^{3}$, with black vertices $y = 0$ (valency $2$) and $y = 3/2$, and white vertices $y = 1$ (valency $2$) and $y = -1/2$.

Step 3: The inner quartic.
A vertex of the composite tree lying over a vertex $v$ of the path has valency $e \cdot \mathrm{val}(v)$, where $e$ is the ramification index of $R$ there. The black valencies $4,2,2,2,1,1$ therefore force $R^{-1}(0)$ to have ramification $(2,1,1)$ (giving $4,2,2$) and $R^{-1}(3/2)$ to have $(2,1,1)$ (giving $2,1,1$); the white valencies $4,2,2,1,1,1,1$ force $R^{-1}(1)$ to have $(2,1,1)$ and $R^{-1}(-1/2)$ to be unramified. So $R$ has exactly three critical points, all simple, with critical values $0$, $3/2$ and $1$. Use the affine freedom to put the critical point over $0$ at $x = 0$ and the one over $3/2$ at $x = 1$, and call the third one $s$. Then $R'(x) = k\,x(x-1)(x-s)$ and $R(0) = 0$, so
$$R(x) = k\left(\frac{x^{4}}{4} - \frac{(1+s)\,x^{3}}{3} + \frac{s\,x^{2}}{2}\right).$$
$R(1) = 3/2$ gives $k\,(2s-1)/12 = 3/2$, i.e. $k = 18/(2s-1)$, and $R(s) = 1$ gives $k\,s^{3}(2-s)/12 = 1$, i.e.
$$3s^{4} - 6s^{3} + 4s - 2 = 0 .$$
Conversely every root $s$ of this quartic gives a Shabat polynomial $Q(R_s(x))$ with the passport of $T$, and the plane tree of $Q \circ R_s$ is the preimage of the three-edge path under the four-sheeted cover $R_s$. The quartic has two real roots, $s = -0.8590$ and $s = 1.6628$, and a conjugate pair $s = 0.5981 \pm 0.3302\,i$. The four trees are pairwise non-isomorphic: the complex roots give a chiral pair (mirror images of each other), and the two real roots give two different mirror-symmetric trees, distinguished by the white vertex of valency $4$ being adjacent to one black leaf ($s = 1.6628$, the figure) or to two ($s = -0.8590$).

Step 4: The field of moduli.
The quartic $3s^{4} - 6s^{3} + 4s - 2$ is irreducible over $\mathbb{Q}$: it has no rational root (the candidates $\pm 1, \pm 2, \pm 1/3, \pm 2/3$ give the values $-1, 3, 6, 86, -23/27, -83/27, -14/27, -62/27$), and modulo $5$ it is $3(s^{4} - 2s^{3} - 2s + 1)$, which has no root in $\mathbb{F}_5$ and is not a product of two quadratics over $\mathbb{F}_5$, so it has no quadratic factor over $\mathbb{Z}$ either. Hence $\mathrm{Gal}(\overline{\mathbb{Q}}/\mathbb{Q})$ permutes the four roots transitively. For $\sigma$ in the Galois group, $T^{\sigma}$ is the tree of $Q \circ R_{\sigma(s)}$, which is isomorphic to $T$ exactly when $\sigma(s) = s$, because the four trees are pairwise non-isomorphic. So the stabiliser of $T$ is $\mathrm{Gal}(\overline{\mathbb{Q}}/\mathbb{Q}(s))$ and the field of moduli of $T$ is $\mathbb{Q}(s)$ with $s = 1.6628$, a field of degree $4$. Equivalently, the Galois orbit of $T$ consists of the four trees of Step 3.

Answer: $4$.

## Rubric

- c1 (5 pts, final answer): Gives $4$.
- c2 (2 pts): Shows that the Shabat polynomial of $T$ is a composition $Q \circ R$ with $\deg Q = 3$ and $\deg R = 4$, for instance by exhibiting the three blocks of four edges preserved by the monodromy group, with the three-edge path as quotient.
- c3 (2 pts): Reduces the inner quartic $R$ to a one-parameter family and obtains the equation $3s^{4} - 6s^{3} + 4s - 2 = 0$ (or an equivalent polynomial for the parameter) from the conditions that its three critical values are the vertices $0$, $3/2$ and $1$ of the path.
- c4 (1 pts): Shows that this quartic is irreducible over $\mathbb{Q}$ and that its four roots give four pairwise non-isomorphic plane trees, so that the Galois orbit of $T$ has exactly four elements.

Common wrong answers: 1, 2, 3

## References box

Plane trees and Shabat polynomials, uniqueness up to affine substitution, Galois action and field of moduli: G. B. Shabat and A. Zvonkin, Plane trees and algebraic numbers, Contemporary Mathematics 178 (1994), 233-275. Decomposition of a polynomial with imprimitive monodromy group: J. F. Ritt, Prime and composite polynomials, Transactions of the American Mathematical Society 23 (1922), 51-66. Compositions of plane trees and their Shabat polynomials: N. M. Adrianov and A. K. Zvonkin, Composition of plane trees, Acta Applicandae Mathematicae 52 (1998), 239-245. The uploaded file verification_notes.txt contains the derivation of the quartic $3s^{4} - 6s^{3} + 4s - 2$ for the inner factor, the proof of its irreducibility, a numerical tracing of the dessin of $Q \circ R_s$ for each of its four roots (compared with the figure: the figure is the tree for $s = 1.6628$, and the four trees are pairwise non-isomorphic), and an independent recognition of the Galois orbit from the normalised polynomials at 60 digits; the complete program is embedded with its output.

## Verify field (paste into 'Please explain where to find or verify the answer')

Sections 1 and 2 of verification_notes.txt give the quartic for the inner factor and its irreducibility; section 5 embeds verify_key.py, which rederives the quartic symbolically, traces the dessin for each of its four roots and compares it with the figure (the figure is the root s = 1.6628, the four trees are pairwise non-isomorphic), and section 4 recognises the Galois orbit independently from the normalised polynomials at 60 digits.

## Screen

Opus 1/1 correct (10 min, 85k tokens: composition from the valencies, Hurwitz count of the quartics, quartic in p^2 from power sums of the critical values, irreducibility mod 5). Sonnet 0/1 (answered 3, a guessed 'known example', no derivation). Held back.