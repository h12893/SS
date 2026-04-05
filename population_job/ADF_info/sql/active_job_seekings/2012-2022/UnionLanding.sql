IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing'
)
BEGIN
    DROP TABLE active_job_seekings_landing
END;

CREATE TABLE active_job_seekings_landing (
    prefecture_code INT,
    sex_code INT,
    generation_code INT,
    job_code INT,
    year INT,
    job_count INT,
);

INSERT INTO active_job_seekings_landing (prefecture_code, sex_code, generation_code, job_code, year, job_count)
    SELECT
        prefecture_code, 
        sex_code, 
        generation_code, 
        job_code, 
        year, 
        job_count
    FROM active_job_seekings_landing_t

        UNION ALL

    SELECT
        prefecture_code, 
        sex_code, 
        generation_code, 
        job_code, 
        year, 
        job_count
    FROM active_job_seekings_landing_m

        UNION ALL

    SELECT
        prefecture_code, 
        sex_code, 
        generation_code, 
        job_code, 
        year, 
        job_count
    FROM active_job_seekings_landing_f

