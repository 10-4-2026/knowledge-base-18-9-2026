
- python build_corpus.py

Nếu mục tiêu của bạn là đi theo đúng lộ trình Retrieval System tại VinFast, tôi khuyến nghị làm 1 dự án duy nhất nhưng phát triển theo từng giai đoạn, từ:

Keyword Search
    ↓
Semantic Search
    ↓
Vector Database
    ↓
Hybrid Search
    ↓
RAG
    ↓
Answer with Citation
    ↓
Azure AI Search


Dự án này sẽ giúp bạn cover toàn bộ:

TF-IDF
BM25
Inverted Index
Embedding
Cosine Similarity
FAISS
Qdrant
Azure AI Search
Chunking
Top-K Retrieval
Hybrid Search
RAG
Citation
Dự án đề xuất
VinFast Knowledge Assistant

Bot hỏi đáp tài liệu kỹ thuật xe điện VinFast.

Ví dụ dữ liệu:

docs/

VF3_manual.pdf
VF5_manual.pdf
VF8_manual.pdf
Charging_guide.pdf
Battery_policy.pdf
Warranty_policy.pdf


Người dùng hỏi:

Pin VF8 bảo hành bao lâu?

Làm sao sạc nhanh VF5?

Công suất động cơ VF8 là bao nhiêu?


Bot trả lời:

Theo tài liệu Warranty_policy.pdf:

Pin VF8 được bảo hành 10 năm hoặc
200.000 km tùy điều kiện nào đến trước.

Nguồn:
Warranty_policy.pdf trang 12

Kiến trúc cuối cùng
project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── embeddings/
│
├── vectorstore/
│
├── src/
│
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── build_corpus.py
│
│   ├── keyword_search/
│   │   ├── tfidf_search.py
│   │   ├── bm25_search.py
│   │   └── inverted_index.py
│
│   ├── semantic_search/
│   │   ├── embedding_generator.py
│   │   ├── faiss_search.py
│   │   └── similarity.py
│
│   ├── hybrid/
│   │   └── hybrid_search.py
│
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── prompt_builder.py
│   │   └── rag_pipeline.py
│
│   ├── api/
│   │   └── app.py
│
│   └── configs/
│       └── settings.py
│
├── requirements.txt
└── README.md

Giai đoạn 1 - Data Ingestion
File
src/ingestion/pdf_loader.py

from pypdf import PdfReader

def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

File
src/ingestion/chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_text(text)

File
src/ingestion/build_corpus.py

import json
import os

from pdf_loader import extract_text
from chunker import chunk_text

DATA_DIR = "../../docs"

all_chunks = []

for file in os.listdir(DATA_DIR):

    if file.endswith(".pdf"):

        text = extract_text(
            os.path.join(DATA_DIR, file)
        )

        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):

            all_chunks.append({
                "doc": file,
                "chunk_id": idx,
                "text": chunk
            })

