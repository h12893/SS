# 事前準備

## ディレクトリ構成

以下のようなディレクトリ構成を前提としている。
構成が異なる場合は、各所のパス部分を対応させる。

```
project-root/
│
├── app/                         # FastAPI アプリケーション本体
│   ├── main.py                  # FastAPI エントリポイント
│   ├── api/                     # API ルーター
│   │   ├── __init__.py
│   │   ├── rag.py               # RAG API（検索→LLM→回答）
│   │   ├── health.py            # ヘルスチェック
│   │   └── profile.py           # ユーザプロファイルAPI（任意）
│   │
│   ├── core/                    # 基盤ロジック
│   │   ├── config.py            # 設定（環境変数）
│   │   ├── embeddings.py        # 埋め込み生成
│   │   ├── llm.py               # ローカルLLM呼び出し
│   │   └── search.py            # Chroma検索
│   │
│   ├── models/                  # Pydanticモデル
│   │   ├── request.py
│   │   └── response.py
│   │
│   ├── services/                # ビジネスロジック
│   │   ├── skill_inventory.py   # スキル棚卸しロジック
│   │   └── certification.py     # 資格推薦ロジック
│   │
│   └── utils/                   # 共通ユーティリティ
│       ├── logger.py
│       └── file_loader.py
│
├── data/                        # JSON データ（資格・スキル）
│   ├── certifications.json
│   ├── skills.json
│   └── sample_user_profiles.json
│
├── vectorstore/                 # Chroma の永続化データ（ローカル）
│   └── chroma.sqlite3
│
├── models/                      # ローカルLLMのモデル格納
│   └── phi-3-mini.gguf
│
├── docker/                      # Docker 関連ファイル
│   ├── Dockerfile               # ACA にデプロイする Dockerfile
│   ├── docker-compose.yml       # ローカル開発用
│   └── entrypoint.sh            # 起動スクリプト
│
├── scripts/                     # 開発用スクリプト
│   ├── build.sh                 # Docker build
│   ├── push.sh                  # ACR push
│   └── deploy.sh                # ACA デプロイ
│
├── tests/                       # テストコード
│   ├── test_rag.py
│   └── test_api.py
│
├── requirements.txt             # Python 依存パッケージ
├── README.md                    # プロジェクト説明
└── .env                         # 環境変数（ローカル用）
```

## ライブラリインストール

以下のライブラリをインストールする。
- fastapi
- uvicorn
- chromadb
- sentence-transformers
- transformers
- accelerate
- llama-cpp-python  
※ Windowsの場合パス長制限でインストール時にエラーが発生する可能性あり。その場合は以下のいずれかで対応する。  
  - Windows の「長いパスを許可」を有効化する（以下2通りのいずれか）
    - レジストリを変更する
      1. Windows キー →「regedit」でレジストリエディタを開く
      2. `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`に移動
      3. LongPathsEnabled を0 → 1に変更
      4. PCを再起動
      5. 再度インストール
    - グループポリシーで設定する
      1. Windows キー →「gpedit.msc」
      2. `ローカルコンピュータポリシー → コンピュータの構成 → 管理用テンプレート → システム → ファイルシステム`に移動
      3. 「Win32 長いパスを有効にする」を「有効」にする
      4. PCを再起動
      5. 再度インストール
  - pip のビルドを避けて「事前ビルド版」を入れる  
  Windows では wheel が提供されているので、ビルドなしでインストールできるバージョンを指定すると成功しやすい。  
  `pip install llama-cpp-python==0.2.20`
  - --no-cache-dir を付けてインストール  
  `pip install --no-cache-dir llama-cpp-python`
  - WSL2（Ubuntu）でインストールする  
  UbuntuでPythonを使うと、Windows のパス問題を完全に回避できllama-cpp-pythonはほぼ確実に成功する。  
  `wsl --install`

## モデルダウンロード

以下の公式ミラー（LM Studio Community）URLより、Llama‑3‑8B‑Instruct（GGUF）をダウンロードする。  
URL：https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF

上記ページよりダウンロードするモデルを選択。  
ここでは`Meta-Llama-3-8B-Instruct-Q4_K_M.gguf`を選択。  
理由は以下の通りだが、各環境に応じてモデルを選択する。
- Q4_K_M は llama‑cpp で最も安定
- 8B はローカルでも動くギリギリのサイズ
- RAG との相性が良い
- ACA にも載せやすい

ダウンロードしたGGUFは以下に配置。  
`project-root/models/llama-3-8b-instruct-q4_k_m.gguf`  
ファイル名や格納場所を変えた場合は、main.pyのモデルパスを対応するように修正。
```
llm = Llama(
    model_path="{モデルのパス}",
    n_ctx=4096,
    n_threads=4
)
```

## uvicornを起動

プロジェクトのルートディレクトリに移動して、ターミナル上で以下のコマンドを実行することでuvicornが起動。  
`uvicorn app.main:app --reload`

上記実行後にターミナルのログ上で
```
INFO:     Application startup complete.
```
と表示されれば、FastAPIが正常に起動し、リクエスト待ち状態に入っている。  
この状態になれば、ブラウザやAPIクライアントでアクセスして実行が可能。

# 実行方法

## FastAPI起動後のブラウザでの動作確認

### 1. FastAPIのドキュメント画面にアクセスする
サーバが正常に起動しているかを確認する。  
ブラウザで http://localhost:8000/docs を開く。  
Swagger UIが表示されればFastAPIは正常動作しており、その場合は/healthと/ragのエンドポイントが見える。

