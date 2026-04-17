データセット内容一覧

----------------------------------------------------------------------------------------------------

# population_curated

- **説明**: 年次人口統計の Fact テーブル
- **更新頻度**: 年次
- **データソース**: [人口動向調査](https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450011&tstat=000001028897) （厚生労働省）
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/population/人口動態_都道府県_yyyy.csv (yyyy = 2016 ~ 2024)
  - Landing:
      - population_landing （保存なし）
  - Curated:
      - population_curated
- **関連ディメンション**:
    - prefecture_metadata_codes

----------------------------------------------------------------------------------------------------

# prefecture_metadata_codes

- **説明**: 都道府県、地域の Dimension テーブル
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
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番4
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/有効求人数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
  - Landing:
      - active_job_openings_landing （保存なし）
  - Curated:
      - active_job_openings_curated
- **関連ディメンション**: 
    - active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_openings_metadata_codes

- **説明**: 業種の Dimension テーブル
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: active_job_openings_curatedの内容より作成
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
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番8
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/就職件数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
  - Landing:
      - employments_landing （保存なし）
  - Curated:
      - employments_curated
- **関連ディメンション**: 
    - active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_seekings_curated

- **説明**: 有効求職者統計の Fact テーブル
- **更新頻度**: 年次
- **データソース**: [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番5
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/有効求職者数_常用のみ_都道府県別_男女別_年代別_中分類_2012~2024_コード変換済み_〇〇.xlsx（〇〇部分は年代分類）
  - Landing:
      - active_job_seekings_landing （保存なし）
  - Curated:
      - active_job_seekings_curated
- **関連ディメンション**: 
    - active_job_openings_metadata_codes
    - sex_metadata_codes
    - generation_metadata_codes

----------------------------------------------------------------------------------------------------

# sex_metadata_codes

- **説明**: 性別の Dimension テーブル
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: active_job_seekings_curatedの内容より作成
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
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: active_job_seekings_curatedの内容より作成
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/job/demogra_code.xlsx
  - Landing:
      - 無し
  - Curated:
      - generation_metadata_codes
- **関連ディメンション**: 無し

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_curated

- **説明**: 労働力調査（全国の総就業者数）の Fact テーブル
- **更新頻度**: 年次
- **データソース**: [「労働力調査」（総務省）](https://www.e-stat.go.jp/statistics/00200531)
    - 政府統計名：労働力調査	
    - 提供統計名：労働力調査	
    - 提供分類1：基本集計　全都道府県	
    - 提供分類2：全国	
    - 提供分類3：年次	
    - 提供周期：年次
    - 表番号：2-2-1
    - 表題：年齢階級，産業別就業者数（2007年～）-第12・13回改定産業分類による
- **格納場所**:
  - Raw:
      - /raw-data/government-statistical/job/「労働力調査」（総務省）/労働力調査_年齢階級別_産業別_就業者数.csv
  - Landing:
      - laborforce_generation_industry_employ_landing_raw （保存なし）
  - Curated:
      - laborforce_generation_industry_employ_curated
- **関連ディメンション**: 
    - laborforce_generation_industry_employ_codes
    - sex_metadata_codes
    - generation_metadata_codes
- **補足**：性別と年代のコード値と内容の対応に関してはsex_metadata_codesとgeneration_metadata_codesを流用  
    - 性別に関しては以下の変更が必要だが、本質的には違いが無いのでそのまま使用
        - 整形 → 総数
    - 年代に関しては、本テーブルの元データでは集計対象が15歳以上に限定されているので以下の変更が必要だが、本質的には違いが無いのでそのまま使用
        - 年齢計 → 15歳以上
        - 19歳以下 → 15~19歳

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_codes

- **説明**: 労働力調査における業種の Dimension テーブル
- **更新頻度**: 不定期（コード内容に更新があった際に更新）
- **データソース**: laborforce_generation_industry_employ_curatedの内容より作成
- **格納場所**:
  - Raw: 
      - /raw-data/government-statistical/job/コード値/laborforce_generation_industry_employ_code.csv
  - Landing:
      - 無し
  - Curated:
      - laborforce_generation_industry_employ_codes
- **関連ディメンション**: 無し
