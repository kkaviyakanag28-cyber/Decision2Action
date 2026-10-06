import re
import pandas as pd


# Keywords that indicate a decision
DECISION_KEYWORDS = [
    "decided",
    "decision",
    "agreed",
    "must",
    "required",
    "will",
    "should",
    "confirmed"
]

# Keywords that indicate a possible action
ACTION_KEYWORDS = [
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

# Project/team owners
OWNER_KEYWORDS = [
    "Data Engineering Team",
    "Analytics Team",
    "Security Team",
    "QA Team",
    "Consulting Team",
    "Project Team",
    "Operations Team",
    "Platform Team",
    "Migration Team",
    "Documentation Team"
]


def split_sentences(text):
    """Split transcript into simple sentences."""
    return re.split(r"[.!?]+", str(text))


def extract_deadline(text):
    """Extract YYYY-MM-DD dates."""
    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

    match = re.search(pattern, str(text))

    if match:
        return match.group()

    return None


def extract_owner(text):
    """Find a known team owner."""

    text_lower = str(text).lower()

    for owner in OWNER_KEYWORDS:
        if owner.lower() in text_lower:
            return owner

    return None


def is_decision(sentence):
    """Check whether a sentence contains decision language."""

    sentence_lower = sentence.lower()

    return any(
        keyword in sentence_lower
        for keyword in DECISION_KEYWORDS
    )


def is_action(sentence):
    """Check whether a sentence contains action language."""

    sentence_lower = sentence.lower()

    return any(
        keyword in sentence_lower
        for keyword in ACTION_KEYWORDS
    )


def calculate_confidence(sentence, owner, deadline):
    """
    Simple baseline confidence score.

    Decision keyword = +30
    Action keyword   = +30
    Owner detected   = +20
    Deadline detected = +20
    """

    score = 0

    if is_decision(sentence):
        score += 30

    if is_action(sentence):
        score += 30

    if owner:
        score += 20

    if deadline:
        score += 20

    return score


def extract_from_text(text, source_id=None):
    """
    Extract decision/action information from one transcript.
    """

    results = []

    sentences = split_sentences(text)

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if not (is_decision(sentence) or is_action(sentence)):
            continue

        owner = extract_owner(sentence)
        deadline = extract_deadline(sentence)

        confidence = calculate_confidence(
            sentence,
            owner,
            deadline
        )

        # Determine review status
        if owner is None or deadline is None:
            status = "NEEDS_HUMAN_REVIEW"
        elif confidence >= 80:
            status = "READY_FOR_REVIEW"
        else:
            status = "NEEDS_HUMAN_REVIEW"

        results.append({
            "source_id": source_id,
            "evidence": sentence,
            "owner": owner if owner else "UNKNOWN",
            "deadline": deadline if deadline else "UNKNOWN",
            "confidence": confidence,
            "status": status
        })

    return results


def process_meeting_file(input_file, output_file):
    """
    Process the complete meeting transcript CSV.
    """

    df = pd.read_csv(input_file)

    extracted_records = []

    for _, row in df.iterrows():

        source_id = row["meeting_id"]
        transcript = row["transcript"]

        results = extract_from_text(
            transcript,
            source_id
        )

        for result in results:
            extracted_records.append(result)

    result_df = pd.DataFrame(extracted_records)

    result_df.to_csv(
        output_file,
        index=False
    )

    return result_df


if __name__ == "__main__":

    input_file = "data/raw/meeting_transcripts.csv"

    output_file = "data/processed/extracted_actions.csv"

    result = process_meeting_file(
        input_file,
        output_file
    )

    print("=" * 60)
    print("DECISION2ACTION - BASELINE EXTRACTION")
    print("=" * 60)

    print(f"Input records processed: 4000")
    print(f"Extracted candidates: {len(result)}")

    print("\nSample extracted results:\n")

    print(
        result.head(10).to_string(index=False)
    )

    print("\nOutput saved to:")
    print(output_file)