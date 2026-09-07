# Decision2Action Synthetic Dataset

Total records: 10,000

Breakdown:
- meeting_transcripts.csv: 4,000
- chat_threads.csv: 2,000
- decisions.csv: 1,500
- tasks.csv: 1,500
- completion_updates.csv: 1,000

All records are synthetic/anonymized and contain no real personal data.

The data includes normal cases and edge cases such as:
- missing owner
- missing deadline
- ambiguous decisions
- pending/blocked completion updates
- needs-review tasks

Purpose:
Training/testing a decision-to-action extraction prototype that links
meeting/chat evidence to owners, deadlines, decisions, tasks and completion updates.
