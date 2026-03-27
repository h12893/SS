PowerBiでの使用クエリの整理

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# 基準年に対する割合算出

## populstion_curated

### Population_Ratio

- 内容：prefecture_code別に2016年の総人口に対する各年の比を算出。
- 形式：メジャー
- 用途：可視化
- 備考：まずは集計対象を「全国」or「都道府県」に限定。

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
    SUM(population_curated[population]),
    base2016
)
```

### Population_Ratio_yyyy

- 内容：yyyyで指定した年度のPopulation_Ratioの値を算出。
- 形式：メジャー
- 用途：Population_Ratio_Category_yyyyの作成に使用
- 備考：カラムで作成するとPopulation_Ratio_Category_yyyy作成時に**計算列の中で、同じテーブルの別の計算列を参照**する状態になり依存関係がループするので、直接可視化に使うかどうかに関わらずメジャーで作成。

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
- 備考：まずは集計対象を「全国」or「都道府県」に限定。

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
    SUM(active_job_openings_curated[job_13]),
    base2016_13
)
```

----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# 指標によるランキング、カテゴリ分け

## populstion_curated

### Population_Ratio_Category_yyyy

- 内容：各都道府県のPopulation_Ratio_yyyyの値を閾値に応じて分類したカテゴリ付与。
- 形式：列
- 用途：Population_Ratioの値で都道府県をカテゴリ分け

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
    r > 1, "1より大きい",
    r > 0.975, "0.975 ~ 1",
    r > 0.95, "0.95 ~ 0.975",
    r > 0.925, "0.925 ~ 0.95",
    r > 0.9, "0.9 ~ 0.925",
    "0.9未満"
)
```

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

----------------------------------------------------------------------------------------------------

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

## Top_N_Selector

```
Top_N_Selector = 
-- 上位（下位）N件をスライサーで動的に変更するためのテーブル
DATATABLE(
    "N", INTEGER,
    {
        {3}, {5}, {10}, {15}  -- Nの候補
    }
)
```


----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------









Is_Top_Bottom_N = 
VAR N = SELECTEDVALUE(Top_N_Selector[N], 5)
VAR currentRank =
    CALCULATE(
        [Population_Ratio_Rank],
        population_curated[prefecture_code]
            = SELECTEDVALUE(prefecture_metadata_codes[prefecture_code])
    )
VAR isTop = currentRank <= N
VAR isBottom = currentRank >= 48 - N + 1
RETURN
IF(isTop || isBottom, 1, 0)



