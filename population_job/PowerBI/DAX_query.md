PowerBiでの使用クエリの整理

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# 基準年に対する割合算出

## population_curated

### Population_Ratio

- 内容：prefecture_code別に2016年の総人口に対する各年の比を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。%単位に変換。

```
Population_Ratio = 
VAR base2016 = 
    CALCULATE(
        SUM(population_curated[population]),
        population_curated[year] = 2016 &&  -- 基準年度として2016年を指定
        0 <= population_curated[prefecture_code] && population_curated[prefecture_code] <= 47  -- 集計対象は「全国」or「都道府県」
    )
RETURN
DIVIDE(
    SUM(population_curated[population])*100,
    base2016
)
```

### Population_Ratio_yyyy

- 内容：yyyyで指定した年度のPopulation_Ratioの値を算出。
- 形式：メジャー
- 用途：Population_Ratio_Category_yyyyの作成に使用
- 備考：カラムで作成するとPopulation_Ratio_Category_yyyy作成時に**計算列の中で、同じテーブルの別の計算列を参照**する状態になり依存関係がループするので、直接可視化に使うかどうかに関わらずメジャーで作成。Population_Ratioが%単位なのでPopulation_Ratio_yyyyも%単位。

```
Population_Ratio_2024 = 
CALCULATE(
    [Population_Ratio],
    population_curated[year] = 2024
)
```

----------------------------------------------------------------------------------------------------

## active_job_openings_curated

### job_13_Ratio

- 内容：prefecture_code別に2016年のjob_13（「10情報処理・通信技術」の有効求人数）に対する各年の比を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。%単位に変換。

```
job_13_Ratio = 
VAR base2016_13 = 
    CALCULATE(
        SUM(active_job_openings_curated[job_13]),
        active_job_openings_curated[year] = 2016 &&  -- 基準年度として2016年を指定
        0 <= active_job_openings_curated[prefecture_code] && active_job_openings_curated[prefecture_code] <= 47  -- 集計対象は「全国」or「都道府県」
    )
RETURN
DIVIDE(
    SUM(active_job_openings_curated[job_13])*100,
    base2016_13
)
```

----------------------------------------------------------------------------------------------------

## employments_curated

### job_13_Ratio

- 内容：prefecture_code別に2016年のjob_13（「10情報処理・通信技術」の有効求人数）に対する各年の比を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。%単位に変換。

```
job_13_Ratio = 
VAR base2016_13 = 
    CALCULATE(
        SUM(employments_curated[job_13]),
        employments_curated[year] = 2016 &&  -- 基準年度として2016年を指定
        0 <= employments_curated[prefecture_code] && employments_curated[prefecture_code] <= 47  -- 集計対象は「全国」or「都道府県」
    )
RETURN
DIVIDE(
    SUM(employments_curated[job_13])*100,
    base2016_13
)
```

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# 複数指標間の比較指標

## population_curated


----------------------------------------------------------------------------------------------------

## active_job_openings_curated

### job_13_Ratio_by_Total

- 内容：prefecture_code別にjob_1（「職業計」の有効求人数）に対するjob_13（「10情報処理・通信技術」の有効求人数）の比（総有効求人に対して「10情報処理・通信技術」の有効求人が占める割合）を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。%単位に変換。

```
job_13_Ratio_by_Total = 
DIVIDE(
    SUM(active_job_openings_curated[job_13])*100,
    SUM(active_job_openings_curated[job_1])
)
```

### job_13_Ratio_by_Population

- 内容：prefecture_code別に人口に対するjob_13（「10情報処理・通信技術」の有効求人数）の比（一人当たりのjob_13の有効求人数）を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。分母の人口は労働世代以外や既就職者も含むのに対して、分子の有効求人数は労働世代かつ未就職者に対するものであるので、割合は非常に小さくなり、指標としては使いづらい。

```
job_13_Ratio_by_Population = 
DIVIDE(
    SUM(active_job_openings_curated[job_13]),
    CALCULATE(
        SUM(population_curated[population])
    )
)

```

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# 指標によるランキング、カテゴリ分け

## population_curated

### Population_Ratio_Category_yyyy

割合系の算出を%単位に変換したことで機能しなくなったので、暫定的に使用しないように変更。

~~
- 内容：各都道府県のPopulation_Ratio_yyyyの値を閾値に応じて分類したカテゴリ付与。
- 形式：列
- 用途：Population_Ratioの値で都道府県をカテゴリ分け
- Population_Ratio_Category_yyyyを凡例に、prefecture_nameをスモールマルチプルに指定することで、都道府県別のグラフが表示されて線の色や凡例はPopulation_Ratio_Category_yyyyの内容で分類される。

