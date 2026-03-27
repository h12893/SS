IF EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'prefecture_metadata_codes'
)
BEGIN
    DROP TABLE prefecture_metadata_codes
END;

CREATE TABLE prefecture_metadata_codes(
    prefecture_code INT NOT NULL PRIMARY KEY,
    prefecture_name NVARCHAR(200) NOT NULL,
    region_code TINYINT NOT NULL,   -- 0:「全国」, 1:「都道府県」, 2:「政令市、23区」, 3:「外国」, 4:「不詳」
    region_type NVARCHAR(500) NULL
);