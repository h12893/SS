# プロトタイプ

## 全体構成（RAG アプリの流れ）
RAG の処理は大きく5つのステップで構成。  
① データ読み込み（JSON）  
② ベクトル化（Embedding）  
③ ベクトルDB（Chroma）に保存  
④ ユーザ質問をベクトル化して検索  
⑤ LLM に「検索結果＋質問」を渡して回答生成  
FastAPI はこの一連の流れをAPIとして公開する役割。  

## main.pyの構造と役割（全体像）
1. ライブラリの import
2. FastAPI アプリの初期化
3. LLM（llama-cpp）のロード
4. Embedding モデルのロード
5. ChromaDB の初期化
6. JSON データを Chroma にロードする関数
7. RAG の回答生成関数（rag_answer）
8. API エンドポイント（/health, /rag）

### 1. ライブラリimport（準備）
```
from fastapi import FastAPI
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
```
ここは単純に必要なライブラリを読み込んでいるだけ。  
RAGの3つの柱（LLM・Embedding・VectorDB）もここでインポート。

### 2. FastAPIアプリの初期化
```
app = FastAPI()
```
APIサーバの本体で、
```
/health
/rag
```
などのエンドポイントを提供する役割。

### 3. LLM（llama-cpp）のロード
```
llm = Llama(
    model_path="./models/llama-3-8b-instruct-q4_k_m.gguf",
    n_ctx=4096,
    n_threads=4
)
```
生成AI（回答生成）部分。
- model_path → GGUF モデルの場所
- n_ctx → LLM が扱える最大トークン数（長文対応の要）
- n_threads → CPU の並列処理数（速度に影響）

RAGの最終ステップ（⑤回答生成）を担当。

### 4. Embeddingモデルのロード
```
embedder = SentenceTransformer("all-MiniLM-L6-v2")
```
テキストをベクトルに変換するモデル。
- JSON のスキル・資格データをベクトル化
- ユーザ質問もベクトル化
- ChromaDB の検索に使う

RAGの②ベクトル化と④検索の両方に使われる。

### 5. ChromaDBの初期化
```
chroma_client = PersistentClient(path="./vectorstore")
collection = chroma_client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)
```
ベクトルデータベース（VectorDB）。
- ベクトル化したスキル・資格データを保存
- ユーザ質問に近いデータを検索

RAGの③保存と④検索を担当。

パラメータの意味
- name：コレクションの識別名。ChromaDB の中で「どのデータセットか」を識別するための名前
- metadata：コレクション全体に適用される設定。特に重要なのはベクトル検索の距離関数（similarity metric）の指定  
`metadata={"hnsw:space": "cosine"}`なら以下のような設定
    - HNSW（高速な近似近傍探索）を使う
    - 距離関数は cosine（コサイン類似度）  

よく使う距離関数：
| 設定値 | 意味 |
|-------|------|
| "cosine" | コサイン類似度（RAG で最も一般的） |
| "l2" | ユークリッド距離 |
| "ip" | 内積（dot product） |

### 6. JSONデータをChromaにロードする関数
```
def load_json_to_chroma():
    ...
```
`RAGの①データ読み込み → ②ベクトル化 → ③Chromaに保存`をまとめて実行。

具体的には：
- certifications.json を読み込む
- skills.json を読み込む
- 大分類（base/value/DS/DE/fusion）を flatten
- Embedding でベクトル化
- Chroma に保存
- persist() で永続化

RAGの前処理（データ準備）を担当。

### 7. RAGの回答生成関数（rag_answer）
```
def rag_answer(query: str):
    ...
```
RAGの本体ロジック。

処理の流れ：
- ① ユーザ質問をベクトル化  
```
embedding = embedder.encode(query)
```
- ② ChromaDBで類似ドキュメント検索  
```
results = collection.query(
    query_embeddings=[embedding],
    n_results=3
)
```
- ③ 検索結果をコンテキストとしてまとめる  
```
context = "\n\n".join(results["documents"][0])
```
- ④ LLMに「質問＋コンテキスト」を渡して回答生成  
```
prompt = f"""
あなたはデータサイエンスのキャリア支援エージェントです。
...
"""
response = llm(prompt)
```
RAGの④検索 → ⑤回答生成を担当します。

### 8. APIエンドポイント
- /health  
```
@app.get("/health")
def health():
    return {"status": "ok"}
```
→ 動作確認用

- /rag  
```
@app.post("/rag")
def rag(query: Query):
    return {"answer": rag_answer(query.query)}
```
→ ユーザが実際に使うAPI  
→ RAG の結果を返す

## まとめ
main.py は RAG の全工程を1ファイルにまとめた構成  

| main.pyの部分 | RAGの工程 | 役割 |
|---------------|-----------|------|
| LLMロード | ⑤回答生成 | LLMによる最終回答 |
| Embeddingロード | ②ベクトル化 | テキスト → ベクトル |
| Chroma初期化 | ③保存 | ベクトルDB |
| load_json_to_chroma | ①読み込み → ②ベクトル化 → ③保存 | データ準備 |
| rag_answer | ④検索 → ⑤回答生成 | RAGの本体 |
| /rag API | 全体 | 外部から利用する窓口 |

