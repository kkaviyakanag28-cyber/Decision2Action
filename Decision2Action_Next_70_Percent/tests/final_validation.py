import os,pandas as pd
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); d=pd.read_csv(os.path.join(B,"data","processed","rule_evaluated_actions.csv"))
for c in ["source_id","owner","deadline","confidence","status","impact","rule_score","recommendation"]: print(c, "PASS" if c in d.columns else "FAIL")
print("Rows:",len(d))
