import os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from database.database import init_db, load_actions

if __name__ == "__main__":
    init_db()
    path = os.path.join(BASE, "data", "processed", "rule_evaluated_actions.csv")
    load_actions(path)
    print("Database initialized and actions loaded successfully.")
