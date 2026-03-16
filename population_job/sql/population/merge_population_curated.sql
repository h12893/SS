CREATE PROCEDURE sp_population_merge
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH src AS (
        SELECT
            prefecture_code,
            year,
            TRY_CAST(NULLIF(population, '') AS INT) AS population,
            TRY_CAST(NULLIF(births, '') AS INT) AS births,
            TRY_CAST(NULLIF(deaths, '') AS INT) AS deaths,
            TRY_CAST(NULLIF(infant_deaths, '') AS INT) AS infant_deaths,
            TRY_CAST(NULLIF(neonatal_deaths, '') AS INT) AS neonatal_deaths,
            TRY_CAST(NULLIF(population_change, '') AS INT) AS population_change,
            TRY_CAST(NULLIF(stillbirths_total, '') AS INT) AS stillbirths_total,
            TRY_CAST(NULLIF(stillbirths_natural, '') AS INT) AS stillbirths_natural,
            TRY_CAST(NULLIF(stillbirths_artificial, '') AS INT) AS stillbirths_artificial,
            TRY_CAST(NULLIF(perinatal_deaths, '') AS INT) AS perinatal_deaths,
            TRY_CAST(NULLIF(stillbirths_22weeks, '') AS INT) AS stillbirths_22weeks,
            TRY_CAST(NULLIF(early_neonatal_deaths, '') AS INT) AS early_neonatal_deaths,
            TRY_CAST(NULLIF(marriages, '') AS INT) AS marriages,
            TRY_CAST(NULLIF(divorces, '') AS INT) AS divorces
        FROM population_landing
        WHERE prefecture_code IS NOT NULL
    )
    MERGE INTO population_curated AS tgt
    USING src
      ON tgt.prefecture_code = src.prefecture_code
     AND tgt.year           = src.year

    WHEN MATCHED THEN
        UPDATE SET
            tgt.population            = src.population,
            tgt.births                = src.births,
            tgt.deaths                = src.deaths,
            tgt.infant_deaths         = src.infant_deaths,
            tgt.neonatal_deaths       = src.neonatal_deaths,
            tgt.population_change     = src.population_change,
            tgt.stillbirths_total     = src.stillbirths_total,
            tgt.stillbirths_natural   = src.stillbirths_natural,
            tgt.stillbirths_artificial= src.stillbirths_artificial,
            tgt.perinatal_deaths      = src.perinatal_deaths,
            tgt.stillbirths_22weeks   = src.stillbirths_22weeks,
            tgt.early_neonatal_deaths = src.early_neonatal_deaths,
            tgt.marriages             = src.marriages,
            tgt.divorces              = src.divorces,
            tgt.updated_at            = GETDATE()

    WHEN NOT MATCHED THEN
        INSERT (
            prefecture_code,
            year,
            population,
            births,
            deaths,
            infant_deaths,
            neonatal_deaths,
            population_change,
            stillbirths_total,
            stillbirths_natural,
            stillbirths_artificial,
            perinatal_deaths,
            stillbirths_22weeks,
            early_neonatal_deaths,
            marriages,
            divorces,
            updated_at
        )
        VALUES (
            src.prefecture_code,
            src.year,
            src.population,
            src.births,
            src.deaths,
            src.infant_deaths,
            src.neonatal_deaths,
            src.population_change,
            src.stillbirths_total,
            src.stillbirths_natural,
            src.stillbirths_artificial,
            src.perinatal_deaths,
            src.stillbirths_22weeks,
            src.early_neonatal_deaths,
            src.marriages,
            src.divorces,
            GETDATE()
        );
END;