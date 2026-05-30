from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
import json
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# # -----------------------------
# # 0. 自作関数のインポート
# # -----------------------------
# def reload_or_import(module_name):
#     if module_name in sys.modules:
#         return importlib.reload(sys.modules[module_name])
#     return importlib.import_module(module_name)

# # ReadWriteData.pyから関数をインポート
# try:
#     reload_or_import("source.mylib.ReadWriteData")
#     from source.mylib.ReadWriteData import *
#     print("✓ source/mylib/ReadWriteData.py のインポートに成功しました")
# except ImportError as e:
#     print(f"✗ インポートエラー: {e}")
# except Exception as e:
#     print(f"✗ エラー: {e}")

app = FastAPI()
output_path = f"./output/answer/answer_{len(os.listdir('./output'))}.json"
output_path = Path(output_path)
print(f"出力ファイルパス: {output_path}")
ver_num = ".1.0.1"  # バージョン番号を定数として定義

# -----------------------------
# 1. Embedding モデル
# -----------------------------
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# 2. Chroma（ローカル永続化）
# -----------------------------
chroma_client = PersistentClient(path="./vectorstore")

collection = chroma_client.get_or_create_collection(
    name=f"rag_collection_v{ver_num}",
    metadata={"hnsw:space": "cosine"}
)

# embeddingに強いスキル文書作成（JSON データから Chroma に登録するための文書、メタデータ、ID を作成する関数）
def build_skill_documents(skills_data):
    documents = []
    metadatas = []
    ids = []

    for category, items in skills_data.items():
        for i, skill in enumerate(items):
            name = str(skill.get("No", ""))+"-"+str(skill.get("SubNo", ""))
            level = skill.get("スキルレベル", "")
            level = level.count("★")  # レベルは★の数で表現されていると仮定
            desc = skill.get("チェック項目", "")

            # ★ embedding 用に強いテキストを組み立てる
            doc = f"[カテゴリ: {category}] スキル名: {name}（レベル{level}） 説明: {desc}"

            documents.append(doc)
            metadatas.append({
                "category": category,
                "name": name,
                "level": level
            })
            ids.append(f"{category}_{i}")

    return documents, metadatas, ids

# ① JSON 読み込み
with open("./data/skillcheck_ver6.00.json", "r", encoding="utf-8-sig") as f:
    skills_data = json.load(f)

# ② embedding に強い文書を作る
documents, metadatas, ids = build_skill_documents(skills_data)

# ③ embedding を計算
embeddings = embedder.encode(documents).tolist()

# ④ Chroma に登録
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

# -----------------------------
# 3. ローカル LLM（Llama）
# -----------------------------
llm = Llama(
    # model_path="./models/phi-3-mini.gguf",
    model_path="./models/Llama-3-8B-Instruct-Q4_K_M.gguf",
    # コンテキストウィンドウサイズ（モデルが一度に読み込める文章量）。
    # 入力と出力の合計で単位はトークン（日本語なら1トークンはほぼ1文字）
    #  Llama‑3 8B なら32768（32K）まで対応しているが、環境によってはメモリ不足になる可能性があるため、16384（16K）に設定。
    n_ctx=16384, 
    n_threads=12 # CPUのスレッド数。使用環境のコア数に合わせて調整（CPUの物理コア数×2 以上は効果がないことが多い）
)

# -----------------------------
# 4. JSON データを Chroma に投入
# -----------------------------
# JSON データを Chroma に投入する関数
def load_json_to_chroma():
    if len(collection.get()["ids"]) > 0:
        return

    # --- certifications.json ---
    with open("./data/資格一覧_ver1.00.json", "r", encoding="utf-8-sig") as f:
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
# LLM の出力から最初の JSON ブロックを抽出する関数
def extract_json(text: str) -> str:
    start = text.find("{")
    if start == -1:
        return ""

    brace_count = 0
    in_json = False
    json_str = ""

    for i in range(start, len(text)):
        char = text[i]

        if char == "{":
            brace_count += 1
            in_json = True

        if in_json:
            json_str += char

        if char == "}":
            brace_count -= 1
            if brace_count == 0:
                break

    return json_str


