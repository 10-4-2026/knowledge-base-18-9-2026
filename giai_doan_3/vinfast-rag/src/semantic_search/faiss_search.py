# Thư viện FAISS dùng để lưu trữ và tìm kiếm vector hiệu năng cao
import faiss

# Thư viện đọc file JSON
import json

# Thư viện xử lý mảng số học
import numpy as np

# Hàm tự viết để biến văn bản thành embedding vector
from embedding_generator import encode


# Đọc dữ liệu từ file corpus.json
corpus = json.load(
    open(
        "../../data/processed/corpus.json",
        encoding="utf-8"
    )
)

# Lấy riêng phần text từ từng document
texts = [x["text"] for x in corpus]


# Chuyển toàn bộ văn bản thành vector embedding
# Kết quả thường có dạng:
# (số document, số chiều embedding)
embeddings = encode(texts)


# Lấy số chiều của vector embedding
# Ví dụ:
# shape = (1000, 384)
# dimension = 384
dimension = embeddings.shape[1]


# Tạo FAISS index sử dụng Inner Product
# Mỗi vector có dimension chiều
index = faiss.IndexFlatIP(
    dimension
)


# Thêm toàn bộ embedding vào FAISS index
index.add(
    np.array(
        embeddings,
        dtype=np.float32
    )
)


# Hàm tìm kiếm
def search(query):

    # Chuyển câu query thành embedding
    q = encode([query])

    # Tìm 5 vector gần nhất
    scores, idx = index.search(
        np.array(q, dtype=np.float32),
        5
    )

    # Trả về document
    return [corpus[i] for i in idx[0]]