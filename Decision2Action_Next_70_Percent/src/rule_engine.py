import os,pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(BASE,"data","processed","extracted_actions.csv")
df=pd.read_csv(p)
def score(r):
    t=str(r.evidence).lower(); s=0; rules=[]
    if "decision made" in t or "agreed to" in t: s+=25; rules.append("DECISION_LANGUAGE")
    if any(x in t for x in ["action item","will complete","should prepare"]): s+=25; rules.append("ACTION_LANGUAGE")
    if str(r.owner).strip(): s+=25; rules.append("OWNER_IDENTIFIED")
    if str(r.deadline).strip(): s+=25; rules.append("DEADLINE_IDENTIFIED")
    return pd.Series([s,"|".join(rules),"READY_FOR_HUMAN_APPROVAL" if s>=75 else "NEEDS_HUMAN_REVIEW"])
df[["rule_score","rules_triggered","recommendation"]]=df.apply(score,axis=1)
df.to_csv(os.path.join(BASE,"data","processed","rule_evaluated_actions.csv"),index=False)
print("Rule evaluation completed.")
