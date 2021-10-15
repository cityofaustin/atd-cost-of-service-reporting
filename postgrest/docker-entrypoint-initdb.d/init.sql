-- docker run -it --rm --network host postgres psql -h localhost -U postgres

create role authenticator noinherit;
create role web_anon nologin;
create schema api;
grant usage on schema api to web_anon;

SET
    search_path TO api,
    public;

create table api.fees (
    accountbillfeersn integer primary key,
    feecode integer not null,
    feedesc text,
    feeamount numeric,
    folderrsn integer not null,
    foldername text,
    folderdescription text,
    indate timestamp without time zone,
    foldertype text,
    subdesc text,
    workcode integer,
    workdesc text,
    work_order text,
    subproject_id text,
    peoplersn integer,
    namefirst text,
    namelast text,
    organizationname text,
    emailaddress text,
    glaccountnumber text,
    billnumber integer,
    billamount numeric,
    paymentamount numeric,
    paymenttype text,
    paymentnumber integer,
    paymentdate timestamp without time zone,
    fund integer,
    dept integer,
    unit integer,
    object integer,
    locationcode integer,
    stampuser text
);

create view api.fee_report as (
    select
    folderrsn "Permit RSN",
    foldertype "Permit Type",
    subdesc "Permit Subtype",
    workdesc "Work Description",
    foldername "Permit Name",
    to_char(indate, 'MM/DD/YYYY') "Application date",
    work_order "Work Order #",
    subproject_id "Subproject ID",
    namefirst || ' ' || namelast "Applicant name",
    emailaddress "Email",
    organizationname "Organization Name",
    fund "Fund",
    dept "Dept",
    unit "Unit",
    object "Object",
    billnumber "Bill Number",
    accountbillfeersn "Fee Number",
    feedesc "Fee Name",
    cast(feeamount as money) "Fee Amount",
    cast(billamount as money) "Bill Amount",
    'https://abc.austintexas.gov/public-search-other?t_detail=1&t_selected_folderrsn=' || folderrsn "URL",
    null "Dept. Approval"
    from api.fees
    order by indate asc
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA api TO web_anon;
