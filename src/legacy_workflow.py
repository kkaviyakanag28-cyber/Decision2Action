"""
Decision2Action - Legacy Workflow Coexistence & Rollback

This module demonstrates:
1. Existing legacy workflow
2. New Decision2Action workflow
3. Coexistence between both workflows
4. Migration switch
5. Rollback to legacy workflow
6. Audit-friendly event logging
"""

from datetime import datetime
import json
import os


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CONFIG_FILE = "database/workflow_config.json"
ROLLBACK_LOG = "database/rollback_log.json"


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def ensure_database_folder():
    os.makedirs("database", exist_ok=True)


def load_config():
    ensure_database_folder()

    if not os.path.exists(CONFIG_FILE):
        config = {
            "active_workflow": "NEW",
            "migration_enabled": True
        }

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

        return config

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config):
    ensure_database_folder()

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


# ---------------------------------------------------------
# Legacy Workflow
# ---------------------------------------------------------

def legacy_workflow(action):
    """
    Simulates the organisation's existing manual workflow.
    """

    return {
        "workflow": "LEGACY",
        "action_id": action.get("action_id"),
        "status": "LEGACY_PENDING",
        "message": "Action forwarded to existing manual task workflow.",
        "timestamp": datetime.now().isoformat()
    }


# ---------------------------------------------------------
# New Decision2Action Workflow
# ---------------------------------------------------------

def new_workflow(action):
    """
    Uses the Decision2Action extracted action.
    """

    impact = action.get("impact", "NORMAL")

    if impact == "HIGH":
        status = "HUMAN_CONFIRMATION_REQUIRED"
    else:
        status = "READY_FOR_REVIEW"

    return {
        "workflow": "DECISION2ACTION",
        "action_id": action.get("action_id"),
        "status": status,
        "message": "Action processed through Decision2Action workflow.",
        "timestamp": datetime.now().isoformat()
    }


# ---------------------------------------------------------
# Coexistence
# ---------------------------------------------------------

def process_action(action):
    """
    Processes an action according to the currently active workflow.
    """

    config = load_config()

    active_workflow = config.get("active_workflow", "NEW")

    if active_workflow == "LEGACY":
        return legacy_workflow(action)

    return new_workflow(action)


# ---------------------------------------------------------
# Migration
# ---------------------------------------------------------

def enable_new_workflow():
    """
    Enable Decision2Action as the active workflow.
    """

    config = load_config()

    config["active_workflow"] = "NEW"
    config["migration_enabled"] = True

    save_config(config)

    print("New Decision2Action workflow enabled.")


# ---------------------------------------------------------
# Rollback
# ---------------------------------------------------------

def rollback_to_legacy(reason):
    """
    Roll back from Decision2Action to the legacy workflow.
    """

    config = load_config()

    old_workflow = config.get("active_workflow", "NEW")

    config["active_workflow"] = "LEGACY"
    config["migration_enabled"] = False

    save_config(config)

    ensure_database_folder()

    rollback_event = {
        "timestamp": datetime.now().isoformat(),
        "event": "WORKFLOW_ROLLBACK",
        "from_workflow": old_workflow,
        "to_workflow": "LEGACY",
        "reason": reason
    }

    logs = []

    if os.path.exists(ROLLBACK_LOG):
        with open(ROLLBACK_LOG, "r", encoding="utf-8") as file:
            logs = json.load(file)

    logs.append(rollback_event)

    with open(ROLLBACK_LOG, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

    print("Rollback completed successfully.")
    print("Active workflow: LEGACY")
    print("Reason:", reason)


# ---------------------------------------------------------
# Status
# ---------------------------------------------------------

def workflow_status():
    """
    Display current workflow status.
    """

    config = load_config()

    print("\n==============================")
    print("WORKFLOW STATUS")
    print("==============================")
    print("Active Workflow :", config["active_workflow"])
    print("Migration       :", config["migration_enabled"])
    print("==============================")


# ---------------------------------------------------------
# Demo
# ---------------------------------------------------------

if __name__ == "__main__":

    ensure_database_folder()

    sample_action = {
        "action_id": "ACT-DEMO-001",
        "impact": "HIGH"
    }

    print("\n==============================")
    print("DECISION2ACTION WORKFLOW DEMO")
    print("==============================")

    # Start with new workflow
    enable_new_workflow()

    workflow_status()

    print("\nProcessing action with NEW workflow:")

    result = process_action(sample_action)

    print(json.dumps(result, indent=4))

    # Demonstrate rollback
    print("\nPerforming rollback...")

    rollback_to_legacy(
        "Rollback demonstration: new workflow temporarily unavailable."
    )

    workflow_status()

    print("\nProcessing same action after rollback:")

    result = process_action(sample_action)

    print(json.dumps(result, indent=4))

    print("\nWorkflow demonstration completed.")
    