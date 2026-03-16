IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_openings_landing'
)
BEGIN
    DROP TABLE active_job_openings_landing 
END;

CREATE TABLE active_job_openings_landing (
    row_num INT,
    prefecture_code INT,
    job_code INT,
    year INT,
    job_count INT,
);
