"""Certification of Theorem 10: for all x in [0, 1],

    0 <= h(x) - u^(1/ln z) <= 0.0006377,   u = 4x(1-x),  ln z = 1 + (ln 4 - 1) u^(1/10),

with equality on the left only at x in {0, 1/2, 1}. Equivalently g <= gt := 1/ln z.
By symmetry it suffices to take x in [0, 1/2]. Requires: pip install python-flint.

Lower inequality (g < gt on (0, 1/2)):
  Region I   (0, 1e-8]  : analytic bound, checked below in ball arithmetic.
  Region II  [1e-8, xs] : interval arithmetic, mean-value form with Taylor arithmetic.
  Region III [xs, 1/2)  : analytic, via Theorem 1 (g = sum gamma_n s^n, gamma_n >= 0, sum 1).
Upper inequality: on [0, 1e-8] since h - A <= h(1e-8); elsewhere interval arithmetic.
"""
from flint import arb, arb_series, ctx
ctx.prec = 120
LN2 = arb(2).log(); LN4 = arb(4).log()
a = LN4 - 1; b = arb(1) / 10; c = 1 / LN4
K = arb("0.0006377"); X0 = arb("1e-8")

def funcs(x):
    """h, u, gt for x a ball or a Taylor series."""
    u = 4 * x * (1 - x)
    h = -(x * x.log() + (1 - x) * (1 - x).log()) / LN2
    gt = 1 / (1 + a * (b * u.log()).exp())
    return h, u, gt

def mv_check(f, lo, hi, test, depth=0):
    """Certify test(f(X)) on [lo, hi] using f(m) + f'(X)(X - m), bisecting as needed."""
    m = (lo + hi) / 2; r = (hi - lo) / 2
    try:
        fm = f(arb_series([m, 1], prec=1)).coeffs()[0]
        d = f(arb_series([arb.union(lo, hi), 1], prec=2)).coeffs()[1]
        if test(fm + d * arb(0, r.upper())):
            return 1
    except ValueError:          # series division failed on a too-wide ball
        pass
    if depth > 80:
        raise RuntimeError("cannot certify near %s" % lo)
    return mv_check(f, lo, m, test, depth + 1) + mv_check(f, m, hi, test, depth + 1)

def q(x):                        # gt - g
    h, u, gt = funcs(x)
    return gt - h.log() / u.log()

def D(x):                        # h - A
    h, u, gt = funcs(x)
    return h - (gt * u.log()).exp()

# ---- Region I. For u <= 4 X0 < e^{-1/b}, u^b ln(1/u) is increasing, so
#      A = u exp(a u^b ln(1/u) / (1 + a u^b)) <= 4 x exp(a M), while h >= x log2(1/x) >= x log2(1/X0).
uM = 4 * X0
assert uM < (-1 / b).exp()
M = uM ** b * (1 / uM).log()
lhs = 4 * (a * M).exp(); rhs = (1 / X0).log() / LN2
assert lhs < rhs
print("Region I  : A <= %s x < %s x <= h on (0, 1e-8]" % (lhs.str(4), rhs.str(4)))

# ---- Region III. With s = (1-2x)^2 and w = (1-s)^b <= 1 - b s (Bernoulli):
#      gt - c = a(1 - w)/((1 + a w)(1 + a)) >= c^2 a b s, and by Theorem 1
#      g <= c + gamma1 s + (1 - c - gamma1) s^2. So gt - g >= s (delta - R s) > 0 for s <= s0.
gamma1 = c * (c / 2 - arb(1) / 3)
delta = c * c * a * b - gamma1; R = 1 - c - gamma1
assert delta > 0
s0 = delta / (2 * R)
xs = (1 - s0.sqrt()) / 2
XS = arb("0.4865")
assert XS > xs
print("Region III: delta = %s, s0 = %s, covers [%s, 1/2)" % (delta.str(4), s0.str(4), xs.str(6)))

# ---- Region II.
n2 = mv_check(q, X0, XS, lambda e: e > 0)
print("Region II : gt > g certified on [1e-8, 0.4865] with %d boxes" % n2)

# ---- Upper bound.
assert -(X0 * X0.log() + (1 - X0) * (1 - X0).log()) / LN2 < K
n3 = mv_check(D, X0, arb(1) / 2, lambda e: e < K)
print("Upper     : h - A < %s certified on [1e-8, 1/2] with %d boxes" % (K.str(5), n3))
print("PROVED: 0 <= h - u^(1/ln z) <= 0.0006377 on [0, 1]")
