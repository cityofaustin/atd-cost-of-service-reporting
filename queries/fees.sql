-- 
-- Queries valid cost of service fees from AMANDA DB. Each row is a billed fee
-- 
SELECT folder.folderrsn,
       folder.foldername,
       folder.folderdescription,
       To_char(folder.indate, 'YYYY-MM-DD')              AS INDATE,
       folder.foldertype,
       validsub.subdesc,
       validwork.workcode,
       validwork.workdesc,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = accountbillfee.folderrsn
               AND folderinfo.infocode = 90005)          work_order,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = accountbillfee.folderrsn
               AND folderinfo.infocode = 75072)          subproject_id,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = accountbillfee.folderrsn
               AND folderinfo.infocode = 76350)          cip_id_number,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = accountbillfee.folderrsn
               AND folderinfo.infocode = 76360)          cip_project_manager,
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
       accountbillfee.feecomment,
       accountbill.billamount,
       accountpayment.paymentnumber,
       accountpayment.paymentamount,
       accountpayment.paymenttype,
       accountpayment.paymentnumber,
       To_char(accountpayment.paymentdate, 'YYYY-MM-DD') AS paymentdate,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = folder.folderrsn
               AND folderinfo.infocode = 90001)          fund,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = folder.folderrsn
               AND folderinfo.infocode = 90002)          dept,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = folder.folderrsn
               AND folderinfo.infocode = 90003)          unit,
       (SELECT infovalue
        FROM   folderinfo
        WHERE  folderinfo.folderrsn = folder.folderrsn
               AND folderinfo.infocode = 90004)          object,
       accountpayment.locationcode,
       accountpayment.stampuser
FROM   accountbillfee
       JOIN validaccountfee
         ON ( accountbillfee.feecode = validaccountfee.feecode )
       JOIN folder
         ON ( accountbillfee.folderrsn = folder.folderrsn )
       JOIN accountbill
         ON ( accountbillfee.billnumber = accountbill.billnumber )
       JOIN accountpaymentdetail
         ON ( accountpaymentdetail.billnumber = accountbill.billnumber )
       JOIN accountpayment
         ON ( accountpayment.paymentnumber =
            accountpaymentdetail.paymentnumber )
       JOIN validsub
         ON ( folder.subcode = validsub.subcode )
       JOIN validwork
         ON ( folder.workcode = validwork.workcode )
       JOIN folderpeople
         ON ( folder.folderrsn = folderpeople.folderrsn
              AND folderpeople.peoplecode = 1 )
       JOIN people
         ON ( folderpeople.peoplersn = people.peoplersn )
WHERE  accountpayment.voidflag = 'N'
       AND accountpayment.paymenttype = 'COS'
       AND accountpayment.paymentdate > To_date('09/30/2021', 'mm/dd/yyyy'); 