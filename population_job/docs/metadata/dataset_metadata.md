# Dataset Metadata

## population_curated
- **説明**: 年次人口統計の Fact テーブル
- **主キー**: prefecture_code, year
- **更新頻度**: 年次
- **データソース**: [「人口動向調査」](https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450011&tstat=000001028897) （厚生労働省）
- **格納場所**:
  - Raw: /raw/population/
  - Landing: population_landing
  - Curated: population_curated
- **関連ディメンション**: metadata_codes
- **変換ロジック**: transform_rules.md を参照
- **最終更新日**: 2026-02-25