with open(
    "../../data/processed/corpus.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )


Kết quả:

[
  {
    "doc":"VF8_manual.pdf",
    "chunk_id":0,
    "text":"..."
  }
]

Giai đoạn 2 - Keyword Search
2.1 TF-IDF

File:

src/keyword_search/tfidf_search.py

import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

corpus = json.load(
    open(
        "../../data/processed/corpus.json",
        encoding="utf-8"
    )
)

texts = [c["text"] for c in corpus]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(texts)

def search(query, top_k=5):

    q = vectorizer.transform([query])

    scores = cosine_similarity(q, X)[0]

    ranked = scores.argsort()[::-1]

    return [
        corpus[i]
        for i in ranked[:top_k]
    ]

2.2 BM25

File:

src/keyword_search/bm25_search.py

import json

from rank_bm25 import BM25Okapi

corpus = json.load(
    open(
        "../../data/processed/corpus.json",
        encoding="utf-8"
    )
)

texts = [
    x["text"].split()
    for x in corpus
]

bm25 = BM25Okapi(texts)

def search(query):

    scores = bm25.get_scores(
        query.split()
    )

    top = sorted(
        range(len(scores)),
        key=lambda i:scores[i],
        reverse=True
    )[:5]

    return [corpus[i] for i in top]

2.3 Inverted Index

File:

src/keyword_search/inverted_index.py

from collections import defaultdict

index = defaultdict(set)

def build(corpus):

    for doc_id, text in enumerate(corpus):

        for token in text.split():

            index[token.lower()].add(doc_id)

def lookup(word):

    return index[word.lower()]

Giai đoạn 3 - Semantic Search
3.1 Embedding

File:

src/semantic_search/embedding_generator.py


Dùng model:

BAAI/bge-small-en-v1.5


hoặc

intfloat/multilingual-e5-base


Code:

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

def encode(texts):

    return model.encode(
        texts,
        normalize_embeddings=True
    )

3.2 Similarity

File:

src/semantic_search/similarity.py

from sklearn.metrics.pairwise import cosine_similarity

def score(q, docs):

    return cosine_similarity(
        q.reshape(1,-1),
        docs
    )[0]

3.3 Build Vector Store

File:

src/semantic_search/faiss_search.py

import faiss
import json
import numpy as np

from embedding_generator import encode

corpus = json.load(
    open(
        "../../data/processed/corpus.json",
        encoding="utf-8"
    )
)

texts = [x["text"] for x in corpus]

embeddings = encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(
    dimension
)

index.add(
    np.array(
        embeddings,
        dtype=np.float32
    )
)

def search(query):

    q = encode([query])

    scores, idx = index.search(
        np.array(q,dtype=np.float32),
        5
    )

    return [corpus[i] for i in idx[0]]

Giai đoạn 4 - Hybrid Search

Đây là phần mà doanh nghiệp dùng nhiều.

BM25 + Vector Search


File:

src/hybrid/hybrid_search.py

from keyword_search.bm25_search import search as bm25
from semantic_search.faiss_search import search as vec

def search(query):

    bm25_docs = bm25(query)

    vec_docs = vec(query)

    merged = {}

    for d in bm25_docs:
        merged[d["text"]] = d

    for d in vec_docs:
        merged[d["text"]] = d

    return list(
        merged.values()
    )[:5]

Giai đoạn 5 - RAG

Kiến trúc:

Question
  ↓
Retriever
  ↓
Top-5 Chunks
  ↓
Prompt Builder
  ↓
GPT
  ↓
Answer

File
src/rag/retriever.py

from hybrid.hybrid_search import search

def retrieve(query):

    return search(query)

File
src/rag/prompt_builder.py

def build_prompt(query, docs):

    context = "\n\n".join(
        d["text"]
        for d in docs
    )

    return f"""
Bạn là trợ lý VinFast.

Context:

{context}

Question:
{query}

Chỉ trả lời bằng thông tin
trong context.
"""

File
src/rag/rag_pipeline.py

from retriever import retrieve
from prompt_builder import build_prompt

from openai import OpenAI

client = OpenAI()

def ask(question):

    docs = retrieve(question)

    prompt = build_prompt(
        question,
        docs
    )

    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return result.choices[0].message.content

Giai đoạn 6 - Citation

Cần thêm metadata.

Corpus:

{
  "doc":"VF8_manual.pdf",
  "page":12,
  "chunk_id":4,
  "text":"..."
}


Prompt:

context += f"""

Source:
{doc['doc']}
Page:
{doc['page']}
"""


Kết quả:

VF8 được bảo hành pin 10 năm.

Nguồn:
VF8_manual.pdf
Trang 12

Giai đoạn 7 - Azure AI Search (Mức VinFast)

Khi đã xong toàn bộ phía trên:

FAISS sẽ được thay bằng:

Azure AI Search


Workflow:

PDF
 ↓

Chunking
 ↓

Azure OpenAI Embedding
 ↓

Azure AI Search Index
 ↓

Hybrid Retrieval
 ↓

GPT-4o
 ↓

Answer + Citation

requirements.txt
langchain
pypdf
sentence-transformers
faiss-cpu
rank-bm25
scikit-learn
openai
fastapi
uvicorn

Thứ tự học và thực hiện (quan trọng)

Tuần 1:

PDF Loader
Chunking
TF-IDF
Inverted Index


Tuần 2:

BM25
Cosine Similarity
Embedding


Tuần 3:

FAISS
Vector Search
Top-K


Tuần 4:

Hybrid Search
RAG
Prompt Engineering


Tuần 5:

Source Citation
Evaluation


Tuần 6:

Azure AI Search
Azure OpenAI
Production Deployment


Nếu đi hết dự án trên và tự code lại được từ đầu không nhìn tài liệu, bạn sẽ đáp ứng gần như đầy đủ các yêu cầu của phần "Giai đoạn 3: Retrieval System" trong lộ trình AI Engineer/RAG và cũng là nền tảng rất sát với các bài toán Enterprise RAG tại VinFast.