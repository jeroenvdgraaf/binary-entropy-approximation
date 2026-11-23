import json
from mpmath import mp, mpf, mpc, log, sqrt, pi, quad, im, nstr, inf
mp.dps=25
G=[mpf(v) for v in json.load(open('gamma_coefficients.json'))]
L2=log(2)
def h(s):
    t=sqrt(s); x=(1-t)/2
    return -(x*log(x)+(1-x)*log(1-x))/L2
def ImG(sig):
    s=mpc(sig,mpf('1e-20')); return im(log(h(s))/log(1-s))
for n in [1,2,3,5,10]:
    val=quad(lambda sg: ImG(sg)*sg**(-n-1), [1,1.0001,1.01,1.5,4,100,inf])/pi
    print(n, nstr(val,10), nstr(G[n],10))
