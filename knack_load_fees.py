"""
docker run --env-file env_file --rm -it -v /Some/path/to/atd-cost-of-service-reporting:/app atddocker/atd-cost-of-service /bin/bash
"""
import logging
import os
import sys

import cx_Oracle
import knackpy
import requests
from config import FIELDS, QUERYPATH, KNACK_IS_DELETED_FIELD, KNACK_OBJECT, KNACK_VIEW

# db vars
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SERVICE = os.getenv("SERVICE")
# knack auth
KNACK_API_KEY = os.getenv("KNACK_API_KEY")
KNACK_APP_ID = os.getenv("KNACK_APP_ID")


def getLogger(name, level=logging.INFO):
    """Return a module logger that streams to stdout"""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt=" %(name)s.%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def row_factory(cursor):
    """Define cursor row handler which returns each row as a dict
    h/t https://stackoverflow.com/questions/35045879/cx-oracle-how-can-i-receive-each-row-as-a-dictionary

    Args:
        cursor (cx_Oracle cursor)
    Returns:
      function: the rowfactory
    """
    return lambda *args: dict(zip([d[0] for d in cursor.description], args))


def get_conn(host, port, service, user, password):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
    return cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)


def load_query(fname):
    with open(fname, "r") as fin:
        # cx_Oracle does not want a statement to end with `;`
        return fin.read().replace(";", "")


def fetch_amanda_records():
    logger.info("Fetching AMANDA records...")

    conn = get_conn(HOST, PORT, SERVICE, USER, PASSWORD)
    query = load_query(QUERYPATH)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.rowfactory = row_factory(cursor)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_pk_field():
    return next(f for f in FIELDS if f.get("primary_key"))


def build_id_list(rows, field_id):
    return [row[field_id] for row in rows]


def lower_case_keys(rows):
    data = []
    for row in rows:
        new = {k.lower(): v for k, v in row.items()}
        data.append(new)
    return data


def map_row(row):
    new_row = {}
    for f in FIELDS:
        new_row[f["knack"]] = row[f["amanda"]]
    return new_row


def main():
    logger.info("Instanciating Knack app...")
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)

    rows_amanda = fetch_amanda_records()
    rows_amanda = lower_case_keys(rows_amanda)

    if not rows_amanda:
        raise ValueError(
            "No data was retrieved from the AMANDA database. This should never happen!"
        )

    logger.info("Fetching Knack records...")
    rows_knack = [dict(row) for row in app.get(KNACK_VIEW)]
    rows_knack_deleted = [
        row for row in rows_knack if row[KNACK_IS_DELETED_FIELD] == True
    ]
    rows_knack_active = [
        row for row in rows_knack if row[KNACK_IS_DELETED_FIELD] == False
    ]

    # construct some lists of record PKs to make life easier
    pk_field = get_pk_field()
    knack_id_list_deleted = build_id_list(rows_knack_deleted, pk_field["knack"])
    knack_id_list_active = build_id_list(rows_knack_active, pk_field["knack"])
    knack_id_list_all = knack_id_list_deleted + knack_id_list_active
    amanda_id_list = build_id_list(rows_amanda, pk_field["amanda"])

    # identify amanda records not in Knack
    new_rows_amanda = [
        row for row in rows_amanda if row[pk_field["amanda"]] not in knack_id_list_all
    ]

    # construct record payload for new rows
    new_rows_knack = [map_row(row) for row in new_rows_amanda]

    # construct payload for records in Knack which are deleted but are now active in Amanda
    # this could happen if a fee was voided by mistake
    reactiveate_rows_knack = [
        {"id": row["id"], KNACK_IS_DELETED_FIELD: False}
        for row in rows_knack_deleted
        if row[pk_field["knack"]] in amanda_id_list
    ]

    # identify active records in Knack which have been deleted in Amanda
    delete_rows_knack = [
        {"id": row["id"], KNACK_IS_DELETED_FIELD: True}
        for row in rows_knack_active
        if row[pk_field["knack"]] not in amanda_id_list
    ]

    logger.info(f"{len(new_rows_knack)} fee records to create")
    logger.info(f"{len(reactiveate_rows_knack)} fee records to re-activate")
    logger.info(f"{len(delete_rows_knack)} to delete")

    for row in new_rows_knack:
        try:
            app.record(method="create", obj=KNACK_OBJECT, data=row)
        except requests.exceptions.HTTPError as e:
            logger.error(e.response.text)
            raise e
        logger.info(f"Created Account Bill RSN: {row['field_285']}")

    for row in delete_rows_knack:
        try:
            app.record(method="update", obj=KNACK_OBJECT, data=row)
        except requests.exceptions.HTTPError as e:
            logger.error(e.response.text)
            raise e
        logger.info(f"Soft-deleted knack row id {row['id']}")

    for row in reactiveate_rows_knack:
        try:
            app.record(method="update", obj=KNACK_OBJECT, data=row)
        except requests.exceptions.HTTPError as e:
            logger.error(e.response.text)
            raise e
        logger.info(f"Reactivated Knack row id {row['id']}")


if __name__ == "__main__":
    logger = getLogger(__file__)
    main()