```
Population_Ratio_Category_2024 = 
VAR r = 
    CALCULATE(
        [Population_Ratio_2024],
        ALLEXCEPT(population_curated, population_curated[prefecture_code])
    )
RETURN
SWITCH(
    TRUE(),
    r > 100, "100%より大きい",
    r > 97.5, "97.5 ~ 100%",
    r > 95, "95 ~ 97.5%",
    r > 92.5, "92.5 ~ 95%",
    r > 90, "90 ~ 92.5%",
    "90%未満"
)
```
~~

### Prefecture_Name

- 内容：prefecture_codeに対応するprefecture_nameをprefecture_metadata_codesから取得。
- 形式：列
- 用途：Population_Ratio_Rankの作成に使用
- 備考：population_curatedのprefecture_codeを使用した場合、凡例にprefecture_metadata_codesのprefecture_nameを指定すると全てのランクが1になる不具合が発生するので、別で都道府県名カラムを作成。原因はリレーションによってフィルタリングがprefecture_metadata_codesにも伝播していると考えられる。

```
Prefecture_Name = 
LOOKUPVALUE(
    prefecture_metadata_codes[prefecture_name],        -- 取得したい列
    prefecture_metadata_codes[prefecture_code],         -- 検索対象列
    [prefecture_code],              -- 検索値
    ""                     -- 該当なし時の代替値（任意）
)
```

### Population_Ratio_Rank

- 内容：Population_Ratioの値の降順にランク付け。
- 形式：メジャー
- 用途：Population_Ratioの上位（下位）N件のみの抽出に使用

```
Population_Ratio_Rank = 
VAR _table = 
    FILTER(
        ALL(population_curated[Prefecture_Name]),
        population_curated[Prefecture_Name] IN {"全国","北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"}
    )
RETURN
RANKX(
    _table,
    [Population_Ratio],
    ,
    DESC
)
```

### Is_Top_Bottom_N_Population_Ratio_Rank

- 内容：Population_Ratio_Rankが上位、下位N件に該当するかどうかのフラグ。
- 形式：メジャー
- 用途：Population_Ratio_Rankの上位、下位N件の絞り込み

```
Is_Top_Bottom_N_Population_Ratio_Rank = 
VAR N = SELECTEDVALUE(Top_N_Selector[N], 5)
VAR currentRank = [Population_Ratio_Rank]
VAR isTop = currentRank <= N
VAR isBottom = currentRank >= 48 - N + 1
RETURN
IF(isTop || isBottom, 1, 0)
```

----------------------------------------------------------------------------------------------------

## active_job_openings_curated

### Prefecture_Name

- 内容：prefecture_codeに対応するprefecture_nameをprefecture_metadata_codesから取得。
- 形式：列
- 用途：job_13_Ratio_Rankの作成に使用
- 備考：active_job_openings_curatedのprefecture_codeを使用した場合、凡例にprefecture_metadata_codesのprefecture_nameを指定すると全てのランクが1になる不具合が発生するので、別で都道府県名カラムを作成。原因はリレーションによってフィルタリングがprefecture_metadata_codesにも伝播していると考えられる。

```
Prefecture_Name = 
LOOKUPVALUE(
    prefecture_metadata_codes[prefecture_name],
    prefecture_metadata_codes[prefecture_code],
    [prefecture_code],
    ""
)
```

### job_13_Ratio_Rank

- 内容：job_13_Ratioの値の降順にランク付け。
- 形式：メジャー
- 用途：job_13_Ratioの上位（下位）N件のみの抽出に使用

```
job_13_Ratio_Rank = 
VAR _table = 
    FILTER(
        ALL(active_job_openings_curated[Prefecture_Name]),
        active_job_openings_curated[Prefecture_Name] IN {"全国","北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"}
    )
RETURN
RANKX(
    _table,
    [job_13_Ratio],
    ,
    DESC
)
```

### Is_Top_Bottom_N_job_13_Ratio_Rank

- 内容：job_13_Ratio_Rankが上位、下位N件に該当するかどうかのフラグ。
- 形式：メジャー
- 用途：job_13_Ratio_Rankの上位、下位N件の絞り込み

```
Is_Top_Bottom_N_job_13_Ratio_Rank = 
VAR N = SELECTEDVALUE(Top_N_Selector[N], 5)
VAR currentRank = [job_13_Ratio_Rank]
VAR isTop = currentRank <= N
VAR isBottom = currentRank >= 48 - N + 1
RETURN
IF(isTop || isBottom, 1, 0)
```

----------------------------------------------------------------------------------------------------

## Top_N_Selector

- 内容：上位、下位N件を抽出する際のスライサー作成用のテーブル。
- 形式：テーブル
- 用途：件数指定用のスライサー
- 備考：件数Nとして指定したい値を必要に応じて追加する。まずは1~10と15の11種で作成。

```
Top_N_Selector = 
-- 上位（下位）N件をスライサーで動的に変更するためのテーブル
DATATABLE(
    "N", INTEGER,
    {
        {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {15}  -- Nの候補
    }
)
```


----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------