def rag_answer(query: str):
    # ① ユーザ質問をベクトル化
    embedding = embedder.encode(query).tolist()

    # ②-1 ChromaDB で類似ドキュメント検索
    results = collection.query(
    query_embeddings=[embedding],
    n_results=50,
    include=["documents", "distances"]
    )

    docs = []
    distances = results.get("distances", [[]])[0] or []
    documents = results.get("documents", [[]])[0] or []

    # ③-2 検索結果をスコア値でフィルタリング
    min_score = 100
    for doc, score in zip(documents, distances):
        if score < min_score:
            min_score = score
        if score < 0.8:  # cosine距離なので小さいほど近い
            docs.append(doc)
    print(f"最小スコア: {min_score}, フィルタ後ドキュメント数: {len(docs)}")

    for doc in docs:
        print(f"ドキュメント: {doc[:100]}...")  # ドキュメントの先頭100文字を表示

    # fallback
    if not docs:
        docs = documents

    # ③ 検索結果をコンテキストとしてまとめる
    context = "\n\n".join(docs)
    print(f"コンテキストの長さ（文字数）: {len(context)}")
    print(f"コンテキスト: {context}")

    # コンテキストが空の場合のフォールバック
    if len(context) == 0:
        context = "（スキルデータが見つかりませんでした）"

    # ④ LLM に構造化 JSON を返させるプロンプト
    prompt = f"""
あなたはデータサイエンス協会のスキルチェックリストに基づいて、
ユーザが満たしているスキルを判定するアセッサーです。

以下のコンテキストには、スキル項目（base/value/DS/DE/fusion）が含まれています。
ユーザの質問内容から、ユーザが「満たしている」と判断できるスキルを抽出し、
必ず次の JSON 形式で返してください。

出力形式（厳守）：

{{
  "base": [
    {{"skill": "スキル名", "level": 数値}},
    ...
  ],
  "value": [...],
  "DS": [...],
  "DE": [...],
  "fusion": [...]
}}

制約：
- JSON 以外の文章は一切出力しない
- もしコンテキストに該当スキルが見つからない場合でも、ユーザの記述内容から明確に判断できる場合はスキルを含めてよい。
- レベルは該当スキルの最大レベルを返す
- 曖昧な場合は含めない
- 絵文字は禁止
- 日本語で返す
- 不要な記号（\\n や *** など）は使わない

# コンテキスト
{context}

# ユーザ質問
{query}

# JSON 出力
"""

    # ⑤ LLM 実行
    response = llm(prompt, max_tokens=16384)  # 出力トークン数の上限。必要に応じて調整
    print(f"LLM 生の出力: {response}")

    # ⑥ LLM の出力（JSON文字列）を抽出
    raw_output = response["choices"][0]["text"]

    json_str = extract_json(raw_output)
    print("抽出した JSON:", json_str)

    # ⑦ JSON としてパース
    try:
        skill_json = json.loads(json_str)
        print("パースした skill_json:", skill_json)
    except json.JSONDecodeError as e:
        print(f"JSON 解析エラー: {e}")
        # JSON 解析に失敗した場合は空の構造を返す
        skill_json = {"base": [], "value": [], "DS": [], "DE": [], "fusion": []}

    # ⑧ レーダーチャートの出力
    # ⑧-1 レーダーチャート用の集計
    radar = {}
    for category, items in skill_json.items():
        total = 0
        for item in items:
            level = item.get("level", 0)
            total += int(level)
        radar[category] = total

    # ⑨ レーダーチャート用に結果をファイルで出力
    skills_path = f"./output/skills/skills_v{ver_num}_{len(os.listdir('./output/skills/'))}.json"
    skills_path = Path(skills_path)
    print(f"出力ファイルパス: {skills_path}")
    try:
        with open(skills_path, "w", encoding="utf-8-sig") as f:
            json.dump(skill_json, 
                      f, 
                      ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
                      indent=4 # indent=4 で見やすく整形
                      )
        print("skill_jsonをJSONファイルに保存しました: skills_path")
    except (OSError, TypeError) as e:
        print(f"skill_json保存中にエラーが発生しました: {e}")

    radar_path = f"./output/radar/radar_v{ver_num}_{len(os.listdir('./output/radar/'))}.json"
    radar_path = Path(radar_path)
    print(f"出力ファイルパス: {radar_path}")
    try:
        with open(radar_path, "w", encoding="utf-8-sig") as f:
            json.dump(radar, 
                      f, 
                      ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
                      indent=4 # indent=4 で見やすく整形
                      )
        print("radarデータをJSONファイルに保存しました: radar_path")
    except (OSError, TypeError) as e:
        print(f"radarデータ保存中にエラーが発生しました: {e}")



    # ⑧-2 レーダーチャートの出力
    # カテゴリ
    categories = ["base", "value", "DS", "DE", "fusion"]

    # 合計値
    values = []
    for cat in categories: 
        values.append(radar[cat])

    # レーダーチャートは最初の値を最後に追加して閉じる
    values += values[:1]

    # 角度を計算
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # 描画
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    # 軸ラベル
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # タイトル
    ax.set_title("Skill Radar Chart", fontsize=16)

    # ファイル出力
    plt.savefig(f"./output/radarchart/radarchart_v{ver_num}_{len(os.listdir('./output/radarchart/'))}.png")

    # ⑩ 最終レスポンス
    return {
        "skills": skill_json,
        "radar_chart": radar
    }

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
