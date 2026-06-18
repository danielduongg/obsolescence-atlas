"""obsolescence-atlas — do the job-automation forecasts even agree?

Merges three published occupational-exposure measures with BLS employment
projections and asks the honest question: do they agree on which jobs are at
risk? (The 2013 automation lens and the 2023 LLM lens are nearly orthogonal.)
"""
import json, numpy as np
D=json.load(open("occupations.json"))["occupations"]
fo=np.array([d["fo"] for d in D]); ai=np.array([d["aioe"] for d in D]); gpt=np.array([d["gpt"] for d in D])
r=lambda a,b: round(float(np.corrcoef(a,b)[0,1]),2)
corr={"fo_gpt":r(fo,gpt),"fo_aioe":r(fo,ai),"aioe_gpt":r(ai,gpt)}
print("correlations:",corr)
# categorize
def cat(d):
    me=max(d["fo"],d["gpt"])
    if d["bls"]<=-5 and me>0.6: return "fading"
    if me>0.6 and d["bls"]>=5:  return "exposed_but_growing"
    if me<0.35:                 return "robust"
    return "mixed"
from collections import Counter
print("categories:",dict(Counter(cat(d) for d in D)))
json.dump({"correlations":corr,"n":len(D)},open("summary.json","w"),indent=2)
