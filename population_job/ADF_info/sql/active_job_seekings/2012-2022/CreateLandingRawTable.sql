IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_raw_t'
)
BEGIN
    DROP TABLE active_job_seekings_landing_raw_t
END;

CREATE TABLE active_job_seekings_landing_raw_t (
    prefecture             NVARCHAR(200),
    generation             NVARCHAR(200),
    job             NVARCHAR(200),
    year_2012             NVARCHAR(200),
    year_2013             NVARCHAR(200),
    year_2014             NVARCHAR(200),
    year_2015             NVARCHAR(200),
    year_2016             NVARCHAR(200),
    year_2017             NVARCHAR(200),
    year_2018             NVARCHAR(200),
    year_2019             NVARCHAR(200),
    year_2020             NVARCHAR(200),
    year_2021             NVARCHAR(200),
    year_2022             NVARCHAR(200),
);


IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_raw_m'
)
BEGIN
    DROP TABLE active_job_seekings_landing_raw_m
END;

CREATE TABLE active_job_seekings_landing_raw_m (
    prefecture             NVARCHAR(200),
    generation             NVARCHAR(200),
    job             NVARCHAR(200),
    year_2012             NVARCHAR(200),
    year_2013             NVARCHAR(200),
    year_2014             NVARCHAR(200),
    year_2015             NVARCHAR(200),
    year_2016             NVARCHAR(200),
    year_2017             NVARCHAR(200),
    year_2018             NVARCHAR(200),
    year_2019             NVARCHAR(200),
    year_2020             NVARCHAR(200),
    year_2021             NVARCHAR(200),
    year_2022             NVARCHAR(200),
);


IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_raw_f'
)
BEGIN
    DROP TABLE active_job_seekings_landing_raw_f
END;

CREATE TABLE active_job_seekings_landing_raw_f (
    prefecture             NVARCHAR(200),
    generation             NVARCHAR(200),
    job             NVARCHAR(200),
    year_2012             NVARCHAR(200),
    year_2013             NVARCHAR(200),
    year_2014             NVARCHAR(200),
    year_2015             NVARCHAR(200),
    year_2016             NVARCHAR(200),
    year_2017             NVARCHAR(200),
    year_2018             NVARCHAR(200),
    year_2019             NVARCHAR(200),
    year_2020             NVARCHAR(200),
    year_2021             NVARCHAR(200),
    year_2022             NVARCHAR(200),
);
