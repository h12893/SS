IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'population_landing'
)
BEGIN
    DROP TABLE population_landing
END;

CREATE TABLE population_landing(
    prefecture_code             NVARCHAR(200),
    prefecture             NVARCHAR(200),
    year             NVARCHAR(200),
    population             NVARCHAR(200),
    births             NVARCHAR(200),
    deaths             NVARCHAR(200),
    infant_deaths             NVARCHAR(200),
    neonatal_deaths             NVARCHAR(200),
    population_change             NVARCHAR(200),
    stillbirths_total             NVARCHAR(200),
    stillbirths_natural             NVARCHAR(200),
    stillbirths_artificial             NVARCHAR(200),
    perinatal_deaths             NVARCHAR(200),
    stillbirths_22weeks             NVARCHAR(200),
    early_neonatal_deaths             NVARCHAR(200),
    marriages             NVARCHAR(200),
    divorces             NVARCHAR(200),
);

IF COL_LENGTH('population_landing', 'prefecture_code') IS NULL
BEGIN
    ALTER TABLE population_landing
    ADD prefecture_code INT NULL;
END