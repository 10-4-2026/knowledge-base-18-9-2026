# Thư viện dùng để đọc file JSON
import json

# Thư viện BM25 dùng cho tìm kiếm từ khóa (keyword search)
from rank_bm25 import BM25Okapi


# Đọc dữ liệu từ file corpus.json
# Kết quả là một danh sách các document
corpus = json.load(
    open(
        "src/keyword_search/corpus.json",  # Đường dẫn file
        "r",                               # Mở ở chế độ đọc
        encoding="utf-8"                   # Hỗ trợ tiếng Việt
    )
)

# Tạo danh sách văn bản đã được tokenize
# Mỗi text được tách thành các từ bằng split()
texts = [
    x["text"].split()
    for x in corpus
]

# Ví dụ:
# corpus:
# [
#   {"id":1, "text":"toi hoc ai"},
#   {"id":2, "text":"machine learning la ai"}
# ]
#
# texts sẽ là:
# [
#   ["toi", "hoc", "ai"],
#   ["machine", "learning", "la", "ai"]
# ]


# Xây dựng chỉ mục BM25 từ toàn bộ tập tài liệu
bm25 = BM25Okapi(texts)


# Hàm tìm kiếm
def search(query):

    # Tách query thành danh sách từ
    # Ví dụ:
    # "hoc ai" -> ["hoc", "ai"]
    #
    # Sau đó BM25 tính điểm cho mọi document
    scores = bm25.get_scores(query.split())

    # Tạo danh sách các chỉ số document
    # Ví dụ:
    # [0, 1, 2, 3, ...]
    #
    # Sau đó sắp xếp theo điểm BM25 giảm dần
    top = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:5]

    # Trả về 5 document có điểm cao nhất
    return [
        corpus[i]
        for i in top
    ]