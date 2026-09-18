Rất tốt. Tôi đề xuất chúng ta làm theo phương pháp của một AI Engineer thực thụ:

Không học xong rồi mới làm.

Làm từng phần nhỏ, mỗi phần đều chạy được và có sản phẩm.

Tôi sẽ hướng dẫn bạn như một mentor kỹ thuật. Sau mỗi bước, bạn sẽ có một sản phẩm hoạt động được.

Tổng quan dự án

Mục tiêu cuối:

Người dùng hỏi
    ↓
"VF8 dùng loại pin gì?"

    ↓

Retriever tìm tài liệu

    ↓

LLM đọc tài liệu

    ↓

Trả lời có nguồn dẫn

"VF8 sử dụng pin Lithium-ion...
Nguồn: VF8_manual.pdf, trang 25"

BƯỚC 0 - Chuẩn bị môi trường
Tạo project
mkdir vinfast-rag
cd vinfast-rag

Tạo virtual environment
python -m venv .venv


Windows:

.venv\Scripts\activate


Linux:

source .venv/bin/activate

Cài package
pip install pandas
pip install numpy
pip install scikit-learn
pip install rank-bm25
pip install sentence-transformers
pip install faiss-cpu
pip install pypdf
pip install streamlit

Cấu trúc thư mục
vinfast-rag/

data/
    pdfs/

src/

app.py

requirements.txt

BƯỚC 1 - Xây Knowledge Base

Mục tiêu:

PDF
↓
TXT
↓
Knowledge Base

Chuẩn bị dữ liệu

Cho vào:

data/pdfs/

VF8_Manual.pdf
VF9_Manual.pdf
ChargingGuide.pdf


Không cần nhiều.

3-5 PDF là đủ.

Viết PDF Reader

Tạo:

src/pdf_loader.py

from pypdf import PdfReader

def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

Test
text = read_pdf("VF8_Manual.pdf")

print(text[:1000])


Mục tiêu:

PDF đọc được.

BƯỚC 2 - Chunking

Đây là bước quan trọng nhất.

Tại sao cần chunk?

Ví dụ:

Manual 300 trang


Không thể đưa hết vào LLM.

Phải chia nhỏ.

Tạo chunker
src/chunker.py

def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

Test
chunks = chunk_text(text)

print(len(chunks))

print(chunks[0])

Kết quả
VF8 Manual

Chunk 1
Chunk 2
Chunk 3
...
Chunk 200

BƯỚC 3 - Metadata

Chưa AI gì cả.

Chỉ quản lý dữ liệu cho đúng.

Tạo cấu trúc:

{
    "doc_name":"VF8_Manual.pdf",
    "chunk_id":1,
    "text":"..."
}


Ví dụ:

records = []

for i, chunk in enumerate(chunks):

    records.append(
        {
            "doc_name": pdf_name,
            "chunk_id": i,
            "text": chunk,
        }
    )


Mục tiêu:

Có một Knowledge Base.

1000 chunks


được lưu trong memory.

BƯỚC 4 - BM25 Search

Bắt đầu Retrieval.

Tạo:

src/bm25_search.py

Tokenize
tokenized_docs = [
    doc.split()
    for doc in documents
]

Build BM25
from rank_bm25 import BM25Okapi

bm25 = BM25Okapi(tokenized_docs)

Search
query = "VF8 battery"

scores = bm25.get_scores(
    query.split()
)

Top K
import numpy as np

top_idx = np.argsort(scores)[::-1][:5]


In kết quả:

for idx in top_idx:
    print(documents[idx])

Milestone 1

Bạn đã có:

Question
↓
BM25
↓
Top 5 Chunks


Đây đã là một Retrieval System.

BƯỚC 5 - Embedding

Nâng cấp sang Semantic Search.

Tạo

src/embedder.py

Load model
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

Encode
embeddings = model.encode(
    documents,
    show_progress_bar=True
)


Kiểm tra:

print(
    embeddings.shape
)


Ví dụ:

(1000,384)


Nghĩa là:

1000 chunks

mỗi chunk
↓
vector 384 chiều

BƯỚC 6 - Semantic Search

Encode câu hỏi:

query_embedding = model.encode(
    [query]
)


Similarity

from sklearn.metrics.pairwise import cosine_similarity

scores = cosine_similarity(
    query_embedding,
    embeddings
)


Top K

top_indices = scores[0].argsort()[::-1][:5]


In kết quả

for idx in top_indices:
    print(documents[idx])

Milestone 2

Hệ thống hiểu:

Pin VF8


và

Battery VF8


là gần nghĩa.

BƯỚC 7 - FAISS

Hiện tại:

1 query
vs
1000 chunks


Tạm ổn.

Nhưng:

100000 chunks


sẽ chậm.

Build Vector DB
import faiss

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)


Add Vector

index.add(
    embeddings.astype("float32")
)


Search

D, I = index.search(
    query_embedding.astype("float32"),
    5
)


Kết quả

Top 5 chunks


nhanh hơn rất nhiều.

BƯỚC 8 - Hybrid Search

Mức enterprise.

Lấy:

bm25_results


và

vector_results


Merge score

final_score = (
    0.4 * bm25_score
    +
    0.6 * vector_score
)


Sort lại.

Workflow:

Question
↓
BM25

Question
↓
Semantic Search

↓
Merge

↓
Top 5


Đây chính là tư duy của Azure AI Search.

BƯỚC 9 - Tích hợp LLM

Bây giờ mới dùng GPT.

Prompt:

prompt = f"""
Answer only based on the context.

Context:
{context}

Question:
{question}
"""


Workflow:

Question

↓

Retriever

↓

Top Chunks

↓

GPT

↓

Answer


Ví dụ:

Question:
VF8 dùng loại pin gì?


Retriever trả:

Chunk 15
Chunk 18
Chunk 22


GPT đọc các chunk đó và trả lời.

BƯỚC 10 - Citation

Rất quan trọng ở doanh nghiệp.

Lưu metadata:

{
    "source":"VF8_Manual.pdf",
    "page":25,
    "chunk_id":18
}


Khi trả lời:

VF8 sử dụng pin Lithium-ion.

Nguồn:
VF8_Manual.pdf
Trang 25

BƯỚC 11 - Tạo Chat UI

Dùng Streamlit.

streamlit run app.py


UI đơn giản:

----------------------
VinFast Knowledge Bot
----------------------

Question:
[______________]

Answer:

...

BƯỚC 12 - Phiên bản giống dự án thật ở VinFast

Sau khi hoàn thành bản local:

Thay thế:

FAISS
↓
Azure AI Search


và

OpenAI API
↓
Azure OpenAI


Kiến trúc sẽ thành:

PDF Documents
        ↓
Chunking
        ↓
Embedding
        ↓
Azure AI Search
        ↓
Hybrid Search
        ↓
Azure OpenAI
        ↓
Answer + Citation

Kế hoạch học thực chiến 14 ngày

Ngày 1-2:

PDF Loader
Chunking

Ngày 3-4:

Metadata
BM25

Ngày 5-6:

Sentence Transformer

Ngày 7-8:

Semantic Search

Ngày 9:

FAISS

Ngày 10:

Hybrid Search

Ngày 11-12:

GPT Integration

Ngày 13:

Citation

Ngày 14:

Streamlit UI

Khi xong ngày 14, bạn sẽ có một dự án RAG end-to-end hoàn chỉnh và đủ mạnh để đưa lên GitHub portfolio hoặc làm nền tảng chuyển sang Azure AI Search/Azure OpenAI trong môi trường doanh nghiệp.