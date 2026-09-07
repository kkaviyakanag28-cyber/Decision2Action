import sys
import os
import sqlite3

# Project root path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database.database import (
    get_connection,
    record_approval,
    record_audit,
    update_action_status,
    get_action
)


def approve_action(action_id, reviewer="Human Reviewer"):
    """
    Approve an action after human confirmation.
    """

    action = get_action(action_id)

    if action is None:
        print(f"Action {action_id} not found.")
        return False

    old_status = action[7]

    # High-impact actions must be explicitly confirmed
    if action[5] == "HIGH":
        print("\nHIGH-IMPACT ACTION")
        print("Human confirmation is required.")

    success = update_action_status(
        action_id,
        "APPROVED",
        f"Approved by {reviewer}"
    )

    if success:

        record_approval(
            action_id,
            "APPROVED",
            f"Approved by {reviewer}"
        )

        print(f"\nAction {action_id} approved successfully.")

        return True

    return False


def override_action(
    action_id,
    reason,
    reviewer="Human Reviewer"
):
    """
    Override an extracted action.
    Override reason is mandatory.
    """

    if not reason or not reason.strip():

        print(
            "Override failed: reason is mandatory."
        )

        return False

    action = get_action(action_id)

    if action is None:

        print(
            f"Action {action_id} not found."
        )

        return False

    old_status = action[7]

    success = update_action_status(
        action_id,
        "OVERRIDDEN",
        reason
    )

    if success:

        record_approval(
            action_id,
            "OVERRIDDEN",
            reason
        )

        print(
            f"\nAction {action_id} overridden successfully."
        )

        print(
            f"Override reason: {reason}"
        )

        return True

    return False


def display_action(action_id):
    """
    Display action details before human review.
    """

    action = get_action(action_id)

    if action is None:

        print(
            f"Action {action_id} not found."
        )

        return

    print("\n" + "=" * 60)
    print("ACTION REVIEW")
    print("=" * 60)

    print(f"Action ID    : {action[0]}")
    print(f"Decision ID  : {action[1]}")
    print(f"Action       : {action[2]}")
    print(f"Owner        : {action[3]}")
    print(f"Deadline     : {action[4]}")
    print(f"Impact       : {action[5]}")
    print(f"Confidence   : {action[6]}")
    print(f"Status       : {action[7]}")

    print("=" * 60)


def show_approval_history(action_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            approval_id,
            decision,
            reason,
            reviewed_at
        FROM approvals
        WHERE action_id = ?
        ORDER BY reviewed_at DESC
    """, (action_id,))

    results = cursor.fetchall()

    connection.close()

    print("\nApproval History")

    if not results:

        print("No approval history found.")

        return

    for row in results:

        print(
            f"ID: {row[0]} | "
            f"Decision: {row[1]} | "
            f"Reason: {row[2]} | "
            f"Time: {row[3]}"
        )


if __name__ == "__main__":

    print("=" * 60)
    print("DECISION2ACTION - HUMAN APPROVAL MODULE")
    print("=" * 60)

    # Get a sample action from database
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT action_id
        FROM actions
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:

        action_id = result[0]

        display_action(action_id)

        print("\nApproval module is ready.")
        print(
            "Use approve_action() or override_action() "
            "for human review."
        )

    else:

        print(
            "No actions available for review."
        )
        