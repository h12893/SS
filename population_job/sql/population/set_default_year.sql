DECLARE @constraintName NVARCHAR(200);
DECLARE @sql NVARCHAR(MAX);

-- 既存の DEFAULT 制約を取得
SELECT @constraintName = dc.name
FROM sys.default_constraints dc
JOIN sys.columns c 
    ON dc.parent_object_id = c.object_id 
   AND dc.parent_column_id = c.column_id
WHERE dc.parent_object_id = OBJECT_ID('population_landing')
  AND c.name = 'year';

-- 既存の DEFAULT 制約を削除
IF @constraintName IS NOT NULL
BEGIN
    SET @sql = 'ALTER TABLE population_landing DROP CONSTRAINT ' + QUOTENAME(@constraintName) + ';';
    EXEC(@sql);
END

-- 新しい DEFAULT 制約を追加（@targetYear を使う）
SET @sql = '
ALTER TABLE population_landing
ADD CONSTRAINT DF_population_landing_year DEFAULT (' + CAST(@targetYear AS NVARCHAR(10)) + ') FOR year;
';

EXEC(@sql);
