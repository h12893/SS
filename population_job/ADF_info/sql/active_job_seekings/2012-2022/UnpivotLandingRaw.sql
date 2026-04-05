INSERT INTO active_job_seekings_landing_t (prefecture_code, sex_code, generation_code, job_code, year, job_count)
SELECT
    prefecture,
    0,
    generation,
    job,
    CAST(REPLACE(year_col, 'year_', '') AS INT) AS year,
    CASE 
        WHEN job_count = '' THEN NULL
        ELSE TRY_CAST(job_count AS INT)
    END AS job_count
FROM (
    SELECT
        prefecture,
        generation,
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
    FROM active_job_seekings_landing_raw_t
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

INSERT INTO active_job_seekings_landing_m (prefecture_code, sex_code, generation_code, job_code, year, job_count)
SELECT
    prefecture,
    1,
    generation,
    job,
    CAST(REPLACE(year_col, 'year_', '') AS INT) AS year,
    CASE 
        WHEN job_count = '' THEN NULL
        ELSE TRY_CAST(job_count AS INT)
    END AS job_count
FROM (
    SELECT
        prefecture,
        generation,
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
    FROM active_job_seekings_landing_raw_m
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

INSERT INTO active_job_seekings_landing_f (prefecture_code, sex_code, generation_code, job_code, year, job_count)
SELECT
    prefecture,
    2,
    generation,
    job,
    CAST(REPLACE(year_col, 'year_', '') AS INT) AS year,
    CASE 
        WHEN job_count = '' THEN NULL
        ELSE TRY_CAST(job_count AS INT)
    END AS job_count
FROM (
    SELECT
        prefecture,
        generation,
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
    FROM active_job_seekings_landing_raw_f
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
