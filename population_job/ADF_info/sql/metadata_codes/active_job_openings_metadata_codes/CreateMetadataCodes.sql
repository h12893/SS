IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'active_job_openings_metadata_codes'
)
BEGIN
    DROP TABLE active_job_openings_metadata_codes
END;

CREATE TABLE active_job_openings_metadata_codes (
    job_code INT NOT NULL PRIMARY KEY,
    job_name_2012_2022 NVARCHAR(200) NOT NULL,   -- 2012~2022年と2023年~で表記が異なる（内容は同じ）なのでカラムを分ける
    job_name_2023_ NVARCHAR(200) NOT NULL,   -- 2012~2022年と2023年~で表記が異なる（内容は同じ）なのでカラムを分ける
    classification_code INT,
    classification NVARCHAR(200),
    classification_hierarchy_code INT,
    classification_hierarchy NVARCHAR(200)
);