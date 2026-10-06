import os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from database.database import update_status

def approve_action(action_id):
    update_status(action_id, "APPROVED", "Human reviewer approved the action.")
    return True

def override_action(action_id, reason):
    if not reason or not reason.strip():
        raise ValueError("Override reason is required.")
    update_status(action_id, "OVERRIDDEN", reason.strip())
    return True
