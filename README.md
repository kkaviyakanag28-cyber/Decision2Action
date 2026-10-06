# Decision2Action

## Decision-to-Action Extraction and Governance System

Decision2Action is a rule-based decision intelligence system that extracts important decisions and actionable tasks from meeting transcripts and converts them into structured actions with owners, deadlines, confidence scores, approval controls, audit trails, and rollback support.

## Problem Statement

In consulting organizations, important decisions are often buried inside long meeting discussions, chat threads, and documents. These decisions may not be converted into clear actions, resulting in missed responsibilities, unclear deadlines, and poor follow-up.

Decision2Action solves this problem by identifying decision/action statements and converting them into structured, reviewable actions.

## Key Features

- Decision and action extraction from meeting transcripts
- Owner identification
- Deadline identification
- Confidence scoring
- Rule-based evaluation
- Human confirmation for high-impact actions
- Approval and override workflow
- Mandatory reason for overrides
- Audit logging
- Legacy workflow coexistence
- Rollback support
- Error analysis
- Evaluation metrics
- Flask web dashboard
- SQLite database

## System Architecture

```text
Meeting Transcripts
        |
        v
Data Processing
        |
        v
Decision / Action Extractor
        |
        v
Rule Engine
        |
        v
Confidence + Risk Evaluation
        |
        v
Human Review
     /       \
 Approve    Override
    |          |
    v          v
 Action     Audit Log
    |
    v
SQLite Database
    |
    v
Dashboard / Reports
