from fastapi import FastAPI, Request
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
# from llama_cpp import Llama
import json
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import time
import asyncio
import httpx

# # -----------------------------deactiva
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
ver_num = ".2.0.1"  # バージョン番号を定数として定義
# outputフォルダは以下にバージョン番号名のフォルダが無ければ作成する
folder_ver_num = ver_num[1:]  # バージョン番号から先頭のドットを除いた部分をフォルダ名に使用
if not os.path.exists(f"./output/{folder_ver_num}"):
    os.makedirs(f"./output/{folder_ver_num}/skills", exist_ok=True)
    os.makedirs(f"./output/{folder_ver_num}/radar", exist_ok=True)
    os.makedirs(f"./output/{folder_ver_num}/radarchart", exist_ok=True)
    os.makedirs(f"./output/{folder_ver_num}/answer", exist_ok=True)
    os.makedirs(f"./output/{folder_ver_num}/before", exist_ok=True)
output_path = f"./output/{folder_ver_num}/answer/answer_v{ver_num}_{len(os.listdir(f'./output/{folder_ver_num}/answer'))}.txt"
output_path = Path(output_path)
print(f"出力ファイルパス: {output_path}")

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
    total_skill_level = {}

    for category, items in skills_data.items():
        skill_level_sum = 0
        for i, skill in enumerate(items):
            name = str(skill.get("No", ""))+"-"+str(skill.get("SubNo", ""))
            level = skill.get("スキルレベル", "")
            level = level.count("★")  # レベルは★の数で表現されていると仮定
            desc = skill.get("チェック項目", "")

            skill_level_sum += level

            # ★ embedding 用に強いテキストを組み立てる
            doc = f"[カテゴリ: {category}] スキル名: {name}（レベル{level}） 説明: {desc}"

            documents.append(doc)
            metadatas.append({
                "category": category,
                "name": name,
                "level": level
            })
            ids.append(f"{category}_{i}")

        total_skill_level[category] = skill_level_sum

    return documents, metadatas, ids, total_skill_level

# ① JSON 読み込み
with open("./data/skillcheck_ver6.00_V.1.1.0.json", "r", encoding="utf-8-sig") as f:
    skills_data = json.load(f)

# ② embedding に強い文書を作る
documents, metadatas, ids, total_skill_level = build_skill_documents(skills_data)

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
    with open("./data/skillcheck_ver6.00_V.1.1.0.json", "r", encoding="utf-8-sig") as f:
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

# 抽出したJSONのスキル名を "No-SubNo" 形式に正規化する関数
def normalize_skill_json(json_str: str) -> str:
    """
    JSON文字列中の skill: 22-22 のような不正な値を
    "22-22" に強制変換する
    """
    import re

    fixed = re.sub(
        r'"skill"\s*:\s*([0-9]+-[0-9]+)',
        r'"skill": "\1"',
        json_str
    )

    return fixed

# LLM の出力を正規化する関数
def normalize_llm_output(obj):
    """
    LLM が返した JSON を必ず list[dict] に正規化する
    """
    # case1: dict → [dict]
    if isinstance(obj, dict):
        return [obj]

    # case2: list → 中身をチェック
    if isinstance(obj, list):
        fixed = []
        for item in obj:
            if isinstance(item, dict):
                fixed.append(item)
            elif isinstance(item, str):
                # 文字列なら無視 or パースを試みる
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, dict):
                        fixed.append(parsed)
                except:
                    pass
        return fixed

    # case3: 文字列 → パースを試みる
    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
            return normalize_llm_output(parsed)
        except:
            return []

    # その他は空
    return []

