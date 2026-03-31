INSERT INTO employments_landing (row_num, prefecture_code, job_code, year, job_count)
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
        year_2012,
        year_2013,
        year_2014,
        year_2015,
        year_2016,
        year_2017,
        year_2018,
        year_2019,
        year_2020,
        year_2021,
        year_2022
    FROM employments_landing_raw 
) AS src
UNPIVOT (
    job_count FOR year_col IN (
        year_2012,
        year_2013,
        year_2014,
        year_2015,
        year_2016,
        year_2017,
        year_2018,
        year_2019,
        year_2020,
        year_2021,
        year_2022
    )
) AS unpvt;
