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
  column_name = 'glaccountnumber';

-- # folder infos
-- 90001	Fund
-- 90002	Department
-- 90003	Unit
-- 90004	Object
-- 90005	Work Order #
-- 75072 Subproject
-- folder.infocode (90001, 90002, 90003, 90004, 90005, 75072)

-- TODOS
-- all info codes except subproject ID
-- select * from VALIDINFO where VALIDINFO.INFOGROUP = 'Cost of Service';

-- plus subproject ID #
-- 75072

-- partner depaartment comes from multiple places
-- not available from UC or GF

-- TURP: Partner Dept is workdesc
-- Partner department for EX is folder ssubtype

-- permit types:
-- TURP: folder.foldertype = 'RW' and subtype (validsub) is temporary use of right of way

-- one per transaction
-- each fee in the cell comma separated 

-- get bill total off of accountbill. line items are accountbillfee. b
-- each row in mockup should eb a bill
