データセット内容一覧

----------------------------------------------------------------------------------------------------

# population_curated

- **説明**: 年次人口統計の Fact テーブル
- **主キー**: prefecture_code, year
- **更新頻度**: 年次
- **データソース**: [人口動向調査](https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450011&tstat=000001028897) （厚生労働省）
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/population/人口動態_都道府県_yyyy.csv (yyyy = 2016 ~ 2024)
  - Landing:
      - population_landing （保存なし）
  - Curated:
      - population_curated
- **関連ディメンション**: prefecture_metadata_codes

----------------------------------------------------------------------------------------------------

# prefecture_metadata_codes

- **説明**: 都道府県、地域の Dimension テーブル
- **主キー**: prefecture_code
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: population_curatedの内容より作成
- **格納場所**:
  - Raw: 
      - 無し
  - Landing:
      - 無し
  - Curated:
      - prefecture_metadata_codes
- **関連ディメンション**: 無し

----------------------------------------------------------------------------------------------------

# active_job_openings_curated

- **説明**: 有効求人統計の Fact テーブル
- **主キー**: prefecture_code, year
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番4
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/有効求人数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
  - Landing:
      - active_job_openings_landing （保存なし）
  - Curated:
      - active_job_openings_curated
- **関連ディメンション**: active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_openings_metadata_codes

- **説明**: 業種の Dimension テーブル
- **主キー**: job_code
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番4の内容より作成
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/job/active_job_openings_code.csv
  - Landing:
      - 無し
  - Curated:
      - active_job_openings_metadata_codes
- **関連ディメンション**: 無し

----------------------------------------------------------------------------------------------------

# employments_curated

- **説明**: 就職件数統計の Fact テーブル
- **主キー**: prefecture_code, year
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番8
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/就職件数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
  - Landing:
      - employments_landing （保存なし）
  - Curated:
      - employments_curated
- **関連ディメンション**: active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_seekings_curated

- **説明**: 有効求職者統計の Fact テーブル
- **主キー**: prefecture_code, sex_code, generation_code, year
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番5
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/有効求職者数_常用のみ_都道府県別_男女別_年代別_中分類_2012~2024_コード変換済み_〇〇.xlsx（〇〇部分は年代分類）
  - Landing:
      - active_job_seekings_landing （保存なし）
  - Curated:
      - active_job_seekings_curated
- **関連ディメンション**: active_job_openings_metadata_codes, sex_metadata_codes, generation_metadata_codes

----------------------------------------------------------------------------------------------------

# sex_metadata_codes

- **説明**: 性別の Dimension テーブル
- **主キー**: sex_code
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番5の内容より作成
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/job/demogra_code.xlsx
  - Landing:
      - 無し
  - Curated:
      - sex_metadata_codes
- **関連ディメンション**: 無し

----------------------------------------------------------------------------------------------------

# generation_metadata_codes

- **説明**: 年代の Dimension テーブル
- **主キー**: generation_code
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番5の内容より作成
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/job/demogra_code.xlsx
  - Landing:
      - 無し
  - Curated:
      - generation_metadata_codes
- **関連ディメンション**: 無し

----------------------------------------------------------------------------------------------------
