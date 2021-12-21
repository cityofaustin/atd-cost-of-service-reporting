import logging
import os
import sys

import cx_Oracle
import knackpy

# db vars
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SERVICE = os.getenv("SERVICE")
# knack auth
KNACK_API_KEY = os.getenv("KNACK_API_KEY")
KNACK_APP_ID = os.getenv("KNACK_APP_ID")
# config
QUERYPATH = "queries/fees.sql"
KNACK_VIEW = "view_54"
KNACK_OBJECT = "object_14"
KNACK_IS_DELETED_FIELD = "field_336"

FIELDS = [
    {"amanda": "accountbillfeersn", "knack": "field_285", "primary_key": True},
    {"amanda": "feecode", "knack": "field_286"},
    {"amanda": "feedesc", "knack": "field_287"},
    {"amanda": "feeamount", "knack": "field_288"},
    {"amanda": "folderrsn", "knack": "field_289"},
    {"amanda": "foldername", "knack": "field_290"},
    {"amanda": "folderdescription", "knack": "field_291"},
    {"amanda": "indate", "knack": "field_292"},
    {"amanda": "foldertype", "knack": "field_293"},
    {"amanda": "subdesc", "knack": "field_294"},
    {"amanda": "workcode", "knack": "field_295"},
    {"amanda": "workdesc", "knack": "field_296"},
    {"amanda": "work_order", "knack": "field_297"},
    {"amanda": "subproject_id", "knack": "field_298"},
    {"amanda": "peoplersn", "knack": "field_299"},
    {"amanda": "namefirst", "knack": "field_300"},
    {"amanda": "namelast", "knack": "field_301"},
    {"amanda": "organizationname", "knack": "field_302"},
    {"amanda": "emailaddress", "knack": "field_303"},
    {"amanda": "glaccountnumber", "knack": "field_304"},
    {"amanda": "billnumber", "knack": "field_305"},
    {"amanda": "billamount", "knack": "field_306"},
    {"amanda": "paymentamount", "knack": "field_307"},
    {"amanda": "paymenttype", "knack": "field_308"},
    {"amanda": "paymentnumber", "knack": "field_309"},
    {"amanda": "paymentdate", "knack": "field_310"},
    {"amanda": "fund", "knack": "field_311"},
    {"amanda": "dept", "knack": "field_312"},
    {"amanda": "unit", "knack": "field_313"},
    {"amanda": "object", "knack": "field_314"},
    {"amanda": "locationcode", "knack": "field_315"},
    {"amanda": "feecomment", "knack": "field_339"},
    {"amanda": "cip_project_manager", "knack": "field_341"},
    {"amanda": "cip_id_number", "knack": "field_337"},
    {"amanda": "stampuser", "knack": "field_316"},
    {"amanda": "partner_dept_name", "knack": "field_342"},
    {"amanda": "folder_id", "knack": "field_355"}
]


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
    logger.debug("Fetching AMANDA records...")

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
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    rows_amanda = fetch_amanda_records()
    rows_amanda = lower_case_keys(rows_amanda)
    if not rows_amanda:
        raise ValueError(
            "No data was retrieved from the AMANDA database. This should never happen!"
        )

    logger.debug("Fetching Knack records...")
    rows_knack = [dict(row) for row in app.get(KNACK_VIEW)]
    pk_field = get_pk_field()
    knack_id_list = build_id_list(rows_knack, pk_field["knack"])
    amanda_id_list = build_id_list(rows_amanda, pk_field["amanda"])

    new_rows_amanda = [
        row for row in rows_amanda if row[pk_field["amanda"]] not in knack_id_list
    ]

    new_rows_knack = [map_row(row) for row in new_rows_amanda]

    delete_rows_knack = [
        {"id": row["id"], KNACK_IS_DELETED_FIELD: True}
        for row in rows_knack
        if row[pk_field["knack"]] not in amanda_id_list
    ]

    logger.info(f"{len(new_rows_knack)} fee records to create")

    for row in new_rows_knack:
        app.record(method="create", obj=KNACK_OBJECT, data=row)
        print("created one")

    logger.info(f"{len(delete_rows_knack)} fee records to delete")

    for row in delete_rows_knack:
        # soft delete fee records
        app.record(method="update", obj=KNACK_OBJECT, data=row)
        print("updated one")


if __name__ == "__main__":
    logger = getLogger(__file__)
    main()
