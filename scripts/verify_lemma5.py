from flint import arb, ctx
ctx.prec = 100
PI, L2 = arb.pi(), arb(2).log()

def Phi(y):                     # boundary function of Lemma 4
    R = y * (1 + 1/y).log() + (1 + y).log()
    v = 4 * y * (1 + y)
    habs = (R*R + PI*PI*y*y).sqrt() / L2
    phi = (PI * y / R).atan()
    return PI * (habs / v).log() + phi * v.log()

def check(a, b):                # certify Phi > 0 on [a, b]
    if Phi(arb.union(a, b)) > 0:
        return 1
    m = (a + b) / 2
    return check(a, m) + check(m, b)

print(check(arb("1e-4"), arb(10)), "boxes")    # prints: 92 boxes
