-- 空白をNULLに統一
UPDATE active_job_openings_landing_raw
SET prefecture = NULL
WHERE prefecture = '';

-- prefecture を直近の値で埋める（SQL Server 版）
WITH filled AS (
    SELECT r1.row_num,
           r1.prefecture,
           (
               SELECT TOP 1 r2.prefecture
               FROM active_job_openings_landing_raw r2
               WHERE r2.row_num <= r1.row_num
                 AND r2.prefecture IS NOT NULL
               ORDER BY r2.row_num DESC
           ) AS prefecture_filled
    FROM active_job_openings_landing_raw r1
)
UPDATE active_job_openings_landing_raw
SET prefecture = filled.prefecture_filled
FROM filled
WHERE active_job_openings_landing_raw.row_num = filled.row_num;

-- prefectreu_codeへの変換
UPDATE active_job_openings_landing_raw
SET prefecture =
    CASE
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'全%' COLLATE Japanese_CI_AS THEN 0
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'北海道%' COLLATE Japanese_CI_AS THEN 1
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'青森%' COLLATE Japanese_CI_AS THEN 2
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'岩手%' COLLATE Japanese_CI_AS THEN 3
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'宮城%' COLLATE Japanese_CI_AS THEN 4
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'秋田%' COLLATE Japanese_CI_AS THEN 5
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'山形%' COLLATE Japanese_CI_AS THEN 6
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'福島%' COLLATE Japanese_CI_AS THEN 7
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'茨城%' COLLATE Japanese_CI_AS THEN 8
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'栃木%' COLLATE Japanese_CI_AS THEN 9
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'群馬%' COLLATE Japanese_CI_AS THEN 10
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'埼玉%' COLLATE Japanese_CI_AS THEN 11
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'千葉%' COLLATE Japanese_CI_AS THEN 12
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'東京%' COLLATE Japanese_CI_AS THEN 13
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'神奈川%' COLLATE Japanese_CI_AS THEN 14
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'新潟%' COLLATE Japanese_CI_AS THEN 15
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'富山%' COLLATE Japanese_CI_AS THEN 16
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'石川%' COLLATE Japanese_CI_AS THEN 17
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'福井%' COLLATE Japanese_CI_AS THEN 18
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'山梨%' COLLATE Japanese_CI_AS THEN 19
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'長野%' COLLATE Japanese_CI_AS THEN 20
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'岐阜%' COLLATE Japanese_CI_AS THEN 21
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'静岡%' COLLATE Japanese_CI_AS THEN 22
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'愛知%' COLLATE Japanese_CI_AS THEN 23
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'三重%' COLLATE Japanese_CI_AS THEN 24
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'滋賀%' COLLATE Japanese_CI_AS THEN 25
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'京都%' COLLATE Japanese_CI_AS THEN 26
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'大阪%' COLLATE Japanese_CI_AS THEN 27
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'兵庫%' COLLATE Japanese_CI_AS THEN 28
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'奈良%' COLLATE Japanese_CI_AS THEN 29
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'和歌山%' COLLATE Japanese_CI_AS THEN 30
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'鳥取%' COLLATE Japanese_CI_AS THEN 31
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'島根%' COLLATE Japanese_CI_AS THEN 32
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'岡山%' COLLATE Japanese_CI_AS THEN 33
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'広島%' COLLATE Japanese_CI_AS THEN 34
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'山口%' COLLATE Japanese_CI_AS THEN 35
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'徳島%' COLLATE Japanese_CI_AS THEN 36
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'香川%' COLLATE Japanese_CI_AS THEN 37
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'愛媛%' COLLATE Japanese_CI_AS THEN 38
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'高知%' COLLATE Japanese_CI_AS THEN 39
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'福岡%' COLLATE Japanese_CI_AS THEN 40
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'佐賀%' COLLATE Japanese_CI_AS THEN 41
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'長崎%' COLLATE Japanese_CI_AS THEN 42
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'熊本%' COLLATE Japanese_CI_AS THEN 43
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'大分%' COLLATE Japanese_CI_AS THEN 44
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'宮崎%' COLLATE Japanese_CI_AS THEN 45
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'鹿児島%' COLLATE Japanese_CI_AS THEN 46
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'沖縄%' COLLATE Japanese_CI_AS THEN 47
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'外%' COLLATE Japanese_CI_AS THEN 48
        WHEN prefecture COLLATE Japanese_CI_AS LIKE N'不%' COLLATE Japanese_CI_AS THEN 49
        ELSE 49
    END
FROM active_job_openings_landing_raw;

