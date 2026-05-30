# 一括での比較

| DB | 特徴 | 向いている用途 |
|----|------|--------------|
| Chroma | 軽量・簡単・ローカル完結 | PoC、小規模RAG、個人開発 |
| FAISS | 超高速・ローカル | 小〜中規模、メタデータ不要 |
| Qdrant | Rust製・高速・メタデータ強い | 中規模RAG、クラウド運用 |
| Milvus | 大規模・本格的 | 企業向け、大規模データ |

# Chroma
Chromaは軽量・高速・シンプル・ローカル完結を強みにしたVectorDBで、RAGのPoC（プロトタイプ）に最も使われるデータベース。

## 特徴
- 軽量で簡単
    - 内部でHNSWを使っているため、高速で高精度な類似検索が
- ローカルで完結
    - 永続化（PersistentClient）が簡単で、ローカルフォルダへのベクトルDBの保存が簡単。
- メタデータ検索が強い
    - ドキュメントごとに自由なメタデータを持てる → 「DS のスキルだけ検索」などが簡単にできる。
- RAGのPoCに最適
    - Python からの操作が圧倒的に簡単で、FAISSやMilvusに比べて、コードが圧倒的に短い
- LLM・Embeddingとの相性が良い  
    特に：
    - SentenceTransformer
    - OpenAI Embeddings
    - Cohere Embeddings

    などと組み合わせると安定する。
- 大規模データには向かない
    - 数百万件以上のデータになると、MilvusやQdrantの方が安定。
- クラスタリングや複雑な検索は弱い  
    以下の用途ではMilvusやQdrantの方が強い。
    - 複雑なフィルタ
    - 複合検索
    - 高度なスコアリング
- サーバーモードがまだ発展途上
    - ローカル前提で作られており、クラウドでの大規模運用はまだ弱い。


## インストール

```
pip install chromadb
```

## コード例
```
import chromadb

chroma_client = PersistentClient(path="./vectorstore")

collection = chroma_client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)
```

# FAISS
FAISSはMetaが開発した高速ベクトル検索ライブラリで、ローカルで完結する最も軽量な選択肢。

## 特徴
- 超高速
- ローカルで完結
- メタデータ管理は自前で実装が必要
- 小規模 RAG に最適

## インストール

```
pip install faiss-cpu
```

## コード例
```
import faiss
import numpy as np

# ベクトルの次元数
dim = 384  # MiniLM の場合

# Index の作成（コサイン類似度の場合は正規化が必要）
index = faiss.IndexFlatIP(dim)

# ベクトル追加
vectors = np.array(embeddings).astype("float32")
faiss.normalize_L2(vectors)
index.add(vectors)

# 検索
query_vec = embedder.encode(query).astype("float32")
faiss.normalize_L2(query_vec.reshape(1, -1))
scores, ids = index.search(query_vec.reshape(1, -1), k=3)
```

# Milvus
Milvusは大規模データ向けの本格的なVectorDB。

## 特徴
- 大規模データ向け
- 高速・高精度
- クラウド運用に向く
- ACA や AKS と相性が良い

## インストール

```
pip install pymilvus
```

## コード例（超簡略版）
```
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

connections.connect("default", host="localhost", port="19530")

# スキーマ定義
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]
schema = CollectionSchema(fields, description="RAG collection")

collection = Collection("rag_collection", schema)

# データ挿入
collection.insert([ids, embeddings])

# 検索
results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param={"metric_type": "COSINE"},
    limit=3
)
```

# Qdrant
QdrantはAPIが非常に使いやすく、ローカルでもクラウドでも動く人気のVectorDB。

## 特徴
- Rust 製で高速
- メタデータ検索が強い
- ローカルでもクラウドでも動く
- Chroma の上位互換に近い使い勝手

## インストール

```
pip install qdrant-client
```

## コード例
```
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(path="./qdrant")

client.recreate_collection(
    collection_name="rag_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# データ追加
client.upsert(
    collection_name="rag_collection",
    points=[
        {"id": i, "vector": embeddings[i], "payload": metadatas[i]}
        for i in range(len(embeddings))
    ]
)

# 検索
results = client.search(
    collection_name="rag_collection",
    query_vector=query_embedding,
    limit=3
)
```

