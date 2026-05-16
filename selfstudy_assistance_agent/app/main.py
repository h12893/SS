from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
import json
import os

app = FastAPI()

# -----------------------------
# 1. Embedding モデル
# -----------------------------
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# 2. Chroma（ローカル永続化）
# -----------------------------
chroma_client = PersistentClient(path="./vectorstore")

collection = chroma_client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)

# -----------------------------
# 3. ローカル LLM（Phi-3）
# -----------------------------
llm = Llama(
    # model_path="./models/phi-3-mini.gguf",
    model_path="./models/Llama-3-8B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=4
)

# -----------------------------
# 4. JSON データを Chroma に投入
# -----------------------------
# def load_json_to_chroma():
#     if len(collection.get()["ids"]) > 0:
#         return  # すでに投入済み

#     with open("./data/資格一覧.json", "r", encoding="utf-8-sig") as f:
#         certs = json.load(f)

#     with open("./data/skillcheck_ver6.00.json", "r", encoding="utf-8-sig") as f:
#         skills = json.load(f)

#     docs = []
#     metadatas = []
#     ids = []

#     for i, item in enumerate(certs + skills):
#         text = json.dumps(item, ensure_ascii=False)
#         docs.append(text)
#         metadatas.append(item)
#         ids.append(f"doc-{i}")

#     embeddings = embedder.encode(docs).tolist()

#     collection.add(
#         documents=docs,
#         embeddings=embeddings,
#         metadatas=metadatas,
#         ids=ids
#     )

#     chroma_client.persist()

def load_json_to_chroma():
    if len(collection.get()["ids"]) > 0:
        return

    # --- certifications.json ---
    with open("./data/資格一覧.json", "r", encoding="utf-8-sig") as f:
        certs_json = json.load(f)
        certs = certs_json["qualification"] if isinstance(certs_json, dict) else certs_json

    # --- skills.json ---
    with open("./data/skillcheck_ver6.00.json", "r", encoding="utf-8-sig") as f:
        skills_json = json.load(f)

    # skills.json は {category: [items]} の構造なので flatten する
    skills = []
    for category, items in skills_json.items():
        for item in items:
            # 大分類をメタデータとして付与
            item_with_category = {
                **item,
                "category": category
            }
            skills.append(item_with_category)

    # --- Chroma に投入 ---
    docs = []
    metadatas = []
    ids = []

    all_items = certs + skills

    for i, item in enumerate(all_items):
        text = json.dumps(item, ensure_ascii=False)
        docs.append(text)
        metadatas.append(item)
        ids.append(f"doc-{i}")

    embeddings = embedder.encode(docs).tolist()

    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    chroma_client.persist()


load_json_to_chroma()

# -----------------------------
# 5. API モデル
# -----------------------------
class Query(BaseModel):
    query: str


# -----------------------------
# 6. RAG パイプライン
# -----------------------------
def rag_answer(query: str):
    # ① クエリを埋め込み
    query_vec = embedder.encode([query]).tolist()[0]

    # ② Chroma で検索
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    context = "\n\n".join(retrieved_docs)

    # ③ LLM に渡すプロンプト
    prompt = f"""
あなたはデータサイエンス分野のキャリア支援エージェントです。
以下の情報を参考に、ユーザの質問に答えてください。
- 出力は必ず **日本語** にする
- 絵文字（😊 など）は一切使用しない
- 不要な記号（\\n や *** など）は使わず、自然な文章として整形する
- 箇条書きは「・」を使う

# コンテキスト
{context}

# ユーザ質問
{query}

# 回答
"""

    output = llm(prompt, max_tokens=512)
    return output["choices"][0]["text"]


# -----------------------------
# 7. FastAPI エンドポイント
# -----------------------------
@app.post("/rag")
def rag_endpoint(q: Query):
    answer = rag_answer(q.query)
    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "ok"}
