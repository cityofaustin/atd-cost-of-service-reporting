



SELECT DISTINCT
    folder.folderrsn,
    folder.foldername,
    folder.folderdescription,
    folder.folderyear || ' ' || folder.foldersequence || ' ' || folder.foldertype AS folder_id,
    To_char(folder.indate, 'YYYY-MM-DD') AS INDATE,
    folder.foldertype,
    validsub.subdesc,
    validwork.workcode,
    validwork.workdesc,
    (
        SELECT
            infovalue
        FROM
            folderinfo
        WHERE
            folderinfo.folderrsn = accountbillfee.folderrsn
            AND folderinfo.infocode = 90005) work_order, (
            SELECT
                infovalue
            FROM
                folderinfo
            WHERE
                folderinfo.folderrsn = accountbillfee.folderrsn
                AND folderinfo.infocode = 75072) subproject_id, (
                SELECT
                    infovalue
                FROM
                    folderinfo
                WHERE
                    folderinfo.folderrsn = accountbillfee.folderrsn
                    AND folderinfo.infocode = 76350) cip_id_number, (
                    SELECT
                        infovalue
                    FROM
                        folderinfo
                    WHERE
                        folderinfo.folderrsn = accountbillfee.folderrsn
                        AND folderinfo.infocode = 76360) cip_project_manager, (
                        SELECT
                            infovalue
                        FROM
                            folderinfo
                        WHERE
                            folderinfo.folderrsn = accountbillfee.folderrsn
                            AND folderinfo.infocode = 75074) partner_dept_name, people.namefirst, people.namelast, people.organizationname, people.emailaddress, folderpeople.folderrsn, people.peoplersn, validaccountfee.glaccountnumber, validaccountfee.feedesc, accountbillfee.accountbillfeersn, accountbillfee.feecode, accountbillfee.feeamount, accountbillfee.billnumber, accountbillfee.feecomment, accountbill.billamount, accountpayment.paymentnumber, accountpayment.paymentamount, accountpayment.paymenttype,
                        --accountpayment.paymentnumber,
                        To_char(accountpayment.paymentdate, 'YYYY-MM-DD') AS paymentdate, (
                            SELECT
                                infovalue
                            FROM
                                folderinfo
                            WHERE
                                folderinfo.folderrsn = folder.folderrsn
                                AND folderinfo.infocode = 90001) fund, (
                                SELECT
                                    infovalue
                                FROM
                                    folderinfo
                                WHERE
                                    folderinfo.folderrsn = folder.folderrsn
                                    AND folderinfo.infocode = 90002) dept, (
                                    SELECT
                                        infovalue
                                    FROM
                                        folderinfo
                                    WHERE
                                        folderinfo.folderrsn = folder.folderrsn
                                        AND folderinfo.infocode = 90003) unit, (
                                        SELECT
                                            infovalue
                                        FROM
                                            folderinfo
                                        WHERE
                                            folderinfo.folderrsn = folder.folderrsn
                                            AND folderinfo.infocode = 90004) object, accountpayment.locationcode, accountpayment.stampuser
                                    FROM
                                        accountbillfee
                                        JOIN validaccountfee ON (accountbillfee.feecode = validaccountfee.feecode)
                                        JOIN folder ON (accountbillfee.folderrsn = folder.folderrsn)
                                        JOIN accountbill ON (accountbillfee.billnumber = accountbill.billnumber)
                                        JOIN accountpaymentdetail ON (accountpaymentdetail.billnumber = accountbill.billnumber)
                                        JOIN accountpayment ON (accountpayment.paymentnumber = accountpaymentdetail.paymentnumber)
                                        LEFT OUTER JOIN validsub ON (folder.subcode = validsub.subcode)
                                        LEFT OUTER JOIN validwork ON (folder.workcode = validwork.workcode)
                                        LEFT OUTER JOIN folderpeople ON (folder.folderrsn = folderpeople.folderrsn
                                                AND folderpeople.peoplecode = 1)
                                        LEFT OUTER JOIN people ON (folderpeople.peoplersn = people.peoplersn)
                                WHERE
                                    accountpayment.voidflag = 'N'
                                    AND accountpayment.paymenttype = 'COS'
                                    AND accountpayment.paymentdate > To_date('09/30/2021', 'mm/dd/yyyy');