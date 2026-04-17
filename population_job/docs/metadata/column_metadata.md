カラム内容一覧

----------------------------------------------------------------------------------------------------

# population_curated

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 都道府県コード | - | 〇 | 〇 | 都道府県を示すコード |
| 2 | year | INT | NO | 年度 | 年 | 〇 | 〇 | レコードの該当年度 |
| 3 | population | INT | YES | 人口 | 人 | - | - | - |
| 4 | births | INT | YES | 出生数 | 人 | - | - | - |
| 5 | deaths | INT | YES | 死亡数 | 人 | - | - | - |
| 6 | infant_deaths | INT | YES | 乳児死亡数 | 人 | - | - | - |
| 7 | neonatal_deaths | INT | YES | 新生児死亡数 | 人 | - | - | - |
| 8 | population_change | INT | YES | 人口増減 | 人 | - | - | - |
| 9 | stillbirths_total | INT | YES | 死産総数 | 人 | - | - | - |
| 10 | stillbirths_natural | INT | YES | 自然死産 | 人 | - | - | - |
| 11 | stillbirths_artificial | INT | YES | 人工死産 | 人 | - | - | - |
| 12 | perinatal_deaths | INT | YES | 周産期死亡 | 人 | - | - | - |
| 13 | stillbirths_22weeks | INT | YES | 22週以降死産 | 人 | - | - | - |
| 14 | early_neonatal_deaths | INT | YES | 早期新生児死亡 | 人 | - | - | - |
| 15 | marriages | INT | YES | 婚姻件数 | 人 | - | - | - |
| 16 | divorces | INT | YES | 離婚件数 | 人 | - | - | - |
| 17 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 更新日時（自動更新） |

----------------------------------------------------------------------------------------------------

# prefecture_metadata_codes

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 都道府県コード | - | 〇 | 〇 | 都道府県を示すコード |
| 2 | prefecture_name | NVARCHAR(200) | NO | 都道府県名 | - | - | - | 都道府県名 |
| 3 | region_code | INT | NO | 地域分類コード | - | - | - | 地域の粒度を「全国」, 「都道府県」, 「政令市、23区」, 「外国」, 「不詳」で分類した場合のコード |
| 4 | region_type | NVARCHAR(200) | YES | 地域分類 | - | - | - | 地域の分類粒度（「全国」, 「都道府県」, 「政令市、23区」, 「外国」, 「不詳」） |

----------------------------------------------------------------------------------------------------

# active_job_openings_curated

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 都道府県コード | - | 〇 | 〇 | 都道府県を示すコード |
| 2 | year | INT | NO | 年度 | 年 | 〇 | 〇 | レコードの該当年度 |
| 3 ~ 88 | job_1 ~ job_86 | INT | YES | 業種別有効求人数 | 人 | - | - | サフィックスの番号が業種コードと対応する分類の有効求人数を表す |
| 89 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 更新日時（自動更新） |

----------------------------------------------------------------------------------------------------

# active_job_openings_metadata_codes

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | job_code | INT | NO | 業種コード | - | 〇 | 〇 | 業種の分類を示すコード |
| 2 | job_name_2012_2022 | NVARCHAR(200) | NO | 業種名 | - | - | - | 2012年～2022年の業種名（コード値は2023年以降と同一） |
| 3 | job_name_2023_ | NVARCHAR(200) | NO | 業種名 | - | - | - | 2023年以降の業種名（コード値は2023年以降と同一） |
| 4 | classification_code | INT | YES | 中分類コード | - | - | - | 業種の中分類のコード値 |
| 5 | classification | NVARCHAR(200) | YES | 中分類名 | - | - | - | 業種の中分類名 |
| 6 | classification_hierarchy_code | INT | YES | 分類階層コード | - | - | - | 業種の分類階層のコード値 |
| 7 | classification_hierarchy | NVARCHAR(200) | YES | 分類階層 | - | - | - | 業種の分類階層 |

----------------------------------------------------------------------------------------------------

# employments_curated

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 都道府県コード | - | 〇 | 〇 | 都道府県を示すコード |
| 2 | year | INT | NO | 年度 | 年 | 〇 | 〇 | レコードの該当年度 |
| 3 ~ 88 | job_1 ~ job_86 | INT | YES | 業種別就職人数 | 人 | - | - | サフィックスの番号が業種コードと対応する分類の就職人数を表す |
| 89 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 更新日時（自動更新） |

----------------------------------------------------------------------------------------------------

# active_job_seekings_curated

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 都道府県コード | - | 〇 | 〇 | 都道府県を示すコード |
| 2 | sex_code | INT | NO | 性別コード | - | 〇 | 〇 | 性別を表すコード |
| 3 | generation_code | INT | NO | 年代コード | - | 〇 | 〇 | 年代を表すコード |
| 4 | year | INT | NO | 年度 | 年 | 〇 | 〇 | レコードの該当年度 |
| 5 ~ 90 | job_1 ~ job_86 | INT | YES | 業種別有効求職者数 | 人 | - | - | サフィックスの番号が業種コードと対応する分類の有効求職者数を表す |
| 91 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 更新日時（自動更新） |

----------------------------------------------------------------------------------------------------

# sex_metadata_codes

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | sex_code | INT | NO | 性別コード | - | 〇 | 〇 | 性別を示すコード |
| 2 | sex | NVARCHAR(200) | NO | 性別 | - | - | - | 性別 |

----------------------------------------------------------------------------------------------------

# generation_metadata_codes

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | generation_code | INT | NO | 年代別コード | - | 〇 | 〇 | 年代を示すコード |
| 2 | generation | NVARCHAR(200) | NO | 年代 | - | - | - | 年代（5歳刻み） |

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_curated

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | sex_code | INT | NO | 性別コード | - | 〇 | 〇 | 性別を表すコード |
| 2 | generation_code | INT | NO | 年代コード | - | 〇 | 〇 | 年代を表すコード |
| 3 | year | INT | NO | 年度 | 年 | 〇 | 〇 | レコードの該当年度 |
| 4 ~ 102 | job_1 ~ job_99 | INT | YES | 業種別就業者数 | 万人 | - | - | サフィックスの番号が業種コードと対応する分類の就業者数を表す |
| 103 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 更新日時（自動更新） |

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_codes

| number | column_name | type | nullable | japanese_column_name | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|----------------------|------|-------------|-------------|-------|
| 1 | job_code | INT | NO | 業種コード | - | 〇 | 〇 | 業種の分類を示すコード |
| 2 | job_name | NVARCHAR(200) | NO | 業種名 | - | - | - | 業種名 |

----------------------------------------------------------------------------------------------------

