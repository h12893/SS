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
import time

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
ver_num = ".1.3.0"  # バージョン番号を定数として定義
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
            # print(f"処理中のスキル: {name}")
            # if name[0] != '"':
            #     name = '"' + name
            # if name[-1] != '"':
            #     name = name + '"'
            # print(f"スキル名: {name}")
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

# カテゴリ別のLLM実行関数
def run_llm_for_category(category, docs, query):
    context = "\n\n".join(docs)

    prompt = f"""
あなたはスキルカテゴリ「{category}」のアセッサーです。
以下のスキル定義（コンテキスト）とユーザの記述から、ユーザが満たしているスキルのみを JSON 形式で返してください。

出力形式（厳守）：
[
  {{"skill": "スキル名", "level": 数値}},
  ...
]

制約：
- JSON 以外の文章は出力しない
- "..." を使わない
- assistant などの余計な語を出力しない
- スキル名は必ずダブルクォートで囲む
- 日本語で返す

# コンテキスト
{context}

# ユーザ記述
{query}

# JSON 出力
"""

    response = llm(prompt, max_tokens=1024*10)
    raw = response["choices"][0]["text"]

    # JSON 抽出（あなたが実装済みの extract_json を使う）
    json_str = extract_json(raw)
    json_str = normalize_skill_json(json_str)

    try:
        parsed = json.loads(json_str)
        return normalize_llm_output(parsed)
    except json.JSONDecodeError as e:
        debug_json_error(json_str, e)
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

def rag_answer(query: str):
    # 処理時間の計測用
    start_time = time.time()
    
    # ① ユーザ質問をベクトル化
    embedding = embedder.encode(query).tolist()

    # ②-1 ChromaDB で類似ドキュメント検索
    results = collection.query(
    query_embeddings=[embedding],
    n_results=15,
    # n_results=50,
    include=["documents", "metadatas", "distances"]
    )

    # docs = []
    # distances = results.get("distances", [[]])[0] or []
    # documents = results.get("documents", [[]])[0] or []

    # # ③-2 検索結果をスコア値でフィルタリング
    # min_score = 100
    # for doc, score in zip(documents, distances):
    #     if score < min_score:
    #         min_score = score
    #     if score < 0.8:  # cosine距離なので小さいほど近い
    #         docs.append(doc)
    # print(f"最小スコア: {min_score}, フィルタ後ドキュメント数: {len(docs)}")

    # for doc in docs:
    #     print(f"ドキュメント: {doc[:100]}...")  # ドキュメントの先頭100文字を表示

    docs_by_category = {
    "base": [],
    "value": [],
    "DS": [],
    "DE": [],
    "fusion": []
    }

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if dist < 0.8:
            cat = meta["category"]
            docs_by_category[cat].append(doc)

#     # fallback
#     if not docs:
#         docs = documents

#     # ③ 検索結果をコンテキストとしてまとめる
#     context = "\n\n".join(docs)
#     print(f"コンテキストの長さ（文字数）: {len(context)}")
#     print(f"コンテキスト: {context}")

#     # コンテキストが空の場合のフォールバック
#     if len(context) == 0:
#         context = "（スキルデータが見つかりませんでした）"

#     # ④ LLM に構造化 JSON を返させるプロンプト
#     prompt = f"""
# あなたはデータサイエンス協会のスキルチェックリストに基づいて、
# ユーザが満たしているスキルを判定するアセッサーです。

# 以下のコンテキストには、スキル項目（base/value/DS/DE/fusion）が含まれています。
# ユーザの質問内容から、ユーザが「満たしている」と判断できるスキルを抽出し、
# 必ず次の JSON 形式で返してください。

# 出力形式（厳守）：

# {{
#   "base": [
#     {{"skill": "スキル名", "level": 数値}},
#     ...
#   ],
#   "value": [...],
#   "DS": [...],
#   "DE": [...],
#   "fusion": [...]
# }}

# 制約：
# - JSON 以外の文章は一切出力しない
# - もしコンテキストに該当スキルが見つからない場合でも、ユーザの記述内容から明確に判断できる場合はスキルを含めてよい。
# - 分類がvalueのスキルは、Noが同じスキルが複数該当している場合は、最も高いレベルのスキルを返す。
# - 曖昧な場合は含めない
# - 絵文字は禁止
# - 日本語で返す
# - 不要な記号（\\n や *** など）は使わない

# # コンテキスト
# {context}

# # ユーザ質問
# {query}

# # JSON 出力
# """

    # # ⑤ LLM 実行
    # response = llm(prompt, max_tokens=1024*16)  # 出力トークン数の上限。必要に応じて調整
    # print(f"LLM 生の出力: {response}")

    # # ⑥ LLM の出力（JSON文字列）を抽出
    # raw_output = response["choices"][0]["text"]

    # json_str = extract_json(raw_output)
    # print("抽出した JSON:", json_str)
    # json_str = normalize_skill_json(json_str)
    # print("形式を補正した JSON:", json_str)

    # # ⑨ レーダーチャート用に結果をファイルで出力
    # skills_path = f"./output/{folder_ver_num}/before/before_v{ver_num}_{len(os.listdir(f'./output/{folder_ver_num}/before/'))}.json"
    # skills_path = Path(skills_path)
    # print(f"出力ファイルパス: {skills_path}")
    # try:
    #     with open(skills_path, "w", encoding="utf-8-sig") as f:
    #         json.dump(json_str, 
    #                   f, 
    #                   ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
    #                   indent=4 # indent=4 で見やすく整形
    #                   )
    #     print(f"json_strをJSONファイルに保存しました: {skills_path}")
    # except (OSError, TypeError) as e:
    #     print(f"json_str保存中にエラーが発生しました: {e}")

    # # ⑦ JSON としてパース
    # try:
    #     skill_json = json.loads(json_str)
    #     print("パースした skill_json:", skill_json)
    # except json.JSONDecodeError as e:
    #     debug_json_error(json_str, e)
    #     # JSON 解析に失敗した場合は空の構造を返す
    #     skill_json = {"base": [], "value": [], "DS": [], "DE": [], "fusion": []}

    skill_json = {
        "base": run_llm_for_category("base", docs_by_category["base"], query),
        "value": run_llm_for_category("value", docs_by_category["value"], query),
        "DS": run_llm_for_category("DS", docs_by_category["DS"], query),
        "DE": run_llm_for_category("DE", docs_by_category["DE"], query),
        "fusion": run_llm_for_category("fusion", docs_by_category["fusion"], query),
    }

    # ⑧ レーダーチャートの出力
    # ⑧-1 レーダーチャート用の集計
    # radar = {}
    # for category, items in skill_json.items():
    #     total = 0
    #     for item in items:
    #         level = item.get("level", 0)
    #         total += int(level)
    #     radar[category] = total

    # ⑧ レーダーチャートの出力
    # ⑧-1 レーダーチャート用の集計
    radar = {}
    for category, items in skill_json.items():
        radar[category] = sum(int(item["level"]) for item in items)

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
    # カテゴリ
    categories = ["base", "value", "DS", "DE", "fusion"]

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
def rag_endpoint(q: Query):
    answer = rag_answer(q.query)
    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "ok"}
