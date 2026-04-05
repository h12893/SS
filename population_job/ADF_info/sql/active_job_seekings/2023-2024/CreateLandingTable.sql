IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_t'
)
BEGIN
    DROP TABLE active_job_seekings_landing_t
END;

CREATE TABLE active_job_seekings_landing_t (
    prefecture_code INT,
    sex_code INT,
    generation_code INT,
    job_code INT,
    year INT,
    job_count INT,
);


IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_m'
)
BEGIN
    DROP TABLE active_job_seekings_landing_m
END;

CREATE TABLE active_job_seekings_landing_m (
    prefecture_code INT,
    sex_code INT,
    generation_code INT,
    job_code INT,
    year INT,
    job_count INT,
);


IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_seekings_landing_f'
)
BEGIN
    DROP TABLE active_job_seekings_landing_f
END;

CREATE TABLE active_job_seekings_landing_f (
    prefecture_code INT,
    sex_code INT,
    generation_code INT,
    job_code INT,
    year INT,
    job_count INT,
);
