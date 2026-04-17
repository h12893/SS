IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'laborforce_generation_industry_employ_code'
)
BEGIN
    DROP TABLE laborforce_generation_industry_employ_code
END;

CREATE TABLE laborforce_generation_industry_employ_code (
    job_code INT NOT NULL PRIMARY KEY,
    job_name NVARCHAR(200) NOT NULL,   
);