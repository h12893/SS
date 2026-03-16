------------------------------------------------------------
-- 1. 全角数字 → 半角数字変換テーブル
------------------------------------------------------------
DECLARE @tbl TABLE(z NCHAR(1), h NCHAR(1));
INSERT INTO @tbl(z, h)
VALUES (N'０',N'0'),(N'１',N'1'),(N'２',N'2'),(N'３',N'3'),(N'４',N'4'),
       (N'５',N'5'),(N'６',N'6'),(N'７',N'7'),(N'８',N'8'),(N'９',N'9');

------------------------------------------------------------
-- 2. prefecture_code の設定（全国=0、外=48、不詳=49）
------------------------------------------------------------
UPDATE l
SET prefecture_code =
    CASE
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'全%' COLLATE Japanese_CI_AS THEN 0
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'外%' COLLATE Japanese_CI_AS THEN 48
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'不%' COLLATE Japanese_CI_AS THEN 49
        ELSE TRY_CAST(
            (
                SELECT h 
                FROM @tbl 
                WHERE z = SUBSTRING(prefecture COLLATE Japanese_CI_AS, 1, 1)
            ) +
            (
                SELECT h 
                FROM @tbl 
                WHERE z = SUBSTRING(prefecture COLLATE Japanese_CI_AS, 2, 1)
            )
            AS INT
        )
    END
FROM population_landing l;