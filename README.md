# atd-cost-of-service-reporting

Automated data processing for ATD's cost of service fee collection.

## Background

Austin Transportation provides various permitting services for fellow City departments. Effective Oct 1, 2021, ATD collects the same processsing feess from City departments its does non-City customers. We call this new fee collection procedure and supporting IT systems "Cost of Service Reporting."

## Business process - overview

1. A City department applies for an ATD-managed permit. For example, an excavation permit.
2. Automated processes in the AMANDA permitting system apply the appropriate fees to the application. By default, the fees are flagged in the AMANDA database as "paid". In fact, the fee has not been paid: funds will need to be completed via an interdepartmental transfer known as a journal voucher (JV).
3. On a monthly basis, a report is generated (with the help of this repo) which itemizes the fees assessed by each department. The report includes detail about the related permit, applicant, etc.
4. Each department is sent a list of the fees they have accrued. Departments review the fee list and confirm the assessment is accurate and provide funding numbers (FDUs) from which funds will be drawn to pay the fee balance.
5. Once approved, ATD Finance staff create journal vouchers which transfer funds from the partner department to ATD.


### Technical process

We use a Knack application, the "Right of Way Portal" as canonical repository for tracking these fees. This app allows business users to review, download, and distribute fee records for further review and processing by staff.

Cost of service fees records are extracted from the AMANDA database and loaded into Knack using `knack_load_fees.py`. The `where` clause used to extract these fees is quite simple:

```sql
    -- payment is not voided
    WHERE  accountpayment.voidflag = 'N'
    -- payment type is cost of service ('COS')
    AND accountpayment.paymenttype = 'COS'
    -- payment date is after sep 30, 2021 (the program started on 10/1/2021)
    AND accountpayment.paymentdate > To_date('09/30/2021', 'mm/dd/yyyy');
```

Each time the script runs, it queries all fees in AMANDA, compares the records to all fees in Knack, and inserts or updates records in the Knack app accordingly.

Records are uniquely identified the `accountbillfeersn` column, which identifies a single permit fee. A single permit often has multiple cost of service fees.

If a fee record exists in AMANDA that does not exist in Knack, the fee record is created in Knack. As well, formerly valid fees are occasionally voided in AMANDA, in which case they will be absent from the AMANDA database. If a fee record exists in Knack but is no longer in the AMANDA extract, the fee record is updated in Knack with a status of `deleted=true`. 