# カテゴリ別のLLM実行関数（ollamaによる非同期版）
async def run_llm_for_category(category, docs, query):
    context = "\n\n".join(docs)

    prompt = f"""
あなたはスキルカテゴリ「{category}」のアセッサーです。
以下のスキル定義（コンテキスト）とユーザ記述から、
該当スキルのみを JSON 形式で返してください。

出力形式（厳守）：
[
  {{"skill": "スキル名", "level": 数値}}
]

制約：
- JSON 以外の文章は出力しない
- "..." を使わない
- スキル名は必ずダブルクォートで囲む
- スキル名（skill）は必ず "数字-数字" の形式とする（スキルの説明文の一部などを使用してはいけない）。
- スキルレベル（level）は★の数を数値に変換して返し、"初級"、"中級"、"上級" などの文字表現は使わない

# コンテキスト
{context}

# ユーザ記述
{query}

# JSON 出力
"""

    url = "http://localhost:11434/api/generate"
    # 逐次読み取り用バッファ
    full_text = ""

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            url,
            json={
                "model": "my-llama3", # 通常版
                # "model": "my-llama3-3b", # 軽量版
                "prompt": prompt,
                "stream": True
            }
        ) as response:

            async for line in response.aiter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # 逐次生成されたテキストを蓄積
                if "response" in data:
                    full_text += data["response"]

                # 完了フラグ
                if data.get("done"):
                    break

    # JSON 抽出（あなたの既存関数を利用）
    json_str = extract_json(full_text)
    json_str = normalize_skill_json(json_str)

    try:
        parsed = json.loads(json_str)
        return normalize_llm_output(parsed)
    except Exception:
        return []

# JSONDecodeError の詳細を表示する関数
def debug_json_error(json_str: str, error: json.JSONDecodeError):
    print("\n=== JSON Decode Error ===")
    print(f"Error message : {error.msg}")
    print(f"Line          : {error.lineno}")
    print(f"Column        : {error.colno}")
    print(f"Char position : {error.pos}")

    # JSON を行ごとに分割
    lines = json_str.splitlines()

    # エラー行を表示（前後の行も表示すると便利）
    start = max(0, error.lineno - 3)
    end = min(len(lines), error.lineno + 2)

    print("\n--- JSON snippet around error ---")
    for i in range(start, end):
        prefix = ">>" if (i + 1) == error.lineno else "  "
        print(f"{prefix} {i+1:3d}: {lines[i]}")
    
    error_line = lines[error.lineno - 1]
    pointer = " " * (error.colno - 1) + "^"
    print(error_line)
    print(pointer)

