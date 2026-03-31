IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'employments_landing_raw'
)
BEGIN
    DROP TABLE employments_landing_raw
END;

CREATE TABLE employments_landing_raw (
    row_num             INT,
    prefecture             NVARCHAR(200),
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
