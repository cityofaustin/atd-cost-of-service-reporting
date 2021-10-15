SELECT
  folder.folderrsn,
  folder.foldername,
  folder.folderdescription,
  to_char(folder.indate, 'YYYY-MM-DD') as INDATE,
  folder.foldertype,
  validsub.subdesc,
  validwork.workcode,
  validwork.workdesc,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = accountbillfee.folderrsn
      and folderinfo.infocode = 90005
  ) work_order,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = accountbillfee.folderrsn
      and folderinfo.infocode = 75072
  ) subproject_id,
  
  -- ( select people.namefirst from people where people.peoplersn = folderpeople.peoplersn and folderpeople.peoplecode = 1) namefirst,
  -- ( select people.namelast from people where people.peoplersn = folderpeople.peoplersn and folderpeople.peoplecode = 1) namelast,
  people.namefirst,
  people.namelast,
  people.organizationname,
  people.emailaddress,
  folderpeople.folderrsn,
  people.peoplersn,
  validaccountfee.glaccountnumber,
  validaccountfee.feedesc,
  accountbillfee.accountbillfeersn,
  accountbillfee.feecode,
  accountbillfee.feeamount,
  accountbillfee.billnumber,
  accountbill.billamount,
  accountpayment.paymentamount,
  accountpayment.paymenttype,
  accountpayment.paymentnumber,
  to_char(accountpayment.paymentdate, 'YYYY-MM-DD') as paymentdate,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = folder.folderrsn
      and folderinfo.infocode = 90001
  ) fund,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = folder.folderrsn
      and folderinfo.infocode = 90002
  ) dept,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = folder.folderrsn
      and folderinfo.infocode = 90003
  ) unit,
  (
    Select
      infovalue
    from
      folderinfo
    where
      folderinfo.folderrsn = folder.folderrsn
      and folderinfo.infocode = 90004
  ) object,
  accountpayment.locationcode,
  accountpayment.stampuser
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
  JOIN folderpeople on (folder.folderrsn = folderpeople.folderrsn and folderpeople.peoplecode = 1)
  join people on (folderpeople.peoplersn = people.peoplersn)
where
  accountpayment.voidflag is not null
  and accountpayment.paymenttype = 'COS'
  and accountpayment.paymentdate  > to_date('09/30/2021', 'mm/dd/yyyy');