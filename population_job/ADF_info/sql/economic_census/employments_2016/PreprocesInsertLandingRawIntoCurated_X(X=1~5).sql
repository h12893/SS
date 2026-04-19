-- prefectreu_codeへの変換
UPDATE economic_census_employments_landing_raw
SET column_3 =
    CASE
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'全国%' COLLATE Japanese_CI_AS THEN 0
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'北海道%' COLLATE Japanese_CI_AS THEN 1
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'青森県%' COLLATE Japanese_CI_AS THEN 2
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'岩手県%' COLLATE Japanese_CI_AS THEN 3
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'宮城県%' COLLATE Japanese_CI_AS THEN 4
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'秋田県%' COLLATE Japanese_CI_AS THEN 5
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'山形県%' COLLATE Japanese_CI_AS THEN 6
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'福島県%' COLLATE Japanese_CI_AS THEN 7
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'茨城県%' COLLATE Japanese_CI_AS THEN 8
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'栃木県%' COLLATE Japanese_CI_AS THEN 9
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'群馬県%' COLLATE Japanese_CI_AS THEN 10
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'埼玉県%' COLLATE Japanese_CI_AS THEN 11
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'千葉県%' COLLATE Japanese_CI_AS THEN 12
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'東京都%' COLLATE Japanese_CI_AS THEN 13
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'神奈川県%' COLLATE Japanese_CI_AS THEN 14
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'新潟県%' COLLATE Japanese_CI_AS THEN 15
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'富山県%' COLLATE Japanese_CI_AS THEN 16
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'石川県%' COLLATE Japanese_CI_AS THEN 17
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'福井県%' COLLATE Japanese_CI_AS THEN 18
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'山梨県%' COLLATE Japanese_CI_AS THEN 19
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'長野県%' COLLATE Japanese_CI_AS THEN 20
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'岐阜県%' COLLATE Japanese_CI_AS THEN 21
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'静岡県%' COLLATE Japanese_CI_AS THEN 22
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'愛知県%' COLLATE Japanese_CI_AS THEN 23
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'三重県%' COLLATE Japanese_CI_AS THEN 24
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'滋賀県%' COLLATE Japanese_CI_AS THEN 25
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'京都府%' COLLATE Japanese_CI_AS THEN 26
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'大阪府%' COLLATE Japanese_CI_AS THEN 27
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'兵庫県%' COLLATE Japanese_CI_AS THEN 28
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'奈良県%' COLLATE Japanese_CI_AS THEN 29
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'和歌山県%' COLLATE Japanese_CI_AS THEN 30
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'鳥取県%' COLLATE Japanese_CI_AS THEN 31
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'島根県%' COLLATE Japanese_CI_AS THEN 32
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'岡山県%' COLLATE Japanese_CI_AS THEN 33
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'広島県%' COLLATE Japanese_CI_AS THEN 34
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'山口県%' COLLATE Japanese_CI_AS THEN 35
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'徳島県%' COLLATE Japanese_CI_AS THEN 36
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'香川県%' COLLATE Japanese_CI_AS THEN 37
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'愛媛県%' COLLATE Japanese_CI_AS THEN 38
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'高知県%' COLLATE Japanese_CI_AS THEN 39
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'福岡県%' COLLATE Japanese_CI_AS THEN 40
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'佐賀県%' COLLATE Japanese_CI_AS THEN 41
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'長崎県%' COLLATE Japanese_CI_AS THEN 42
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'熊本県%' COLLATE Japanese_CI_AS THEN 43
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'大分県%' COLLATE Japanese_CI_AS THEN 44
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'宮崎県%' COLLATE Japanese_CI_AS THEN 45
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'鹿児島県%' COLLATE Japanese_CI_AS THEN 46
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'沖縄県%' COLLATE Japanese_CI_AS THEN 47
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'外%' COLLATE Japanese_CI_AS THEN 48
        WHEN column_3 COLLATE Japanese_CI_AS LIKE N'不%' COLLATE Japanese_CI_AS THEN 49
        ELSE 49
    END
FROM economic_census_employments_landing_raw;

