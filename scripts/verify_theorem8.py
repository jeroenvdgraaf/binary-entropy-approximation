from flint import arb, ctx
ctx.prec = 128
HI, LO, X0 = arb("0.0080004"), arb("-0.0065493"), arb("1e-4")
LN2 = arb(2).log()

def h(x):                       # binary entropy in bits
    return -(x * x.log() + (1 - x) * (1 - x).log()) / LN2

def D(x):                       # u^(3/4) - h(x)
    u = 4 * x * (1 - x)
    return u.sqrt() * u.sqrt().sqrt() - h(x)

def dD(x):                      # derivative of D
    u = 4 * x * (1 - x)
    return arb(3) / 4 * (4 - 8 * x) / u.sqrt().sqrt() \
        - ((1 - x) / x).log() / LN2

def check(a, b):                # certify LO < D < HI on [a, b]
    m, r = (a + b) / 2, (b - a) / 2
    enc = D(m) + dD(arb.union(a, b)) * arb(0, r.upper())
    if enc < HI and enc > LO:
        return 1
    return check(a, m) + check(m, b)

# endpoint region [0, X0]: monotonicity
assert (4 * X0).sqrt() * (4 * X0).sqrt().sqrt() < HI
assert -h(X0) > LO
print(check(X0, arb(1) / 2), "boxes")
