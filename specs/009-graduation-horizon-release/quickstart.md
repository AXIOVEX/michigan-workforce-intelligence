# Validation sequence

Install project report/dev dependencies and released Spec Kit evaluator/AEE extensions as documented in the release validation record. Run the edition evidence validator, relevant tests, `make ci`, native local CI when Docker is absent, and portable launcher tests. Build using `python scripts/build_reports.py --version YYYY.MM.DD.HHMMSSZ` with the committed active edition. Inspect every rendered page in `tmp/pdfs/`.

Run AEE assessments on the feature claim bundle at each stage, then challenge/graph/verify/gaps through `.specify/extensions/aee/scripts/python/run_aee.py`. Review recovery findings before publication. Use the existing `python scripts/reports.py release --version ...` from a clean, pushed checkout with authenticated `gh` and required gates satisfied. Do not delete prior releases.