-- industry_codeへの変換
UPDATE economic_census_employments_landing_raw
SET column_9 =
    CASE

	WHEN column_9 = N'A～R全産業（Ｓ公務を除く）' THEN 2
	WHEN column_9 = N'A～B農林漁業' THEN 3
	WHEN column_9 = N'A農業，林業' THEN 4
	WHEN column_9 = N'01農業' THEN 5
	WHEN column_9 = N'02林業' THEN 6
	WHEN column_9 = N'B漁業' THEN 7
	WHEN column_9 = N'03漁業（水産養殖業を除く）' THEN 8
	WHEN column_9 = N'04水産養殖業' THEN 9
	
	
	WHEN column_9 = N'C～R非農林漁業（Ｓ公務を除く）' THEN 12
	WHEN column_9 = N'C鉱業，採石業，砂利採取業' THEN 13
	WHEN column_9 = N'05鉱業，採石業，砂利採取業' THEN 14
	WHEN column_9 = N'D建設業' THEN 15
	WHEN column_9 = N'06総合工事業' THEN 16
	WHEN column_9 = N'07職別工事業（設備工事業を除く）' THEN 17
	WHEN column_9 = N'08設備工事業' THEN 18
	
	WHEN column_9 = N'E製造業' THEN 20
	WHEN column_9 = N'09食料品製造業' THEN 21
	WHEN column_9 = N'10飲料・たばこ・飼料製造業' THEN 22
	WHEN column_9 = N'11繊維工業' THEN 23
	WHEN column_9 = N'12木材・木製品製造業（家具を除く）' THEN 24
	WHEN column_9 = N'13家具・装備品製造業' THEN 25
	WHEN column_9 = N'14パルプ・紙・紙加工品製造業' THEN 26
	WHEN column_9 = N'15印刷・同関連業' THEN 27
	WHEN column_9 = N'16化学工業' THEN 28
	WHEN column_9 = N'17石油製品・石炭製品製造業' THEN 29
	WHEN column_9 = N'18プラスチック製品製造業（別掲を除く）' THEN 30
	WHEN column_9 = N'19ゴム製品製造業' THEN 31
	WHEN column_9 = N'20なめし革・同製品・毛皮製造業' THEN 32
	WHEN column_9 = N'21窯業・土石製品製造業' THEN 33
	WHEN column_9 = N'22鉄鋼業' THEN 34
	WHEN column_9 = N'23非鉄金属製造業' THEN 35
	WHEN column_9 = N'24金属製品製造業' THEN 36
	WHEN column_9 = N'25はん用機械器具製造業' THEN 37
	WHEN column_9 = N'26生産用機械器具製造業' THEN 38
	WHEN column_9 = N'27業務用機械器具製造業' THEN 39
	WHEN column_9 = N'28電子部品・デバイス・電子回路製造業' THEN 40
	WHEN column_9 = N'29電気機械器具製造業' THEN 41
	WHEN column_9 = N'30情報通信機械器具製造業' THEN 42
	WHEN column_9 = N'31輸送用機械器具製造業' THEN 43
	WHEN column_9 = N'32その他の製造業' THEN 44
	
	WHEN column_9 = N'F電気・ガス・熱供給・水道業' THEN 46
	WHEN column_9 = N'33電気業' THEN 47
	WHEN column_9 = N'34ガス業' THEN 48
	WHEN column_9 = N'35熱供給業' THEN 49
	WHEN column_9 = N'36水道業' THEN 50
	WHEN column_9 = N'G情報通信業' THEN 51
	WHEN column_9 = N'37通信業' THEN 52
	WHEN column_9 = N'38放送業' THEN 53
	WHEN column_9 = N'39情報サービス業' THEN 54
	WHEN column_9 = N'40インターネット附随サービス業' THEN 55
	WHEN column_9 = N'41映像・音声・文字情報制作業' THEN 56
	WHEN column_9 = N'G1情報通信業（通信業，放送業，映像・音声・文字情報制作業）' THEN 57
	WHEN column_9 = N'G2情報通信業（情報サービス業，インターネット附随サービス業）' THEN 58
	WHEN column_9 = N'H運輸業，郵便業' THEN 59
	WHEN column_9 = N'42鉄道業' THEN 60
	WHEN column_9 = N'43道路旅客運送業' THEN 61
	WHEN column_9 = N'44道路貨物運送業' THEN 62
	WHEN column_9 = N'45水運業' THEN 63
	WHEN column_9 = N'46航空運輸業' THEN 64
	WHEN column_9 = N'47倉庫業' THEN 65
	WHEN column_9 = N'48運輸に附帯するサービス業' THEN 66
	WHEN column_9 = N'49郵便業（信書便事業を含む）' THEN 67
	
	WHEN column_9 = N'I卸売業，小売業' THEN 69
	WHEN column_9 = N'I1卸売業' THEN 70
	WHEN column_9 = N'50各種商品卸売業' THEN 71
	WHEN column_9 = N'51繊維・衣服等卸売業' THEN 72
	WHEN column_9 = N'52飲食料品卸売業' THEN 73
	WHEN column_9 = N'53建築材料，鉱物・金属材料等卸売業' THEN 74
	WHEN column_9 = N'54機械器具卸売業' THEN 75
	WHEN column_9 = N'55その他の卸売業' THEN 76
	WHEN column_9 = N'I2小売業' THEN 77
	WHEN column_9 = N'56各種商品小売業' THEN 78
	WHEN column_9 = N'57織物・衣服・身の回り品小売業' THEN 79
	WHEN column_9 = N'58飲食料品小売業' THEN 80
	WHEN column_9 = N'59機械器具小売業' THEN 81
	WHEN column_9 = N'60その他の小売業' THEN 82
	WHEN column_9 = N'61無店舗小売業' THEN 83
	WHEN column_9 = N'J金融業，保険業' THEN 84
	WHEN column_9 = N'62銀行業' THEN 85
	WHEN column_9 = N'63協同組織金融業' THEN 86
	WHEN column_9 = N'64貸金業，クレジットカード業等非預金信用機関' THEN 87
	WHEN column_9 = N'65金融商品取引業，商品先物取引業' THEN 88
	WHEN column_9 = N'66補助的金融業等' THEN 89
	WHEN column_9 = N'67保険業（保険媒介代理業，保険サービス業を含む）' THEN 90
	
	WHEN column_9 = N'K不動産業，物品賃貸業' THEN 92
	WHEN column_9 = N'K1不動産業' THEN 93
	WHEN column_9 = N'68不動産取引業' THEN 94
	WHEN column_9 = N'69不動産賃貸業・管理業' THEN 95
	WHEN column_9 = N'K2物品賃貸業' THEN 96
	WHEN column_9 = N'70物品賃貸業' THEN 97
	WHEN column_9 = N'L学術研究，専門・技術サービス業' THEN 98
	WHEN column_9 = N'71学術・開発研究機関' THEN 99
	WHEN column_9 = N'72専門サービス業（他に分類されないもの）' THEN 100
	WHEN column_9 = N'73広告業' THEN 101
	WHEN column_9 = N'74技術サービス業（他に分類されないもの）' THEN 102
	
	WHEN column_9 = N'M宿泊業，飲食サービス業' THEN 104
	WHEN column_9 = N'75宿泊業' THEN 105
	WHEN column_9 = N'M1宿泊業' THEN 106
	WHEN column_9 = N'M2飲食店，持ち帰り・配達飲食サービス業' THEN 107
	WHEN column_9 = N'76飲食店' THEN 108
	WHEN column_9 = N'77持ち帰り・配達飲食サービス業' THEN 109
	WHEN column_9 = N'N生活関連サービス業，娯楽業' THEN 110
	WHEN column_9 = N'78洗濯・理容・美容・浴場業' THEN 111
	WHEN column_9 = N'79その他の生活関連サービス業' THEN 112
	WHEN column_9 = N'80娯楽業' THEN 113
	
	WHEN column_9 = N'O教育，学習支援業' THEN 115
	WHEN column_9 = N'O1教育，学習支援業（学校教育）' THEN 116
	WHEN column_9 = N'81学校教育' THEN 117
	WHEN column_9 = N'O2教育，学習支援業（その他の教育，学習支援業）' THEN 118
	WHEN column_9 = N'82その他の教育，学習支援業' THEN 119
	WHEN column_9 = N'P医療，福祉' THEN 120
	WHEN column_9 = N'83医療業' THEN 121
	WHEN column_9 = N'84保健衛生' THEN 122
	WHEN column_9 = N'85社会保険・社会福祉・介護事業' THEN 123
	
	WHEN column_9 = N'Q複合サービス事業' THEN 125
	WHEN column_9 = N'Q1複合サービス事業（郵便局）' THEN 126
	WHEN column_9 = N'86郵便局' THEN 127
	WHEN column_9 = N'Q2複合サービス事業（協同組合）' THEN 128
	WHEN column_9 = N'87協同組合（他に分類されないもの）' THEN 129
	WHEN column_9 = N'Rサービス業（他に分類されないもの）' THEN 130
	WHEN column_9 = N'R1サービス業（政治・経済・文化団体，宗教）' THEN 131
	WHEN column_9 = N'93政治・経済・文化団体' THEN 132
	WHEN column_9 = N'94宗教' THEN 133
	WHEN column_9 = N'R2サービス業（政治・経済・文化団体，宗教を除く）' THEN 134
	WHEN column_9 = N'88廃棄物処理業' THEN 135
	WHEN column_9 = N'89自動車整備業' THEN 136
	WHEN column_9 = N'90機械等修理業（別掲を除く）' THEN 137
	WHEN column_9 = N'91職業紹介・労働者派遣業' THEN 138
	WHEN column_9 = N'92その他の事業サービス業' THEN 139
	WHEN column_9 = N'95その他のサービス業' THEN 140
        ELSE NULL
    END
