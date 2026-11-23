import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False,
 "axes.grid":True,"grid.color":"#e4e3de","grid.linewidth":0.6,"axes.edgecolor":"#8a8980",
 "lines.linewidth":1.6,"figure.dpi":150,"savefig.bbox":"tight"})
BLUE,RED,GRAY="#2a78d6","#c8102e","#6b6a63"
c=1/np.log(4)
def H(x): return -(x*np.log2(x)+(1-x)*np.log2(1-x))
x=np.linspace(1e-9,1-1e-9,4001); u=4*x*(1-x)

f,ax=plt.subplots(figsize=(5.2,3.0))
ax.plot(x,u**c,color=GRAY,ls="--",lw=1.1,label=r"$u^{1/\ln 4}$ (upper bound)")
ax.plot(x,u,color=GRAY,ls=":",lw=1.3,label=r"$u=4x(1-x)$ (lower bound)")
ax.plot(x,u**0.75,color=BLUE,label=r"$u^{3/4}$")
ax.plot(x,H(x),color=RED,lw=1.3,label=r"$h(x)$")
ax.set_xlabel(r"$x$"); ax.set_xlim(0,1); ax.set_ylim(0,1.05); ax.legend(frameon=False,loc="lower center",fontsize=8)
f.savefig("fig1.pdf")

xs=np.concatenate([np.logspace(-8,np.log10(0.05),3000),np.linspace(0.05,0.5,3000)])
D=(4*xs*(1-xs))**0.75-H(xs)
f,ax=plt.subplots(figsize=(5.2,2.6))
ax.axhline(0,color="#8a8980",lw=0.8)
ax.plot(xs,D,color=BLUE)
i,j=D.argmax(),D.argmin()
ax.plot([xs[i],xs[j]],[D[i],D[j]],"o",color=BLUE,ms=4)
ax.annotate(f"max {D[i]:.4f}\n$x\\approx{xs[i]:.4f}$",(xs[i],D[i]),xytext=(-85,-2),textcoords="offset points",fontsize=8,va="top")
ax.annotate(f"min {D[j]:.4f}\n$x\\approx{xs[j]:.3f}$",(xs[j],D[j]),xytext=(-100,12),textcoords="offset points",fontsize=8,va="center")
ax.set_xscale("log"); ax.set_xlim(1e-6,0.5)
ax.set_xlabel(r"$x$ (log scale)"); ax.set_ylabel(r"$u^{3/4}-h(x)$")
f.savefig("fig2.pdf")

xg=np.logspace(-14,np.log10(0.4999),3000); ug=4*xg*(1-xg)
g=np.log(H(xg))/np.log(ug)
f,ax=plt.subplots(figsize=(5.2,2.6))
for yv,lab in [(1,"1"),(0.75,"3/4"),(c,r"$1/\ln 4$")]:
    ax.axhline(yv,color=GRAY,lw=0.8,ls="--"); ax.text(1.3e-14,yv+0.006,lab,fontsize=8,color=GRAY)
ax.plot(xg,g,color=BLUE)
ax.set_xscale("log"); ax.set_xlim(1e-14,0.5); ax.set_ylim(0.7,1.02)
ax.set_xlabel(r"$x$ (log scale)"); ax.set_ylabel(r"$g(x)=\ln h/\ln u$")
f.savefig("fig3.pdf")

# fig4: boundary function Phi(y) of Lemma 8
yy=np.logspace(-12,8,4000)
R=yy*np.log1p(1/yy)+np.log1p(yy); v=4*yy*(1+yy)
habs=np.sqrt(R**2+np.pi**2*yy**2)/np.log(2); ph=np.arctan(np.pi*yy/R)
Phi=np.pi*np.log(habs/v)+ph*np.log(v)
f,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(yy,Phi,color=BLUE)
k=Phi.argmin(); ax.plot(yy[k],Phi[k],"o",color=BLUE,ms=4)
ax.annotate(f"min {Phi[k]:.3f} at $y\\approx{yy[k]:.3f}$",(yy[k],Phi[k]),xytext=(10,-4),textcoords="offset points",fontsize=8,va="top")
ax.axhline(np.pi*np.log(np.pi/(2*np.log(2))),color=GRAY,lw=0.8,ls="--")
ax.set_xscale("log"); ax.set_ylim(0,6.5); ax.set_xlim(1e-12,1e8)
ax.set_xlabel(r"$y$ (log scale)"); ax.set_ylabel(r"$\Phi(y)$")
f.savefig("fig4.pdf")
