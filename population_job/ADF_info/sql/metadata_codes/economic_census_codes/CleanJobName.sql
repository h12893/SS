-- job_name_2012内の空白削除
UPDATE economic_census_code
SET job_name_2012 = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name_2012))

-- job_name_2016内の空白削除
UPDATE economic_census_code
SET job_name_2016 = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name_2016))

-- job_name_2021内の空白削除
UPDATE economic_census_code
SET job_name_2021 = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name_2021))