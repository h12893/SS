IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_openings_landing_raw'
)
BEGIN
    DROP TABLE active_job_openings_landing_raw
END;


CREATE TABLE active_job_openings_landing_raw (
    row_num             INT,
    prefecture             NVARCHAR(200),
    job             NVARCHAR(200),
    year_2023             NVARCHAR(200),
    year_2024             NVARCHAR(200),
);
