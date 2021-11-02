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
