import os,json
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.makedirs(os.path.join(BASE,"database"),exist_ok=True)
p=os.path.join(BASE,"database","workflow_config.json")
json.dump({"workflow_mode":"LEGACY"},open(p,"w"),indent=2)
print("Rollback mode set to LEGACY.")
