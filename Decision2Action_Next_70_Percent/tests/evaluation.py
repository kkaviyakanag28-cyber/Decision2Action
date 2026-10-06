import os,pandas as pd
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); d=pd.read_csv(os.path.join(B,"data","processed","extracted_actions.csv"))
print("Rows:",len(d)); print("Owner identification:",round(d.owner.astype(bool).mean()*100,2),"%"); print("Deadline identification:",round(d.deadline.astype(bool).mean()*100,2),"%"); print("Average confidence:",round(d.confidence.mean()*100,2),"%")
