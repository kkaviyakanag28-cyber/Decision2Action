import pandas as pd
import os


# =========================================================
# DECISION2ACTION - EVALUATION MODULE
# Baseline vs Decision2Action
# =========================================================

RAW_PATH = "data/raw/meeting_transcripts.csv"
PROCESSED_PATH = "data/processed/extracted_actions.csv"
OUTPUT_PATH = "data/processed/evaluation_results.csv"


def load_data():
    """Load source and extracted datasets."""

    raw = pd.read_csv(RAW_PATH)
    extracted = pd.read_csv(PROCESSED_PATH)

    return raw, extracted


def calculate_baseline(raw):
    """
    Baseline:
    Assume a traditional/manual workflow where decisions
    are not automatically converted into tracked actions.

    Baseline detection uses simple decision-language matching.
    """

    decision_keywords = [
        "decided",
        "decision",
        "agreed",
        "we will",
        "must",
        "should",
        "action"
    ]

    detected = 0

    for text in raw["transcript"].fillna("").astype(str):

        text_lower = text.lower()

        if any(keyword in text_lower for keyword in decision_keywords):
            detected += 1

    total = len(raw)

    baseline_rate = (detected / total * 100) if total else 0

    return detected, total, baseline_rate


def calculate_prototype(extracted):
    """
    Calculate Decision2Action prototype performance.
    """

    total = len(extracted)

    valid_actions = 0
    owner_found = 0
    deadline_found = 0
    high_impact = 0
    review_required = 0

    for _, row in extracted.iterrows():

        evidence = str(row.get("evidence", ""))

        owner = str(row.get("owner", "UNKNOWN"))

        deadline = str(row.get("deadline", "UNKNOWN"))

        status = str(row.get("status", ""))

        impact = str(row.get("impact", "NORMAL"))

        # Action extraction
        if evidence.strip():
            valid_actions += 1

        # Owner extraction
        if owner.upper() != "UNKNOWN" and owner.strip():
            owner_found += 1

        # Deadline extraction
        if deadline.upper() != "UNKNOWN" and deadline.strip():
            deadline_found += 1

        # High impact
        if impact.upper() == "HIGH":
            high_impact += 1

        # Human review
        if (
            "REVIEW" in status.upper()
            or "CONFIRMATION" in status.upper()
        ):
            review_required += 1

    extraction_rate = (
        valid_actions / total * 100
        if total else 0
    )

    owner_rate = (
        owner_found / total * 100
        if total else 0
    )

    deadline_rate = (
        deadline_found / total * 100
        if total else 0
    )

    return {
        "total": total,
        "valid_actions": valid_actions,
        "extraction_rate": extraction_rate,
        "owner_rate": owner_rate,
        "deadline_rate": deadline_rate,
        "high_impact": high_impact,
        "review_required": review_required
    }


def generate_evaluation():

    print("=" * 70)
    print("DECISION2ACTION - MEASURABLE EVALUATION")
    print("=" * 70)

    raw, extracted = load_data()

    # -----------------------------------------------------
    # BASELINE
    # -----------------------------------------------------

    baseline_detected, baseline_total, baseline_rate = (
        calculate_baseline(raw)
    )

    # -----------------------------------------------------
    # PROTOTYPE
    # -----------------------------------------------------

    prototype = calculate_prototype(extracted)

    # -----------------------------------------------------
    # TARGETS
    # -----------------------------------------------------

    target_extraction = 85
    target_owner = 80
    target_deadline = 75

    # -----------------------------------------------------
    # IMPROVEMENT
    # -----------------------------------------------------

    extraction_improvement = (
        prototype["extraction_rate"] - baseline_rate
    )

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    results = {

        "metric": [
            "Total Source Records",
            "Baseline Decision Detection %",
            "Decision2Action Extraction %",
            "Owner Identification %",
            "Deadline Identification %",
            "High Impact Actions",
            "Human Review Required",
            "Target Extraction %",
            "Target Owner Identification %",
            "Target Deadline Identification %",
            "Extraction Improvement %"
        ],

        "value": [

            baseline_total,

            round(baseline_rate, 2),

            round(prototype["extraction_rate"], 2),

            round(prototype["owner_rate"], 2),

            round(prototype["deadline_rate"], 2),

            prototype["high_impact"],

            prototype["review_required"],

            target_extraction,

            target_owner,

            target_deadline,

            round(extraction_improvement, 2)
        ]
    }

    results_df = pd.DataFrame(results)

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    results_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    print("\nBASELINE")
    print("-" * 50)

    print(
        f"Source records          : {baseline_total}"
    )

    print(
        f"Decision detection      : "
        f"{baseline_rate:.2f}%"
    )

    print("\nDECISION2ACTION")
    print("-" * 50)

    print(
        f"Extracted actions       : "
        f"{prototype['valid_actions']}"
    )

    print(
        f"Extraction rate         : "
        f"{prototype['extraction_rate']:.2f}%"
    )

    print(
        f"Owner identification    : "
        f"{prototype['owner_rate']:.2f}%"
    )

    print(
        f"Deadline identification : "
        f"{prototype['deadline_rate']:.2f}%"
    )

    print(
        f"High impact actions     : "
        f"{prototype['high_impact']}"
    )

    print(
        f"Human review required   : "
        f"{prototype['review_required']}"
    )

    print("\nTARGETS")
    print("-" * 50)

    print(
        f"Extraction target       : "
        f"{target_extraction}%"
    )

    print(
        f"Owner target            : "
        f"{target_owner}%"
    )

    print(
        f"Deadline target         : "
        f"{target_deadline}%"
    )

    print("\nIMPROVEMENT")
    print("-" * 50)

    print(
        f"Extraction improvement  : "
        f"{extraction_improvement:.2f}%"
    )

    print("\nResults saved to:")
    print(OUTPUT_PATH)

    print("\nEvaluation completed successfully.")


if __name__ == "__main__":
    generate_evaluation()
    