FROM economic_census_employments_landing_raw;

-- yearの'年'削除
UPDATE economic_census_employments_landing_raw
SET column_6 =
    LEFT(LTRIM(RTRIM(column_6)), 4)
FROM economic_census_employments_landing_raw;

-- landing_rawの内容をcuratedに挿入
WITH src AS (
    SELECT
        TRY_CAST(NULLIF(LTRIM(RTRIM(column_3)), '') AS INT) AS prefecture_code,
        TRY_CAST(NULLIF(LTRIM(RTRIM(column_6)), '') AS INT) AS year,
        TRY_CAST(NULLIF(LTRIM(RTRIM(column_9)), '') AS INT) AS industry_code,
        TRY_CAST(NULLIF(LTRIM(RTRIM(REPLACE(column_11, ',', ''))), '') AS INT) AS employments_total_t,
        TRY_CAST(NULLIF(LTRIM(RTRIM(REPLACE(column_12, ',', ''))), '') AS INT) AS employments_total_m,
        TRY_CAST(NULLIF(LTRIM(RTRIM(REPLACE(column_13, ',', ''))), '') AS INT) AS employments_total_f
    FROM economic_census_employments_landing_raw
    WHERE column_3 <= 47
        AND column_6 IS NOT NULL
        AND ((column_9 = 2) OR ((column_9 >= 51) AND (column_9 <= 58)))
)
MERGE economic_census_employments_curated AS tgt
USING src
    ON tgt.prefecture_code= src.prefecture_code
        AND tgt.year = src.year
        AND tgt.industry_code= src.industry_code

WHEN MATCHED THEN
    UPDATE SET
        tgt.employments_total_t= src.employments_total_t,
        tgt.employments_total_m= src.employments_total_m,
        tgt.employments_total_f= src.employments_total_f,
        tgt.updated_at = GETDATE()

WHEN NOT MATCHED THEN
    INSERT (
        prefecture_code,
        year,
        industry_code,
        employments_total_t,
        employments_total_m,
        employments_total_f,
        updated_at
    )
    VALUES (
        src.prefecture_code,
        src.year,
        src.industry_code,
        src.employments_total_t,
        src.employments_total_m,
        src.employments_total_f,
        GETDATE()
    );

-- 分割分の他rawデータ格納用にlanding_rawテーブルを空にする
TRUNCATE TABLE economic_census_employments_landing_raw