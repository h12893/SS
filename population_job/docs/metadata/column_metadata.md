# Column Metadata

## population_curated

| number | column_name | type | nullable | description | unit | primary key | foreign key | notes |
|--------|-------------|------|----------|-------------|------|-------------|-------------|-------|
| 1 | prefecture_code | INT | NO | 地域コード | - | 〇 | 〇 | metadata_codes と JOIN |
| 2 | year | INT | NO | 年度 | 年 | 〇 | 〇 | - |
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
| 17 | updated_at | DATETIME | NO | 更新日時 | - | - | - | 自動更新 |