### 2. ヘルスチェックAPIを実行する
アプリ全体が正常に起動しているかを確認する。  
`Swagger UI → GET /health → Try it out → Execute`を実行して、レスポンスが`{ "status": "ok" }`なら成功。  
ここでエラーが出る場合はアプリ起動に問題がある。

### 3. RAG APIをテストする
Chroma と LLM が正しく動作しているかを確認する。
`Swagger UI → POST /rag → Try it out → Execute`を実行してい`query`にテスト用の質問を入力。  
```
例："データ分析の経験があります。おすすめの資格は？"
```  
一定時間後にLLMの回答が返ってくることを確認（環境などによって回答までの時間は変動する）。

### 4. Chromaのデータ投入が成功しているか確認する
RAG の回答にスキルや資格データが含まれているかを確認する。  
`/rag`の回答にJSONの内容が反映されているか確認。  
```
例：資格名・スキル名・カテゴリなどが回答に含まれる
```

### 5. LLMが動作しているか確認する
モデルロードが成功していれば、RAGなしでも回答が生成される。  
`/rag`に適当な質問を送り、何らかの文章が返ってくればLLMは正常に動作している。
```
例："Python の学習方法を教えて"
```

### Validation Error (422)に関して
上記手順で正常に動作していそうな場合でも、Swagger UIの画面下部に “Validation Error (422)” が表示されることがある。

この、`Swagger UI の 422 Validation Error`は**仕様上必ず表示されるテンプレート例**であり、これだけではエラーかどうかは判断不可。

Swagger UI の画面で
- 上部 → 実際のレスポンス（200 OK）
- 下部 → FastAPI が自動生成した「エラー時のレスポンス例（422）」

が並んで表示されている場合、Swagger UIが成功例（200）と失敗例（422）を両方表示する仕様通りの結果となっている。

## 回答内容確認

### 「文脈に沿っている」「RAG が効いている」ことの判断
回答結果の中に
- 「単一データソースの BI レポート」
- ★や★★のスキルレベル表現

などの、skills.jsonに入れているような「スキルチェックシート由来の文言」や、「データサイエンス協会のスキル構造」に近い表現が含まれているかを確認する。  
LLM 単体だと、ピンポイントに「単一データソースのBIレポート構築手順」や「★付きスキル一覧」を自然に出してくる確率は低く、
- Chroma に入れたスキル・資格データ
- それをcontextとしてプロンプトに渡しているRAGの流れ

が効いているからこそ、上記要素を含む回答が作成されていると判断できる。

### この段階で回答精度を調べるためのFastAPIの使い方
ここからは「RAG の精度をちゃんと見る」ために、FastAPIをどう使っていくかを整理します。

#### 1. 基本：Swagger UI でいろんな質問を投げてみる
- ブラウザで http://localhost:8000/docs を開く
- POST /rag を開く
- Try it out を押す
- query に、実際に想定している質問を入れて試す  
  例：
  - 「データエンジニア志望ですが、どのスキルから優先的に学ぶべきですか？」
  - 「DS と DE の違いと、それぞれに必要なスキルを教えてください」
  - 「ログデータを使った分析案件で役立つ資格は？」
- Execute を押して、返ってきた answer を読む  
  ここで見るべきは：
  - ちゃんとスキルや資格の具体名が出ているか
  - あなたの JSON に入れた内容と整合しているか
  - 変な幻覚（存在しない資格名など）が出ていないか

#### 2. curlやVS Codeからも試す
実際のクライアントからも叩いて「APIの動作」を確認。

curl の例：  
bash
```
curl -X POST http://localhost:8000/rag \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"データサイエンティストとしてキャリアを伸ばすために、どのスキルを優先すべき？\"}"
```

VS CodeのREST Client拡張を使う例（test.http など）：  
http
```
POST http://localhost:8000/rag
Content-Type: application/json
{
  "query": "データエンジニアとして転職したいです。どのスキルと資格が重要ですか？"
}
```

#### 3. プロンプト（system 的な部分）を調整して精度を見る
現状のrag_answerの中のプロンプト（要約）：  
python
```
prompt = f"""
あなたはデータサイエンス分野のキャリア支援エージェントです。
以下の情報を参考に、ユーザの質問に答えてください。

# コンテキスト
{context}

# ユーザ質問
{query}

# 回答
"""
```

ここを少しずつ変えながら、回答の変化を見る。  
- 資格推薦に寄せたい場合の例：  
```
text
あなたはデータサイエンス・データエンジニアリング分野の
「資格・スキル推薦アドバイザー」です。

以下のコンテキストには、資格情報とスキル情報が含まれています。
ユーザの質問に対して、

1. 現状のスキル状況の整理
2. おすすめの資格（理由付き）
3. 次に身につけるべきスキル

を日本語で、箇条書きでわかりやすく回答してください。
```

- スキル棚卸しに寄せたい場合の例：
```
text
ユーザの経験・スキルを棚卸しし、
どの大分類（base/value/DS/DE/fusion）に強みがあるかを整理し、
不足している部分を具体的に指摘してください。
```
→ このような変更をして、同じqueryを投げて「どのプロンプトが一番しっくりくるか」を見ていくことで精度検証とする。


#### 4. コンテキストが本当に効いているかを確認する簡単なテスト
RAG が効いているかを確かめるために、使用したデータにしかない固有名詞を使う。  
例えば：  
- skills.json にだけ出てくる用語
- certifications.json にだけ出てくる資格名
- 「★」や「レベル3」など、独特の表現

こういうものを含んだ質問を投げてみて、
- その用語がちゃんと回答に出てくるか
- 逆に、コンテキストにないものを聞いたときに「知らない」とは言わないまでも、変な嘘をついていないか

を見ていくことで、「RAG としての効き具合」が確認できる。
