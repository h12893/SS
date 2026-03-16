
# Transformation Rules

## prefecture_code 抽出
- 全角数字 → 半角数字変換
- SUBSTRING(prefecture,1,2) を変換
- 特別扱い:
  - 全国 → 0
  - 外国 → 48
  - 不詳 → 49

## region_type 付与
- 0: 全国
- 1: 都道府県
- 2: 政令市、23区
- 3: 外国
- 4: 不詳

## prefecture 名称クレンジング
- 都道府県・政令市 → 先頭2桁コード削除
- 全国・外国・不詳 → コード削除しない
- 全角スペース・半角スペース・タブ削除

## MERGE ロジック
- prefecture_code + year をキーに更新/追加
- 数値項目は TRY_CAST
