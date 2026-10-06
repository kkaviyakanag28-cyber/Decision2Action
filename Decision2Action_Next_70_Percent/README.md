# Decision2Action - Next 70%

Working final-stage package for decision-to-action extraction.

Pipeline:
Source data -> Extraction -> Owner/Deadline -> Rule Engine -> Human Confirmation -> SQLite Audit -> Flask Dashboard

Run:
1. pip install -r requirements.txt
2. python src/generate_dataset.py
3. python src/extractor.py
4. python src/rule_engine.py
5. python src/load_database.py
6. python app.py

Then open http://127.0.0.1:5000
