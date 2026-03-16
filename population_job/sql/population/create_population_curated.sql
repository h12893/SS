IF NOT EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'population_curated'
)
BEGIN
    CREATE TABLE population_curated (
        prefecture_code        INT            NOT NULL,
        year                   INT            NOT NULL,
        population             INT            NULL,
        births                 INT            NULL,
        deaths                 INT            NULL,
        infant_deaths          INT            NULL,
        neonatal_deaths        INT            NULL,
        population_change      INT            NULL,
        stillbirths_total      INT            NULL,
        stillbirths_natural    INT            NULL,
        stillbirths_artificial INT            NULL,
        perinatal_deaths       INT            NULL,
        stillbirths_22weeks    INT            NULL,
        early_neonatal_deaths  INT            NULL,
        marriages              INT            NULL,
        divorces               INT            NULL,
        updated_at             DATETIME       NOT NULL 
        CONSTRAINT DF_population_curated_updated_at DEFAULT (GETDATE()),
        CONSTRAINT PK_population_curated PRIMARY KEY (prefecture_code, year)
);
END;

IF COL_LENGTH('population_curated', 'prefecture_code') IS NULL
BEGIN
    ALTER TABLE population_curated
    ADD prefecture_code INT NOT NULL;
END