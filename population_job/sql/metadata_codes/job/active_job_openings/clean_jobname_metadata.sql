-- job_name_2012_2022内の空白削除
UPDATE active_job_openings_metadata_codes
SET job_name_2012_2022 = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name_2012_2022))

-- job_name_2023_内の空白削除
UPDATE active_job_openings_metadata_codes
SET job_name_2023_  = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name_2023_))
