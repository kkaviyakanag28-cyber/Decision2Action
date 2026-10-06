import os, pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(BASE,"data","processed","rule_evaluated_actions.csv")
df=pd.read_csv(p)
required=["action_id","source_id","owner","deadline","confidence","status","rule_score","recommendation"]
missing=[c for c in required if c not in df.columns]
if missing:
    raise SystemExit("Missing columns: "+str(missing))
print("FINAL VALIDATION: PASS")
print("Records:",len(df))
print("Required fields:",", ".join(required))
