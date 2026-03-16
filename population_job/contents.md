# このフォルダについて

政府統計データに関連したドキュメントやメタデータを格納。

# フォルダ構成

## \docs

ドキュメント形式で保存されるメタデータの格納先。

### \metadata

- dataset_metadata.md：使用したデータそのものの説明。

- column_metadata.md：各カラムの意味・型・制約などの説明。

- transformation_metadata.md：Raw → Landing → Curated の変換ルールの説明。

- region_type_definition.md：コード値と名称の対応表。

## \sql

SQLテーブル形式で保存されるデータの作成用のクエリの格納先。
SQLは格納ファイルを.sqlに、ファイル名は **動詞＋対象＋用途** 形式で、全て小文字とする。

### \population

#### PL_population_yyyyのクエリ

- create_population_curated.sql：population_curatedを作成（パイプラインの*CreateCuratedTableIfNotExists*の処理に対応）

- create_population_landing.sql：population_landingを作成（パイプラインの*CreateLandingTableIfNotExists*の処理に対応）

- truncate_population_landing.sql：population_landingの中身を削除（パイプラインの*TruncateLanding*の処理に対応）

- set_default_year.sql：population_landingのyearのDEFAULT制約を付け替え（パイプラインの*SetDefaultYear*の処理に対応）

- clean_prefecturecode_landing.sql：カラムの型変換（パイプラインの*UpdatePrefectureCodeAndCleanPrefecture*の処理に対応）

- merge_population_curated.sql：population_landingのpopulation_curatedへのマージ処理（パイプラインの*sp_population_merge*の処理に対応）

### \jobs

### \metadata_codes

#### PL_metadata_codesのクエリ

- create_codes_metadata.sql：metadata_codesを作成（パイプラインの*CreateMetadataCodes*の処理に対応）

- truncate_codes_metadata.sql：metadata_codesの中身を削除（パイプラインの*TruncateMetadataCodes*の処理に対応）

- insert_elseinfo_codes.sql：region_typeが「全国」「外国」「不詳」のコードをmetadata_codesに挿入（パイプラインの*InsertElseInfo*の処理に対応）

- insert_prefecture_codes.sql：region_typeが「都道府県」のコードをmetadata_codesに挿入（パイプラインの*InsertPrefecturerInfo*の処理に対応）

- insert_city_codes.sql：region_typeが「政令市、23区」のコードをmetadata_codesに挿入（パイプラインの*InsertCityInfo*の処理に対応）

## \ADF

ADFをGit連携させる場合のRootフォルダ。

### \dataset

ADFのデータセット定義（Dataset JSON）を保存する場所。

例）encode_raw_population_yyyy.jsonなど

- 含まれる情報

    - データのスキーマ（列名・型）

    - ファイルパス（Blob Storageのパスなど）

    - 接続先（linkedServiceの参照）

    - フォーマット（CSV / JSON / Parquet）

- 更新されるタイミング

    - 新しいデータセットを作成したとき

    - Raw / Landing / Curated の構造を変更したとき

### \factory

ADF全体のファクトリ設定（Factory JSON）を保存する場所。

例）read-government-statistical.jsonなど

- 含まれる情報

    - ADFの名前

    - リージョン

    - Git連携設定

    - Data Factory全体のメタ情報

- 更新されるタイミング

    - ADFの設定を変更したとき

    - Git連携設定を変更したとき

### \linkedService

ADFの接続情報（Linked Service JSON）を保存する場所。

例）Connect_dbmake2026datalake.jsonなど

- 含まれる情報

    - SQL Databaseの接続設定

    - Blob Storageの接続設定

    - Key Vaultの参照

    - 認証方式（Managed Identityなど）

- 更新されるタイミング

    - 新しい接続先を追加したとき

    - 接続設定を変更したとき

### \pipeline

ADFのパイプライン定義（Pipeline JSON）を保存する場所。

例）PL_population_yyyy.jsonなど

- 含まれる情報

    - Script Activity（SQL実行）

    - Copy Activity（Raw → Landing）

    - ForEach Activity

    - パイプラインパラメータ

    - アクティビティ間の依存関係

- 更新されるタイミング

    - ADF Studioでパイプラインを編集して保存したとき

    - Gitモードで新規パイプラインを作成したとき

### publish_config.json

Git → ADF（実行環境）へPublishする際の設定ファイル。

- 含まれる情報

    - Publish先のブランチ（通常adf_publish）

    - ADF JSONのルートフォルダ

    - Publish時の動作設定

- 更新されるタイミング

    - Git連携を設定したとき

    - Publishブランチを変更したとき

## \pipelines

ADFのARMエクスポートファイルの格納先。

- adf_export.json：ARMエクスポートで得られる、ADFの構成（パイプライン・データセット・リンクサービスなど）をすべて含むファイル（2026/03/01時点のスナップショットとして保存）