-- job_codeへの変換
UPDATE active_job_openings_landing_raw
SET job =
    CASE
        WHEN job LIKE N'職業%' THEN 1
        WHEN job LIKE N'Ａ%' THEN 2

        WHEN job LIKE N'% 01%' THEN 3
        WHEN job LIKE N'% 02%' THEN 4
        WHEN job LIKE N'% 03%' THEN 5
        WHEN job LIKE N'% 04%' THEN 6

        WHEN job LIKE N'Ｂ%' THEN 7

        WHEN job LIKE N'% 05%' THEN 8
        WHEN job LIKE N'% 06%' THEN 9
        WHEN job LIKE N'% 07%' THEN 10
        WHEN job LIKE N'% 08%' THEN 11
        WHEN job LIKE N'% 09%' THEN 12
        WHEN job LIKE N'% 10%' THEN 13
        WHEN job LIKE N'% 11%' THEN 14
        WHEN job LIKE N'% 12%' THEN 15
        WHEN job LIKE N'% 13%' THEN 16
        WHEN job LIKE N'% 14%' THEN 17
        WHEN job LIKE N'% 15%' THEN 18
        WHEN job LIKE N'% 16%' THEN 19
        WHEN job LIKE N'% 17%' THEN 20
        WHEN job LIKE N'% 18%' THEN 21
        WHEN job LIKE N'% 19%' THEN 22
        WHEN job LIKE N'% 20%' THEN 23
        WHEN job LIKE N'% 21%' THEN 24
        WHEN job LIKE N'% 22%' THEN 25
        WHEN job LIKE N'% 23%' THEN 26
        WHEN job LIKE N'% 24%' THEN 27

        WHEN job LIKE N'Ｃ%' THEN 28

        WHEN job LIKE N'% 25%' THEN 29
        WHEN job LIKE N'% 26%' THEN 30
        WHEN job LIKE N'% 27%' THEN 31
        WHEN job LIKE N'% 28%' THEN 32
        WHEN job LIKE N'% 29%' THEN 33
        WHEN job LIKE N'% 30%' THEN 34
        WHEN job LIKE N'% 31%' THEN 35

        WHEN job LIKE N'Ｄ%' THEN 36

        WHEN job LIKE N'% 32%' THEN 37
        WHEN job LIKE N'% 33%' THEN 38
        WHEN job LIKE N'% 34%' THEN 39

        WHEN job LIKE N'Ｅ%' THEN 40

        WHEN job LIKE N'% 35%' THEN 41
        WHEN job LIKE N'% 36%' THEN 42
        WHEN job LIKE N'% 37%' THEN 43
        WHEN job LIKE N'% 38%' THEN 44
        WHEN job LIKE N'% 39%' THEN 45
        WHEN job LIKE N'% 40%' THEN 46
        WHEN job LIKE N'% 41%' THEN 47
        WHEN job LIKE N'% 42%' THEN 48

        WHEN job LIKE N'Ｆ%' THEN 49

        WHEN job LIKE N'% 43%' THEN 50
        WHEN job LIKE N'% 44%' THEN 51
        WHEN job LIKE N'% 45%' THEN 52

        WHEN job LIKE N'Ｇ%' THEN 53

        WHEN job LIKE N'% 46%' THEN 54
        WHEN job LIKE N'% 47%' THEN 55
        WHEN job LIKE N'% 48%' THEN 56

        WHEN job LIKE N'Ｈ%' THEN 57

        WHEN job LIKE N'% 49%' THEN 58
        WHEN job LIKE N'% 50%' THEN 59
        WHEN job LIKE N'% 51%' THEN 60
        WHEN job LIKE N'% 52%' THEN 61
        WHEN job LIKE N'% 53%' THEN 62
        WHEN job LIKE N'% 54%' THEN 63
        WHEN job LIKE N'% 55%' THEN 64
        WHEN job LIKE N'% 56%' THEN 65
        WHEN job LIKE N'% 57%' THEN 66
        WHEN job LIKE N'% 58%' THEN 67
        WHEN job LIKE N'% 59%' THEN 68

        WHEN job LIKE N'Ｉ%' THEN 69

        WHEN job LIKE N'% 60%' THEN 70
        WHEN job LIKE N'% 61%' THEN 71
        WHEN job LIKE N'% 62%' THEN 72
        WHEN job LIKE N'% 63%' THEN 73
        WHEN job LIKE N'% 64%' THEN 74

        WHEN job LIKE N'Ｊ%' THEN 75

        WHEN job LIKE N'% 65%' THEN 76
        WHEN job LIKE N'% 66%' THEN 77
        WHEN job LIKE N'% 67%' THEN 78
        WHEN job LIKE N'% 68%' THEN 79
        WHEN job LIKE N'% 69%' THEN 80

        WHEN job LIKE N'Ｋ%' THEN 81

        WHEN job LIKE N'% 70%' THEN 82
        WHEN job LIKE N'% 71%' THEN 83
        WHEN job LIKE N'% 72%' THEN 84
        WHEN job LIKE N'% 73%' THEN 85

        WHEN job LIKE N'分類不能%' THEN 86

        ELSE NULL
    END
FROM active_job_openings_landing_raw;