def normalize_level(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        # 日本語 → 数値
        if value == "初級": return 1
        if value == "中級": return 2
        if value == "上級": return 3

        # ★ → 数値
        if set(value) == {"★"}:
            return len(value)

        # 数値文字列
        if value.isdigit():
            return int(value)

    # それ以外は 0 とみなす
    return 0

@app.post("/rag")
async def rag_answer(request: Request):
    start_time = time.time()
    body = await request.json()
    query = body["query"]

    # embedding → 類似検索（あなたの既存コード）
    # embedding = embedder.embed(query)
    embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=50,
        include=["documents", "metadatas", "distances"]
    )

    # カテゴリごとに分類
    docs_by_category = {"base": [], "value": [], "DS": [], "DE": [], "fusion": []}

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if dist < 0.8:
            docs_by_category[meta["category"]].append(doc)

    # 並列で LLM を呼ぶ
    categories = ["base", "value", "DS", "DE", "fusion"]

    LLM_results = await asyncio.gather(
        run_llm_for_category("base", docs_by_category["base"], query),
        run_llm_for_category("value", docs_by_category["value"], query),
        run_llm_for_category("DS", docs_by_category["DS"], query),
        run_llm_for_category("DE", docs_by_category["DE"], query),
        run_llm_for_category("fusion", docs_by_category["fusion"], query)
    )

    skill_json = {}

    for cat, res in zip(categories, LLM_results):
        if isinstance(res, list):
            skill_json[cat] = res
        else:
            skill_json[cat] = []  # 壊れていたら空にする

    # ⑧ レーダーチャートの出力
    # ⑧-1 レーダーチャート用の集計
    radar = {}
    for category, items in skill_json.items():
        # radar[category] = sum(int(item["level"]) for item in items)
        radar[category] = sum(normalize_level(item["level"]) for item in items)

    # ⑨ レーダーチャート用に結果をファイルで出力
    skills_path = f"./output/{folder_ver_num}/skills/skills_v{ver_num}_{len(os.listdir(f'./output/{folder_ver_num}/skills/'))}.json"
    skills_path = Path(skills_path)
    print(f"出力ファイルパス: {skills_path}")
    try:
        with open(skills_path, "w", encoding="utf-8-sig") as f:
            json.dump(skill_json, 
                      f, 
                      ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
                      indent=4 # indent=4 で見やすく整形
                      )
        print(f"skill_jsonをJSONファイルに保存しました: {skills_path}")
    except (OSError, TypeError) as e:
        print(f"skill_json保存中にエラーが発生しました: {e}")

    radar_path = f"./output/{folder_ver_num}/radar/radar_v{ver_num}_{len(os.listdir(f'./output/{folder_ver_num}/radar/'))}.json"
    radar_path = Path(radar_path)
    print(f"出力ファイルパス: {radar_path}")
    try:
        with open(radar_path, "w", encoding="utf-8-sig") as f:
            json.dump(radar, 
                      f, 
                      ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
                      indent=4 # indent=4 で見やすく整形
                      )
        print(f"radarデータをJSONファイルに保存しました: {radar_path}")
    except (OSError, TypeError) as e:
        print(f"radarデータ保存中にエラーが発生しました: {e}")

    # ⑧-2 レーダーチャートの出力

    # 合計値
    values = []
    for cat in categories: 
        # カテゴリごとの合計値を全スキルレベルの合計で割って正規化。total_skill_levelが0の場合は1で割る（実際にはそのカテゴリのスキルがないので0になるはず）
        values.append(round(radar[cat] / total_skill_level.get(cat, 1), 2))  

    # レーダーチャートは最初の値を最後に追加して閉じる
    values += values[:1]

    # 角度を計算
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # 描画
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 半径方向の最小値・最大値設定
    ax.set_ylim(0, 1)  # ここで最小値0、最大値1に設定

    # 角度の開始位置を調整（例: 上方向をスタートにする）
    ax.set_theta_offset(np.pi / 2)  # π/2 で上方向
    # 時計回りにする場合は -1、反時計回りは 1
    ax.set_theta_direction(-1)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    # 軸ラベル
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # タイトル
    ax.set_title("Skill Radar Chart", fontsize=16)

    # ファイル出力
    plt.savefig(f"./output/{folder_ver_num}/radarchart/radarchart_v{ver_num}_{len(os.listdir(f'./output/{folder_ver_num}/radarchart/'))}.png")

    skill_txt = json.dumps(skill_json, ensure_ascii="utf-8-sig", indent=4)
    radar_txt = json.dumps(radar, ensure_ascii="utf-8-sig", indent=4)
    answer_txt = "=== スキルチェック結果 ===" + \
        skill_txt + \
        "\n\n" + \
        "=== レーダーチャート結果 ===" + \
         radar_txt
        #  "\n\n" + \
        # "=== コンテキスト ===" + \
        #  context
    try:
        with open(output_path, "w", encoding="utf-8-sig") as f:
            f.write(answer_txt)
        print(f"回答データをtxtファイルに保存しました: {output_path}")
    except (OSError, TypeError) as e:
        print(f"radarデータ保存中にエラーが発生しました: {e}")

    # 処理時間の計測用
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"処理時間: {processing_time:.2f}秒")

    # ⑩ 最終レスポンス
    return {
        "skills": skill_json,
        "radar_chart": radar
    }


# -----------------------------
# 7. FastAPI エンドポイント
# -----------------------------
@app.post("/rag")
async def rag_endpoint(q: Query):
    answer = await rag_answer(q.query)
    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "ok"}
