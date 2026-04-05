IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'sex_metadata_codes'
)
BEGIN
    DROP TABLE sex_metadata_codes
END;

CREATE TABLE sex_metadata_codes (
    sex_code INT NOT NULL PRIMARY KEY,
    sex NVARCHAR(200) NOT NULL,
);

IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'generation_metadata_codes'
)
BEGIN
    DROP TABLE generation_metadata_codes
END;

CREATE TABLE generation_metadata_codes (
    generation_code INT NOT NULL PRIMARY KEY,
    generation NVARCHAR(200) NOT NULL,
);