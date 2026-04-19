IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'economic_census_code'
)
BEGIN
    DROP TABLE economic_census_code
END;

CREATE TABLE economic_census_code(
        job_code INT NOT NULL PRIMARY KEY,
        job_name_2012 NVARCHAR(200) NOT NULL,
        job_name_2016 NVARCHAR(200) NOT NULL,
        job_name_2021 NVARCHAR(200) NOT NULL,
);