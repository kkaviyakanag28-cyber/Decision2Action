def evaluate_rules(record):
    """
    Evaluate the evidence behind an extracted action.
    """

    rules = []
    score = 0

    evidence = str(record.get("evidence", "")).lower()
    owner = record.get("owner")
    deadline = record.get("deadline")

    # Rule 1: Decision language
    decision_words = [
        "decided",
        "decision",
        "agreed",
        "must",
        "required",
        "confirmed"
    ]

    if any(word in evidence for word in decision_words):
        rules.append("Decision language detected")
        score += 30

    # Rule 2: Action language
    action_words = [
        "complete",
        "validate",
        "migrate",
        "update",
        "finalize",
        "prepare",
        "review",
        "perform",
        "handle",
        "verify",
        "test"
    ]

    if any(word in evidence for word in action_words):
        rules.append("Action language detected")
        score += 30

    # Rule 3: Owner
    if owner and str(owner).upper() != "UNKNOWN":
        rules.append("Owner identified")
        score += 20
    else:
        rules.append("Owner missing")

    # Rule 4: Deadline
    if deadline and str(deadline).upper() != "UNKNOWN":
        rules.append("Deadline identified")
        score += 20
    else:
        rules.append("Deadline missing")

    # Final recommendation
    if score >= 80:
        recommendation = "READY_FOR_HUMAN_APPROVAL"
    else:
        recommendation = "NEEDS_HUMAN_REVIEW"

    return {
        "rule_score": score,
        "rules_triggered": " | ".join(rules),
        "recommendation": recommendation
    }


def apply_rules_to_file(input_file, output_file):
    """
    Read extracted actions and apply the rule engine.
    """

    import pandas as pd

    df = pd.read_csv(input_file)

    rule_results = []

    for _, row in df.iterrows():

        result = evaluate_rules(row.to_dict())

        rule_results.append(result)

    rule_df = pd.DataFrame(rule_results)

    final_df = pd.concat(
        [df.reset_index(drop=True),
         rule_df.reset_index(drop=True)],
        axis=1
    )

    final_df.to_csv(
        output_file,
        index=False
    )

    return final_df


if __name__ == "__main__":

    input_file = "data/processed/extracted_actions.csv"

    output_file = "data/processed/rule_evaluated_actions.csv"

    result = apply_rules_to_file(
        input_file,
        output_file
    )

    print("=" * 60)
    print("DECISION2ACTION - RULE ENGINE")
    print("=" * 60)

    print(f"Records evaluated: {len(result)}")

    print("\nRecommendation summary:")

    print(
        result["recommendation"].value_counts()
    )

    print("\nSample results:\n")

    print(
        result[
            [
                "source_id",
                "owner",
                "deadline",
                "rule_score",
                "rules_triggered",
                "recommendation"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nOutput saved to:")
    print(output_file)