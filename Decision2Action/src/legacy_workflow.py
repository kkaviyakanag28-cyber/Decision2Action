import os, json
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(BASE, "database", "workflow_config.json")
LOG = os.path.join(BASE, "database", "rollback_log.json")

def set_workflow(name):
    with open(CONFIG, "w") as f:
        json.dump({"active_workflow": name}, f, indent=2)

def rollback():
    set_workflow("LEGACY")
    record = {"timestamp": datetime.now().isoformat(timespec="seconds"),
              "from": "NEW", "to": "LEGACY", "reason": "Rollback requested"}
    with open(LOG, "w") as f:
        json.dump(record, f, indent=2)
    return record

if __name__ == "__main__":
    set_workflow("NEW")
    print("Current workflow: NEW")
    print("Rollback:", rollback())
