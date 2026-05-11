Cognitive Search のインデックス設計とは何か（目的）
一言でいうと：
「検索エンジンがデータを理解しやすいように、データの“見出し”や“項目”を定義する作業」です。

もっと噛み砕くと：

Cognitive Search は「検索エンジン」

JSON や文章を「検索しやすい形」に変換する必要がある

そのために「どの項目を検索対象にするか」「どの項目をフィルタに使うか」を決める

これが インデックス設計 です。

🧠 例え話：図書館の本の整理と同じ
図書館で本を探すとき、以下の情報があると便利ですよね：

タイトル

著者

ジャンル

出版年

キーワード

これがないと、本を探せません。

Cognitive Search も同じで、
「どのフィールドを検索対象にするか」  
「どのフィールドをフィルタに使うか」  
を決める必要があります。

🧩 インデックス設計で決めること（具体的）
Cognitive Search のインデックスでは、各フィールドに対して以下を設定します：

設定項目	意味
type	データ型（string, number, array など）
searchable	文章検索の対象にするか
filterable	絞り込み検索に使うか
sortable	並び替えに使うか
facetable	集計（カテゴリ分け）に使うか
retrievable	検索結果に含めるか
vector	ベクトル検索に使うか（RAG の要）


📘 あなたのデータでのインデックス設計（例）
① 資格試験データのインデックス例
フィールド名	用途	searchable	filterable	vector
name	試験名	✔	✔	✔
description	試験内容	✔	✖	✔
category	分類（AI/統計/クラウド）	✔	✔	✔
exam_schedule.exam_date	開催日	✖	✔	✖
exam_schedule.application_deadline	申込期限	✖	✔	✖
difficulty	難易度	✔	✔	✔
related_skills	関連スキル	✔	✔	✔


→ LLM が「ユーザのスキル」→「関連資格」を検索しやすくなる。

② スキルチェックリストのインデックス例
フィールド名	用途	searchable	filterable	vector
skill-sets	シート名（基盤/融合など）	✔	✔	✔
大分類	スキル分類	✔	✔	✔
中分類	スキル分類	✔	✔	✔
小分類	スキル分類	✔	✔	✔
スキル項目	スキル名	✔	✔	✔
スキルの説明	詳細説明	✔	✖	✔
レベル1〜3	レベル定義	✔	✖	✔
関連タスク	タスク	✔	✔	✔
必要知識	知識	✔	✔	✔
関連ツール	ツール	✔	✔	✔


→ LLM が「ユーザの業務経験」→「該当スキル」を検索しやすくなる。

🔍 インデックス設計が必要な理由（RAG の観点）
RAG の流れは以下の通り：

ユーザ入力

Cognitive Search で関連情報を検索

LLM に渡す

回答生成

この中で 検索精度を決めるのがインデックス設計 です。

もしインデックス設計が甘いと：

「統計検定」と検索してもヒットしない

「データ前処理の経験があります」→該当スキルが見つからない

「申込期限が近い資格」→フィルタできない

など、RAG が機能しなくなります。

🧭 Cognitive Search インデックス設計でやること（まとめ）
どのフィールドを検索対象にするか決める（searchable）

どのフィールドで絞り込みできるようにするか決める（filterable）

どのフィールドをベクトル検索に使うか決める（vector）

JSON の構造をそのままインデックスに反映する

資格データとスキルデータで別インデックスを作る







Cognitive Search インデックス作成の全体像（初心者向け）
インデックス作成は、ざっくり言うと次の 3 ステップです：

インデックスの箱を作る（フィールド定義）

データを入れる（資格 JSON をアップロード or 取り込み）

検索できるように設定する（searchable / filterable / vector など）

これを順番にやれば、RAG の検索基盤が完成します。

🧭 手順：Cognitive Search のインデックスを作成する
以下は、Azure Portal を使った初心者向けの手順です。

01
Cognitive Search リソースを開く
最初の準備
まずは Azure Portal で Cognitive Search の管理画面に入ります。

Azure Portal にログイン

左メニューから 「すべてのリソース」 を開く

作成済みの Cognitive Search リソース を選択する

02
インデックス作成画面を開く
重要
検索エンジンの“箱”となるインデックスを作成します。

Cognitive Search のメニューから 「Index」 を選択

上部の 「+ Add Index」 をクリック

03
インデックス名を決める
資格データ用のインデックス名を設定します。

例：certifications-index

後から変更できないので、わかりやすい名前にする

04
フィールド（項目）を追加する
最重要
資格データの JSON に合わせてフィールドを定義します。

No（string, key=true）

資格名（searchable=true, filterable=true）

内容・範囲（searchable=true）

知識・スキル（searchable=true, filterable=true）

対象（searchable=true, filterable=true）

受験資格（searchable=true, filterable=true）

開催日（Edm.DateTimeOffset, filterable=true, sortable=true）

報奨金額（Edm.Int32, filterable=true, sortable=true）

合格率（Edm.Double, filterable=true）

公式サイトURL（retrievable=true）

データ更新日（filterable=true, sortable=true）

05
searchable / filterable / sortable を設定
検索の精度と絞り込み機能を決める重要な設定です。

searchable：文章検索したい項目（資格名、内容、知識・スキルなど）

filterable：絞り込みに使う項目（開催日、対象、報奨金額など）

sortable：並び替えに使う項目（開催日、報奨金額など）

06
ベクトル検索（vector field）を設定
RAG の意味検索を有効にするための設定です。

フィールド例：vectorContent

データ型：Collection(Edm.Single)

次元数：使用する埋め込みモデルに合わせる（例：1536）

vectorSearch を有効化し、HNSW などのアルゴリズムを選択

07
データソースを登録する
資格 JSON を Cognitive Search に取り込む準備です。

メニューから 「Data sources」 を選択

「+ Add data source」 をクリック

種類：Azure Blob Storage または Cosmos DB

資格 JSON を格納したストレージを指定

08
インデクサーを作成してデータを取り込む
データソースからインデックスにデータを流し込みます。

メニューから 「Indexers」 を選択

「+ Add Indexer」 をクリック

データソースとインデックスを紐づける

Run を押して取り込み開始

09
検索テストで動作確認
インデックスが正しく動いているか確認します。

Cognitive Search のメニューから 「Search explorer」 を開く

例：search=G検定

例：$filter=対象 eq '若手エンジニア'

例：ベクトル検索のテストも可能

10
アプリケーションから利用開始
インデックスが完成したら、アプリ側から検索 API を呼び出します。

REST API または SDK（Python / C#）を使用

RAG の Retrieval 部分で Cognitive Search を呼び出す

LLM に検索結果を渡して回答生成

🧩 この手順で何ができるようになるか
資格データを 意味検索（ベクトル検索） できる

「開催日が近い資格」「若手向け資格」などの 絞り込み検索 ができる

RAG の Retrieval 部分が完成し、LLM が正確に資格を推薦できる