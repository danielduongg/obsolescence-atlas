"""Figures: the forecaster-disagreement scatter, correlations, wage vs exposure."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
D=json.load(open("occupations.json"))["occupations"]
fo=np.array([d["fo"] for d in D]);ai=np.array([d["aioe"] for d in D]);gpt=np.array([d["gpt"] for d in D]);wage=np.array([d["wage"] for d in D])
plt.rcParams.update({"figure.facecolor":"#0a0710","axes.facecolor":"#161020","savefig.facecolor":"#0a0710",
  "text.color":"#f1eaff","axes.labelcolor":"#cdbfe6","xtick.color":"#a99cc4","ytick.color":"#a99cc4",
  "axes.edgecolor":"#2a2040","font.size":10,"axes.titlecolor":"#f1eaff"})
r=lambda a,b: float(np.corrcoef(a,b)[0,1])

plt.figure(figsize=(6.2,5)); plt.scatter(fo,gpt,s=22,c="#b07bff",alpha=.7,edgecolor="none")
plt.xlabel("Frey–Osborne automation (2013)"); plt.ylabel("Eloundou GPT-exposure (2023)")
plt.title(f"The two eras of forecasts disagree (r={r(fo,gpt):.2f})"); plt.xlim(-.03,1.03); plt.ylim(-.03,1.03)
plt.tight_layout(); plt.savefig("fig_disagreement.png",dpi=120); plt.close()

plt.figure(figsize=(6.2,3.6)); pairs=[("FO vs GPT",r(fo,gpt)),("FO vs AIOE",r(fo,ai)),("AIOE vs GPT",r(ai,gpt))]
b=plt.bar([p[0] for p in pairs],[p[1] for p in pairs],color=["#ff7b9c","#ffb454","#27d08a"])
plt.ylim(0,1); plt.ylabel("correlation"); plt.title("2013 vs 2023 measures barely correlate")
for bar,(_,v) in zip(b,pairs): plt.text(bar.get_x()+bar.get_width()/2,v+0.02,f"{v:.2f}",ha="center")
plt.tight_layout(); plt.savefig("fig_correlations.png",dpi=120); plt.close()

plt.figure(figsize=(6.4,4.4)); plt.scatter(wage/1000,gpt,s=22,c="#5b8cff",alpha=.7,edgecolor="none")
plt.xlabel("median wage ($k)"); plt.ylabel("GPT-exposure")
plt.title(f"Higher-paid jobs skew toward more LLM exposure (r={r(wage,gpt):.2f})")
plt.tight_layout(); plt.savefig("fig_wage_exposure.png",dpi=120); plt.close()
print("wrote 3 figures; corr(wage,gpt)=",round(r(wage,gpt),2))
