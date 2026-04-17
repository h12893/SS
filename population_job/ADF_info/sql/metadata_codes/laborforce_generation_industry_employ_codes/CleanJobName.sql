-- job_name内の空白削除
UPDATE laborforce_generation_industry_employ_code
SET job_name = TRIM(BOTH ' ' FROM TRIM(BOTH '　' FROM job_name))