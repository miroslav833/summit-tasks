# Domains for new tasks

Read with note.md. This file says which domain the owner of this folder submits in and what background can be drawn on.

## Submission domain

Mathematics. In task.json: `"domain": "mathematics"`.

Confirmed on the Submit page on 2026-10-16: the Classification row shows "Mathematics · Image" by default, so Mathematics is the assigned domain and image is the default modality. The colleague whose log sits in note.md had an account locked to Biology/Medicine; that does not apply here.

The account is in a trial period (banner on the Submit page: the team reviews new members' work closely). The first few submissions carry more weight than usual, so no rushed packages.

Engineering (`"domain": "engineering"`) has not been seen in the Category dropdown. Do not use it unless the owner reports it is offered.

## Owner's research background

Materials engineering, titanium alloys. Publications:

- Influence of Alloying Elements in Fatigue Properties of Alpha/Beta Titanium Alloys
- The Effects of Oxygen on the Fatigue Behaviour of MIM Ti-6Al-7Nb Alloy
- Porous titanium processed by powder injection moulding of titanium hydride and space holders
- Influence of Oxygen on the Fatigue Behavior of Ti-6Al-7Nb alloy
- Porous titanium by powder injection moulding of titanium hydride and PMMA space holders

Topics covered there: high-cycle fatigue of alpha/beta Ti, interstitial oxygen and its effect on strength and fatigue limit, metal injection moulding of TiH2 powder, porosity control with space holders (PMMA), stiffness and strength of porous titanium.

## How the publications may be used

They are background, not source material. instruction.md allows questions built on "your own research experience", so a question can grow out of the physics or the modelling in these papers. It cannot reuse their data, figures, or conclusions.

Allowed:
- A question that needs a modelling choice an expert in this area makes from experience (which fatigue life relation, which porosity scaling, which strengthening law), with numbers invented for the question.
- A self-made figure (matplotlib) drawn from invented data.
- Mathematics questions that borrow the setting from this field: an S-N curve as a fitted power law, a Weibull distribution of pore sizes, a lattice model of a porous solid, shrinkage of a sintered body as a geometry problem.

Not allowed:
- Any number, table or figure copied from a paper. The findability check searches for the answer; anything in a published paper is findable.
- A question whose answer is a stated result of a paper.
- Author names, journal names or anything that points to the owner. The references box can cite published papers, but the task must read as an anonymous expert's question.

## Mathematics subfields to try first

These give an exact answer that can be checked by two independent routes, and the colleague's log has not burned them out:

- Combinatorics and graph theory: chromatic polynomials, matching counts, Tutte polynomial evaluations on a drawn graph. Trap: a symmetry that the natural count double-counts.
- Algebraic geometry of plane curves: geometric genus from drawn singularities (the instruction.md example is this; go harder, with non-ordinary singularities whose delta needs a resolution).
- Low-dimensional topology: knot and link invariants from a drawn diagram. Warning from the log: Opus does determinant, Alexander and Jones polynomial by hand without error up to ten crossings. Only use a pair of knots that no hand invariant separates and a question that needs a different route.
- Number theory and algebra: class numbers, unit groups, Galois groups of a polynomial read from a drawn Newton polygon or splitting diagram.
- Probability on a drawn structure: absorption probabilities, hitting times, exact Markov chain answers where the "obvious" symmetry argument is wrong.

What the colleague's log says applies to every one of these: a clean derivation gets solved five out of five. The question has to have one decisive step where the standard approach gives a plausible wrong answer, and that step has to be reachable in a few thousand tokens.
