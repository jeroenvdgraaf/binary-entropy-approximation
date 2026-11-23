# G(s) = ln h / ln(1-s), s=(1-2x)^2.  g(x)=G(t^2), t=|1-2x|.
from mpmath import mp, mpf, log
mp.dps = 60
N = 400
c = 1/log(4)
def mul(a,b):
    r=[mpf(0)]*N
    for i,ai in enumerate(a):
        if ai==0: continue
        for j in range(N-i): r[i+j]+=ai*b[j]
    return r
# P(s) = c*sum s^n/(n(2n-1))  -> ln h = ln(1-P) = -sum_k P^k/k
P=[mpf(0)]+[c/(n*(2*n-1)) for n in range(1,N)]
lnh=[mpf(0)]*N; Pk=[mpf(1)]+[mpf(0)]*(N-1)
for k in range(1,N):
    Pk=mul(Pk,P)
    if all(abs(v)<mpf(10)**-55 for v in Pk): break
    lnh=[a-b/k for a,b in zip(lnh,Pk)]
# ln(1-s) = -sum s^n/n ; divide both by -s
num=[-lnh[n+1] for n in range(N-1)]       # -ln h / s
den=[mpf(1)/(n+1) for n in range(N-1)]    # -ln(1-s)/s
G=[mpf(0)]*(N-1)
for n in range(N-1):
    G[n]=(num[n]-sum(G[k]*den[n-k] for k in range(n)))/den[0]
import json; json.dump([str(v) for v in G], open('gamma_coefficients.json','w'))
print("gamma_0",G[0], " (c=",c,")")
neg=[n for n in range(1,N-1) if G[n]<0]
print("negative coefficients:",neg[:20], "count",len(neg))
for n in list(range(1,15))+[20,50,100,200,300,398]:
    print(n, mp.nstr(G[n],12), mp.nstr(G[n]*n**2,8) if n>0 else '')
