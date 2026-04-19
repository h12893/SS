IF NOT EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'economic_census_employments_curated'
)

CREATE TABLE economic_census_employments_curated(
    prefecture_code INT NOT NULL,
    year INT NOT NULL,
    industry_code INT NOT NULL,
    employments_total_t INT NULL,
    employments_total_m INT NULL,
    employments_total_f INT NULL,
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_economic_census_employments_curated PRIMARY KEY (prefecture_code, year, industry_code)
);
