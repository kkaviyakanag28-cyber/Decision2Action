import os,pandas as pd
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); p=os.path.join(B,"data","processed","rule_evaluated_actions.csv"); d=pd.read_csv(p)
s=pd.DataFrame({"metric":["total","low_confidence","missing_owner","missing_deadline","high_impact","human_confirmation_required"],"count":[len(d),(d.confidence<.7).sum(),(~d.owner.astype(bool)).sum(),(~d.deadline.astype(bool)).sum(),(d.impact=="HIGH").sum(),(d.status=="HUMAN_CONFIRMATION_REQUIRED").sum()]})
s.to_csv(os.path.join(B,"data","processed","error_analysis.csv"),index=False); print(s.to_string(index=False))
