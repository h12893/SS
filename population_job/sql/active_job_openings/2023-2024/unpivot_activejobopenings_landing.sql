INSERT INTO active_job_openings_landing (row_num, prefecture_code, job_code, year, job_count)
SELECT
    row_num,
    prefecture,
    job,
    CAST(REPLACE(year_col, 'year_', '') AS INT) AS year,
    CASE 
        WHEN job_count = '' THEN NULL
        ELSE TRY_CAST(job_count AS INT)
    END AS job_count
FROM (
    SELECT
        row_num,
        prefecture,
        job,
        year_2023,
        year_2024
    FROM active_job_openings_landing_raw 
) AS src
UNPIVOT (
    job_count FOR year_col IN (
        year_2023,
        year_2024
    )
) AS unpvt;
