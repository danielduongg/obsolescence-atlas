import json, numpy as np
D=json.load(open("occupations.json"))["occupations"]

def test_data_integrity():
    assert len(D) >= 60
    for d in D:
        assert {"name","fo","aioe","gpt","bls","wage"} <= set(d)
        for k in ("fo","aioe","gpt"): assert 0.0 <= d[k] <= 1.0
        assert d["wage"] > 0 and -40 <= d["bls"] <= 60

def test_forecasts_disagree():
    fo=np.array([d["fo"] for d in D]); gpt=np.array([d["gpt"] for d in D])
    assert np.corrcoef(fo,gpt)[0,1] < 0.35      # 2013 vs 2023: ~uncorrelated

def test_ai_era_measures_agree():
    ai=np.array([d["aioe"] for d in D]); gpt=np.array([d["gpt"] for d in D])
    assert np.corrcoef(ai,gpt)[0,1] > 0.8       # the two AI-era measures agree

def test_exposure_not_destiny():
    # at least some high-exposure occupations are still projected to grow
    grow=[d for d in D if max(d["fo"],d["gpt"])>0.6 and d["bls"]>=5]
    assert len(grow) >= 3
