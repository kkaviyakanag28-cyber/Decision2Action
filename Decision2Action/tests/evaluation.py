import os, sys
import pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

def run():
    p=os.path.join(BASE,"data","processed","rule_evaluated_actions.csv")
    df=pd.read_csv(p)
    print("Source records:", len(df))
    print("Extraction records:", len(df))
    print("Owner identified:", int(df["owner"].fillna("").astype(str).str.strip().ne("").sum()))
    print("Deadline identified:", int(df["deadline"].fillna("").astype(str).str.strip().ne("").sum()))
    print("Average confidence:", round(df["confidence"].mean(),2))
    print("Average rule score:", round(df["rule_score"].mean(),2))

if __name__=="__main__":
    run()
