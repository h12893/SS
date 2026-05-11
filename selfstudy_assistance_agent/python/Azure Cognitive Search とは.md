Azure Cognitive Search とは
クラウドベースの検索サービス  
テキスト、PDF、画像、音声など多様なデータをインデックス化し、高速検索を提供する。

AI を活用した高度検索  
セマンティック検索、ベクトル検索、ハイブリッド検索など、従来のキーワード検索を超えた検索精度を実現。

RAG（Retrieval-Augmented Generation）の検索基盤として最適  
Azure OpenAI と組み合わせて社内ナレッジ検索やチャットボットを構築できる。

🧩 何ができるのか（主要機能）
1. 全文検索（Full-text Search）
Lucene ベースのキーワード検索。日本語形態素解析にも対応。

2. ベクトル検索（Vector Search）
Embedding による意味検索。類義語・言い換えに強い。

3. ハイブリッド検索（Hybrid Search）
全文検索＋ベクトル検索を統合し、RAG で最も高精度。

4. セマンティックランキング
検索結果を意味的に再ランキングし、関連度の高い順に並べる。Standard 以上で利用可能。

5. AI エンリッチメント（Cognitive Skills）
OCR

PDF 解析

テキスト抽出

エンティティ抽出

自動チャンキング

自動ベクトル化
などをパイプラインで実行。

6. インデクサー（Indexer）
Blob Storage、Cosmos DB、SQL DB などから自動でデータ収集・更新。

7. ナレッジストア（Knowledge Store）
エンリッチメント結果を Azure Storage に保存し、分析や BI に活用可能。

🛠 どう使うのか（利用フロー）
Search Service を作成（Azure Portal）

インデックスを設計（フィールド定義、型、検索可否など）

データソースを接続（Blob、Cosmos DB など）

インデクサーで取り込み

検索 API / SDK でクエリ実行（Python, C#, REST）

主な設定項目（インデックス設計の要点）
1. Fields（フィールド定義）
各フィールドに以下の属性を設定：

type（Edm.String, Edm.Int32, Edm.GeographyPoint など）

searchable（全文検索対象にするか）

filterable（フィルタ条件に使えるか）

sortable（並び替え可能か）

facetable（集計に使えるか）

key（主キー）

2. Scoring Profiles（スコア調整）
freshness（新しいほどスコア↑）

magnitude（数値の大小でスコア調整）

distance（距離ベース）

tag（タグ一致でスコア↑）

3. Semantic Settings（セマンティック検索）
semantic configuration

prioritized fields（タイトル・本文など）

4. Vector Settings（ベクトル検索）
vector field（次元数、型）

vector index（HNSW など）

5. Indexer Settings
データソース

スケジュール（毎時・毎日など）

📌 まとめ
Azure Cognitive Search は、Azure 上で RAG や社内検索を構築するための “検索エンジン＋AI パイプライン” を提供するサービス。  
全文検索・ベクトル検索・AI エンリッチメントを組み合わせて、高精度な検索体験を実現できます。










Azure Cognitive Search リソース作成（初心者向けステップガイド）
Azure Cognitive Search の作成は、次の 7 ステップで完了します。

以下に 手順書形式でまとめます。

01
Azure Portal にサインインする
すべての操作は Azure Portal から行います。

ブラウザで https://portal.azure.com を開く

Azure アカウントでログインする

02
Cognitive Search リソース作成画面を開く
検索サービスの作成を開始します。

Azure Portal → 左上「リソースの作成」 → 検索バーに「Cognitive Search」

「Cognitive Search」を選択

「作成」をクリック

03
基本設定を入力する
重要
リソースの基本情報を設定します。

サブスクリプション：利用するものを選択

リソースグループ：新規作成または既存を選択

サービス名：例）career-search-service

リージョン：日本なら「Japan East」推奨

SKU（価格レベル）：Standard 以上を選択（ベクトル検索に必須）

04
ネットワーク設定を確認する
基本的にはデフォルトのままで問題ありません。

初心者は「パブリックアクセスを許可」で OK

社内ネットワーク制限が必要な場合は後で設定可能

05
暗号化・タグ設定（任意）
必要に応じて設定します。

暗号化はデフォルトで OK

タグは管理上必要なら追加

06
確認して作成
設定内容を確認し、リソースを作成します。

「確認および作成」をクリック

問題なければ「作成」をクリック

数十秒でデプロイ完了

07
作成された Cognitive Search を開く
ここからインデックス作成やデータ取り込みを行います。

「リソースに移動」をクリック

Cognitive Search の管理画面が開く

ここで インデックス作成 や データソース設定 を行う