データセット内容一覧

----------------------------------------------------------------------------------------------------

# population_curated

### 説明
年次人口統計の Fact テーブル
### 更新頻度
年次
### データソース
- [人口動向調査](https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450011&tstat=000001028897) （厚生労働省）
### 格納場所
#### Raw 
- /raw-data/government-statistical/population/人口動態_都道府県_yyyy.csv (yyyy = 2016 ~ 2024)
#### Curated
population-dynamics-prefecture.dbo.population_curated
### 関連ディメンション
- population-dynamics-prefecture.dbo.prefecture_metadata_codes

----------------------------------------------------------------------------------------------------

# prefecture_metadata_codes

### 説明
都道府県、地域の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
無し（ADF上でpopulation_curatedの内容より作成）
### 格納場所
#### Raw
無し
#### Curated
population-dynamics-prefecture.dbo.prefecture_metadata_codes
### 関連ディメンション
無し

----------------------------------------------------------------------------------------------------

# active_job_openings_curated

### 説明
有効求人統計の Fact テーブル
### 更新頻度
年次
### データソース
- [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番4
### 格納場所
#### Raw
- /raw-data/government-statistical/job/有効求人数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
#### Curated
population-dynamics-prefecture.dbo.active_job_openings_curated
### 関連ディメンション 
- population-dynamics-prefecture.dbo.active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_openings_metadata_codes

### 説明
業種の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
- active_job_openings_code.csv（active_job_openings_curatedの内容より作成）
### 格納場所
#### Raw 
- /raw-data/government-statistical/job/active_job_openings_code.csv
#### Curated
population-dynamics-prefecture.dbo.active_job_openings_metadata_codes
### 関連ディメンション
無し

----------------------------------------------------------------------------------------------------

# employments_curated

### 説明
就職件数統計の Fact テーブル
### 更新頻度
年次
### データソース
- [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番8
### 格納場所
#### Raw
- /raw-data/government-statistical/job/就職件数_常用のみ_都道府県別_中分類_2012~2024_rownum追加.xlsx
#### Curated
population-dynamics-prefecture.dbo.employments_curated
### 関連ディメンション 
- population-dynamics-prefecture.dbo.active_job_openings_metadata_codes

----------------------------------------------------------------------------------------------------

# active_job_seekings_curated

### 説明
有効求職者統計の Fact テーブル
### 更新頻度
年次
### データソース
- [雇用関係指標（年度）](https://www.mhlw.go.jp/toukei/list/114-1d.html) （厚生労働省）　通番5
### 格納場所
#### Raw
- /raw-data/government-statistical/job/有効求職者数_常用のみ_都道府県別_男女別_年代別_中分類_2012~2024_コード変換済み_〇〇.xlsx（〇〇部分は年代分類）
#### Curated
population-dynamics-prefecture.dbo.active_job_seekings_curated
### 関連ディメンション 
- population-dynamics-prefecture.dbo.active_job_openings_metadata_codes
- population-dynamics-prefecture.dbo.sex_metadata_codes
- population-dynamics-prefecture.dbo.generation_metadata_codes

----------------------------------------------------------------------------------------------------

# sex_metadata_codes

### 説明
性別の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
- demogra_code.xlsxのsexシート（active_job_seekings_curatedの内容より作成）
### 格納場所
#### Raw 
- /raw-data/government-statistical/job/demogra_code.xlsx
#### Curated
population-dynamics-prefecture.dbo.sex_metadata_codes
### 関連ディメンション
無し

----------------------------------------------------------------------------------------------------

# generation_metadata_codes

### 説明
年代の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
- demogra_code.xlsxのgenerationシート（active_job_seekings_curatedの内容より作成）
### 格納場所
#### Raw 
- /raw-data/government-statistical/job/demogra_code.xlsx
#### Curated
population-dynamics-prefecture.dbo.generation_metadata_codes
### 関連ディメンション
無し

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_curated

### 説明
労働力調査（全国の総就業者数）の Fact テーブル
### 更新頻度
年次
### データソース
- [「労働力調査」（総務省）](https://www.e-stat.go.jp/statistics/00200531)
    - 政府統計名：労働力調査	
    - 提供統計名：労働力調査	
    - 提供分類1：基本集計　全都道府県	
    - 提供分類2：全国	
    - 提供分類3：年次	
    - 提供周期：年次
    - 表番号：2-2-1
    - 表題：年齢階級，産業別就業者数（2007年～）-第12・13回改定産業分類による
### 格納場所
#### Raw
- /raw-data/government-statistical/job/「労働力調査」（総務省）/労働力調査_年齢階級別_産業別_就業者数.csv
#### Curated
population-dynamics-prefecture.dbo.laborforce_generation_industry_employ_curated
### 関連ディメンション
- laborforce_generation_industry_employ_codes
- sex_metadata_codes
- generation_metadata_codes
### 補足
性別と年代のコード値と内容の対応に関してはsex_metadata_codesとgeneration_metadata_codesを流用  
- 性別に関しては以下の変更が必要だが、本質的には違いが無いのでそのまま使用
    - 整形 → 総数
- 年代に関しては、本テーブルの元データでは集計対象が15歳以上に限定されているので以下の変更が必要だが、本質的には違いが無いのでそのまま使用
    - 年齢計 → 15歳以上
    - 19歳以下 → 15~19歳

----------------------------------------------------------------------------------------------------

# laborforce_generation_industry_employ_codes

### 説明
労働力調査における業種の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
 - laborforce_generation_industry_employ_code.csv（laborforce_generation_industry_employ_curatedの内容より作成）
### 格納場所
#### Raw 
- /raw-data/government-statistical/job/コード値/laborforce_generation_industry_employ_code.csv
#### Curated
population-dynamics-prefecture.dbo.laborforce_generation_industry_employ_codes
### 関連ディメンション
無し

----------------------------------------------------------------------------------------------------

# economic_census_employments_curated

### 説明
経済センサス（都道府県×業種×性別での就業者数）の Fact テーブル
### 更新頻度
5年ごと（2011年は震災の影響で2012年に実施）
### データソース
- [「経済センサス」（総務省・経済産業省）](https://www.e-stat.go.jp/statistics/00200553)
    1. 2021年
        - 政府統計名：経済センサス‐活動調査	
        - 提供統計名：令和３年経済センサス‐活動調査	
        - 提供分類1：事業所に関する集計	
        - 提供分類2：産業横断的集計	
        - 提供分類3：事業所数、従業者数	
        - 表番号：2-1
        - 表題：産業(中分類)、経営組織(8区分)別全事業所数、男女別従業者数及び常用雇用者数－全国、都道府県、大都市 
    2. 2016年    
        - 政府統計名：経済センサス‐活動調査	
        - 提供統計名：平成28年経済センサス‐活動調査
        - 提供分類1：事業所に関する集計	
        - 提供分類2：産業横断的集計	
        - 表番号：4-2
        - 表題：産業（中分類），経営組織（７区分），従業上の地位（６区分），男女別従業者数―全国，都道府県，大都市  
    3. 2012年    
        - 政府統計名：経済センサス‐活動調査	
        - 提供統計名：平成24年経済センサス‐活動調査
        - 提供分類1：事業所に関する集計	
        - 提供分類2：産業横断的集計	
        - 表番号：5-2
        - 表題：産業(中分類)，経営組織(７区分)，従業上の地位(６区分)，男女別従業者数―全国，都道府県，大都市 ### 格納場所
#### Raw
- /raw-data/government-statistical/job/「経済センサス」（総務省・経済産業省）/経済センサス_産業_事業所数_雇用者数_都道府県_2021年_X.csv（X = 1 or 2）
- /raw-data/government-statistical/job/「経済センサス」（総務省・経済産業省）/経済センサス_産業_雇用者数_都道府県_2016年_X.csvX = 1 ~ 5）
- /raw-data/government-statistical/job/「経済センサス」（総務省・経済産業省）/経済センサス_産業_雇用者数_都道府県_2012年_X.csvX = 1 ~ 5）
#### Curated
population-dynamics-prefecture.dbo.economic_census_employments_curated
### 関連ディメンション
- economic_census_code
- prefecture_metadata_codes
### 補足
都道府県のコード値と内容の対応に関してはprefecture_metadata_codesを流用  

----------------------------------------------------------------------------------------------------

# economic_census_code

### 説明
経済センサスにおける業種の Dimension テーブル
### 更新頻度
不定期（コード内容に更新があった際に更新）
### データソース
 economic_census_code.csv（economic_census_employments_curatedの内容より作成）
### 格納場所
#### Raw 
- /raw-data/government-statistical/job/コード値/economic_census_code.csv
#### Curated
population-dynamics-prefecture.dbo.economic_census_code
### 関連ディメンション
無し
