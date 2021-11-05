"""
- duplicate event type field?
- row per permit or or per fee?
- column names or column order?
"""
import calendar
from datetime import datetime, timezone


def last_day_of_month(record, credit):
    today = datetime.now(timezone.utc)
    month = today.month
    year = today.year
    first_day, last_day = calendar.monthrange(year, month)
    return f"{month}/{last_day}/{year}"


def fiscal_year_today(record, credit):
    today = datetime.now(timezone.utc)
    month = today.month
    year = today.year
    if month > 9:
        return year + 1
    return year


def fiscal_year_payment_date(record, credit):
    # todo: need local time
    payment_date_field = "field_310"
    timestamp = record[payment_date_field]["unix_timestamp"] / 1000
    dt = datetime.utcfromtimestamp(timestamp)
    month = dt.month
    year = dt.year
    if month > 9:
        return year + 1
    return year


def current_month(record, credit):
    today = datetime.now(timezone.utc)
    return today.month


def credit_amount(record, credit):
    return record["field_288"] if credit else 0


def debit_amount(record, credit):
    return 0 if credit else record["field_288"]


def record_name(record, credit):
    folder_rsn = record["field_289"]
    return f"Row Permits - {folder_rsn}"


def fund(record, credit):
    if credit:
        return 5125
    return record["field_311"]


def dept(record, credit):
    if credit:
        return 2400
    return record["field_312"]


def unit(record, credit):
    if credit:
        return 9100
    return record["field_313"]


def object_(record, credit):
    if credit:
        return None
    return record["field_314"]


FIELDS = [
    {"name": "*Spreadsheet Doc Id", "default": "<todo>"},
    {"name": "Auto Numbering"},
    {"name": "Code", "default": "JVD"},
    {"name": "Dept", "default": 2400},
    {"name": "ID", "default": "<todo>"},
    {"name": "Unit", "default": 9100},
    {"name": "LineGroup Line No", "default": "TODO: rowmatch func"},
    {"name": "Accounting Line No", "default": "TODO: rownumber func"},
    {"name": "Document Name", "default": "ROW permits"},
    {"name": "Record Date", "handler": last_day_of_month},
    {"name": "Budget FY", "handler": fiscal_year_today},
    {"name": "Fiscal Year", "handler": fiscal_year_payment_date},
    {"name": "Period", "handler": current_month},
    {"name": "Document Description", "hander": record_name},
    {"name": "Total Credits", "handler": credit_amount},
    {"name": "Total Debits", "handler": debit_amount},
    {"name": "Budget Control Level Reduction"},
    {"name": "Fund Balance Control Level Reduction"},
    {"name": "Cash Balance Control Level Reduction"},
    {"name": "Reversal Date"},
    {"name": "Create Reversal Document on Hold"},
    {"name": "Escrow ID"},
    {"name": "Extended Description"},
    {"name": "Contact Code"},
    {"name": "Created By"},
    {"name": "Created On"},
    {"name": "Modified By"},
    {"name": "Modified On"},
    {"name": "Line Group"},
    {"name": "Event Type", "default": "GA05"},
    {"name": "Posting Pair", "default": "A"},
    {"name": "Posting Pair Name"},
    {"name": "Line Group Description"},
    {"name": "Debit Total", "handler": debit_amount},
    {"name": "Credit Total", "handler": credit_amount},
    {"name": "Cross Appr Unit"},
    {"name": "Ref Doc Code"},
    {"name": "Ref Doc Dept"},
    {"name": "Ref Doc ID"},
    {"name": "Ref Vendor Line"},
    {"name": "Ref Commodity Line"},
    {"name": "Ref Accounting Line"},
    {"name": "Reference Type"},
    {"name": "Event Type", "default": "GA05"},
    {"name": "Posting Pair"},
    {"name": "Posting Pair Name"},
    {"name": "Posting Code", "default": "A001"},
    {"name": "Posting Code Name"},
    {"name": "Accounting Template"},
    {"name": "Line Description", "default": "ROW permits"},
    {"name": "Debit Amount", "handler": debit_amount},
    {"name": "Credit Amount", "handler": credit_amount},
    {"name": "Period"},
    {"name": "Bank", "default": 23},
    {"name": "Ref Doc Code"},
    {"name": "Ref Doc Dept"},
    {"name": "Ref Doc ID"},
    {"name": "Ref Vendor Line"},
    {"name": "Ref Commodity Line"},
    {"name": "Ref Accounting Line"},
    {"name": "Reference Type"},
    {"name": "Fund", "handler": fund},
    {"name": "Department", "handler": dept},
    {"name": "Unit", "handler": unit},
    {"name": "Sub Unit"},
    {"name": "Appr Unit"},
    {"name": "Object", "handler": object_},
    {"name": "Sub Object"},
    {"name": "Revenue", "default": 4057},
    {"name": "Sub Revenue"},
    {"name": "BSA"},
    {"name": "Sub BSA"},
    {"name": "Location"},
    {"name": "Activity"},
    {"name": "Function"},
    {"name": "Reporting"},
    {"name": "Task Order"},
]


# FIELDS = [
#     {"amanda": "accountbillfeersn", "knack": "field_285", "primary_key": True},
#     {"amanda": "feecode", "knack": "field_286"},
#     {"amanda": "feedesc", "knack": "field_287"},
#     {"amanda": "feeamount", "knack": "field_288"},
#     {"amanda": "folderrsn", "knack": "field_289"},
#     {"amanda": "foldername", "knack": "field_290"},
#     {"amanda": "folderdescription", "knack": "field_291"},
#     {"amanda": "indate", "knack": "field_292"},
#     {"amanda": "foldertype", "knack": "field_293"},
#     {"amanda": "subdesc", "knack": "field_294"},
#     {"amanda": "workcode", "knack": "field_295"},
#     {"amanda": "workdesc", "knack": "field_296"},
#     {"amanda": "work_order", "knack": "field_297"},
#     {"amanda": "subproject_id", "knack": "field_298"},
#     {"amanda": "peoplersn", "knack": "field_299"},
#     {"amanda": "namefirst", "knack": "field_300"},
#     {"amanda": "namelast", "knack": "field_301"},
#     {"amanda": "organizationname", "knack": "field_302"},
#     {"amanda": "emailaddress", "knack": "field_303"},
#     {"amanda": "glaccountnumber", "knack": "field_304"},
#     {"amanda": "billnumber", "knack": "field_305"},
#     {"amanda": "billamount", "knack": "field_306"},
#     {"amanda": "paymentamount", "knack": "field_307"},
#     {"amanda": "paymenttype", "knack": "field_308"},
#     {"amanda": "paymentnumber", "knack": "field_309"},
#     {"amanda": "paymentdate", "knack": "field_310"},
#     {"amanda": "fund", "knack": "field_311"},
#     {"amanda": "dept", "knack": "field_312"},
#     {"amanda": "unit", "knack": "field_313"},
#     {"amanda": "object", "knack": "field_314"},
#     {"amanda": "locationcode", "knack": "field_315"},
#     {"amanda": "feecomment", "knack": "field_339"},
#     {"amanda": "cip_project_manager", "knack": "field_341"},
#     {"amanda": "cip_id_number", "knack": "field_337"},
#     {"amanda": "stampuser", "knack": "field_316"},
# ]
