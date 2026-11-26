# Why (4x(1−x))^{3/4} approximates the binary entropy so well

Source and verification code for the paper

> J. van de Graaf, *Why (4x(1−x))^{3/4} approximates the binary entropy so well: a proof of Topsøe's convexity conjecture*, [arXiv:2611.33213](https://arxiv.org/abs/2611.33213) (2026).

## What the paper proves

Write the binary entropy as h(x) = u^{g(x)} with u = 4x(1−x). Topsøe (2001) proved 1/ln 4 ≤ g ≤ 1 and conjectured that g is convex. The paper proves this: in the variable s = (1−2x)², g is a Pick function, so g(x) = Σ γₙ (1−2x)^{2n} with all γₙ > 0. As an application it gives certified constants for the approximation h ≈ u^{3/4}:

    −0.0065493 ≤ (4x(1−x))^{3/4} − h(x) ≤ 0.0080004   on [0, 1].

Writing g = 1/ln z, with z between e and 4, it also proves the one-sided bound

    0 ≤ h(x) − u^{1/ln z} ≤ 0.0006377   on [0, 1],   ln z = 1 + (ln 4 − 1) u^{1/10},

about 170 times tighter than Topsøe's h ≥ u.

## Repository layout

| Path | Contents |
|---|---|
| `paper/entropy.md` | Paper source (pandoc Markdown) |
| `paper/main.tex` | LaTeX generated from it, as submitted to arXiv |
| `paper/fig*.pdf` | Figures |
| `scripts/verify_lemma5.py` | Certifies Lemma 5 (Φ > 0 on [1e-4, 10]) with interval arithmetic |
| `scripts/verify_theorem8.py` | Certifies the sharp constants of Theorem 8 with interval arithmetic |
| `scripts/verify_theorem10.py` | Certifies Theorem 10, the bound 0 ≤ h − u^(1/ln z) ≤ 0.0006377 |
| `scripts/taylor_coeffs.py` | Computes the first 398 Taylor coefficients γₙ in 60-digit arithmetic |
| `scripts/check_representation.py` | Compares those coefficients with the integral formula of Theorem 1 |
| `scripts/make_figures.py` | Regenerates the figures |

## Rerunning the checks

```
pip install python-flint mpmath numpy matplotlib
cd scripts
python verify_lemma5.py        # prints: 92 boxes
python verify_theorem8.py      # prints: 145 boxes
python verify_theorem10.py     # prints: PROVED ...
python taylor_coeffs.py        # writes gamma_coefficients.json
python check_representation.py
```

The two `verify_*` scripts use Arb ball arithmetic (via python-flint): every quantity is an interval guaranteed to contain the true value, and a subinterval is accepted only if the whole enclosure has the right sign. They are proofs, not sampling.

## Building the paper

```
cd paper
python ../scripts/make_figures.py   # optional: regenerate the figures
pdflatex main.tex && pdflatex main.tex
```

`main.tex` was produced from `entropy.md` with `pandoc entropy.md -s -o main.tex`.

## Use of AI tools

Significant parts of the proofs, the text and the scripts were produced with the AI system Claude (Anthropic); see the section "Use of AI tools" in the paper.

## License

The code in `scripts/` is released under the MIT License (see `LICENSE`). The paper text and figures are © Jeroen van de Graaf and are distributed on arXiv under the arXiv non-exclusive license.
