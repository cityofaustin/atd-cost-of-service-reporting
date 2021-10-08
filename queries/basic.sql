--  sample folders
select
  *
from
  folder
where
  folderrsn in (12796688, 12796669, 12795210);

-- use to find occurences of colum name
select
  owner,
  table_name
from
  all_tab_columns
where
  column_name = 'DEPARTMENTDESC';

SELECT
  distinct folder.folderrsn,
  folder.foldername,
  folder.folderdescription,
  validaccountfee.glaccountnumber --, abf.feecode
,
  validaccountfee.feedesc,
  accountbillfee.feeamount,
  accountbillfee.billnumber,
  accountpayment.paymentamount --, accountpayment.amountapplied
,
  accountpayment.paymenttype,
  accountpayment.paymentnumber,
  accountpayment.paymentdate last_paymentdate,
  accountpayment.locationcode location_code,
  accountpayment.paymentcomment checknumber,
  accountpayment.stampuser,
  validsub.subcode,
  validsub.subdesc,
  validwork.workcode,
  validwork.workdesc,
  people.namefirst,
  people.namelast
FROM
  accountbillfee
  JOIN validaccountfee ON (accountbillfee.feecode = validaccountfee.feecode)
  JOIN folder ON (accountbillfee.folderrsn = folder.folderrsn)
  JOIN accountbill ON (
    accountbillfee.billnumber = accountbill.billnumber
  )
  JOIN accountpaymentdetail ON (
    accountpaymentdetail.billnumber = accountbill.billnumber
  )
  JOIN accountpayment ON (
    accountpayment.paymentnumber = accountpaymentdetail.paymentnumber
  )
  JOIN validsub on (folder.subcode = validsub.subcode)
  JOIN validwork on (folder.workcode = validwork.workcode)
  JOIN folderpeople on (folder.folderrsn = folderpeople.folderrsn)
  join people on (folderpeople.peoplersn = people.peoplersn)
where
  accountpayment.voidflag is not null
  and accountpayment.paymenttype = 'COS'
  and rownum < 10;