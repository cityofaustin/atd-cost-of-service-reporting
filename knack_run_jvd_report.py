import csv
import logging
import os
import sys

import knackpy

from config import FIELDS

# docker run -it --rm --env-file env_file --network host -v /Users/john/Dropbox/atd/atd-cost-of-service-reporting:/app atddocker/amanda-reporting /bin/bash
KNACK_API_KEY = os.getenv("KNACK_API_KEY")
KNACK_APP_ID = os.getenv("KNACK_APP_ID")

# config
KNACK_VIEW = "view_59"


def getLogger(name, level=logging.INFO):
    """Return a module logger that streams to stdout"""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt=" %(name)s.%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def handle_field(r, f, credit):
    if f.get("default"):
        return f["default"]
    handler = f.get("handler")
    if handler:
        return handler(r, credit)
    return None


def handle_record(r):
    credit_row = {}
    debit_row = {}
    for f in FIELDS:
        credit_row[f["name"]] = handle_field(r, f, credit=True)
        debit_row[f["name"]] = handle_field(r, f, credit=False)
    return [credit_row, debit_row]


def main():
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    records = app.get(KNACK_VIEW, record_limit=10)
    report_rows = []
    for r in records:
        rows = handle_record(r)
        report_rows.extend(rows)

    with open("jvd.csv", "w") as fout:
      fieldnames = report_rows[0].keys()
      writer = csv.DictWriter(fout, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(report_rows)



if __name__ == "__main__":
    logger = getLogger(__file__)
    main()
