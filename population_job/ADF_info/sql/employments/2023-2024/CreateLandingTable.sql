IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'employments_landing'
)
BEGIN
    DROP TABLE employments_landing 
END;

CREATE TABLE employments_landing (
    row_num INT,
    prefecture_code INT,
    job_code INT,
    year INT,
    job_count INT,
);
