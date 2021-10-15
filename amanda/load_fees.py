import os
import csv

import cx_Oracle

from utils.postgrest import Postgrest

# docker run -it --rm --env-file env_file --network host -v /Users/john/Dropbox/atd/atd-cost-of-service-reporting/amanda:/app atddocker/amanda-reporting /bin/bash

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SERVICE = os.getenv("SERVICE")
QUERYPATH = "queries/fees.sql"
PGREST_ENDPOINT="http://127.0.0.1:3000"
PGREST_JWT=None

def get_conn(host, port, service, user, password):
  dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
  return cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)

def load_query(fname):
  with open(fname, "r") as fin:
    # cx_Oracle does not want a statement to end with `;`
    return fin.read().replace(";", "")

def lower_case_keys(rows):
  data = []
  for row in rows:
    new = {k.lower(): v for k, v in row.items()}
    data.append(new)
  return data
    

def main():
  conn = get_conn(HOST, PORT, SERVICE, USER, PASSWORD)
  query = load_query(QUERYPATH)
  cursor = conn.cursor()
  cursor.execute(query)

  # define row handler which returns each row as a dict
  # h/t https://stackoverflow.com/questions/35045879/cx-oracle-how-can-i-receive-each-row-as-a-dictionary
  cursor.rowfactory = lambda *args: dict(
      zip([d[0] for d in cursor.description], args)
  )
  rows = cursor.fetchall()
  conn.close()

  if not rows:
      raise IOError(
          "No data was retrieved from the financial database. This should never happen!"
      )

  rows = lower_case_keys(rows)
  client = Postgrest(PGREST_ENDPOINT, token=PGREST_JWT)
  client.upsert("fees", rows)
  print(f"{len(rows)} upserted")
  
  data = client.select("fee_report", order_by="Application date")
  
  with open("report.csv", "w") as fout:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
      writer.writerow(row)

main()

# curl -H 'Accept: text/csv' localhost:3000/fee_report   