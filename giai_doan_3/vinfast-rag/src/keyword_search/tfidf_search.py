'''
Tóm tắt ngắn gọn

Đây là một hệ thống Semantic Search đơn giản dựa trên TF-IDF + Cosine Similarity:

Đọc tập văn bản (corpus.json).
Chuyển toàn bộ văn bản thành vector TF-IDF.
Khi người dùng nhập câu hỏi:
Vector hóa câu hỏi.
Tính độ tương đồng cosine với mọi tài liệu.
Sắp xếp theo độ tương đồng giảm dần.
Trả về top_k tài liệu phù hợp nhất.

Độ phức tạp mỗi lần tìm kiếm là khoảng O(N x D) với:

N: số lượng văn bản.
D: số chiều của vector TF-IDF (số từ vựng).
'''

# Thư viện dùng để đọc và xử lý dữ liệu JSON
import json 

# TF-IDF dùng để chuyển văn bản thành vector số
from sklearn.feature_extraction.text import TfidfVectorizer 

# Hàm tính độ tương đồng cosine giữa các vector
from sklearn.metrics.pairwise import cosine_similarity


# Đọc file corpus.json và chuyển nội dung JSON thành đối tượng Python
corpus = json.load(
    open(
        "../../data/processed/corpus.json",  # Đường dẫn tới file dữ liệu
        "r",                                # Mở file ở chế độ đọc (read)
        encoding="utf-8"                    # Sử dụng mã hóa UTF-8 để hỗ trợ tiếng Việt
    )
)

# Lấy toàn bộ text từ corpus
# Giả sử mỗi phần tử trong corpus có dạng:
# {"id": 1, "text": "Xin chào"}
texts = [c["text"] for c in corpus]


# Khởi tạo mô hình TF-IDF
vectorizer = TfidfVectorizer()

# Học từ vựng (fit) và chuyển toàn bộ văn bản thành ma trận TF-IDF (transform)
# Kết quả X là ma trận có kích thước:
# (số văn bản, số từ vựng)
X = vectorizer.fit_transform(texts)


# Hàm tìm kiếm văn bản tương tự
def search(query, top_k=5):

    # Chuyển câu truy vấn thành vector TF-IDF
    # Sử dụng cùng vocabulary đã học ở trên
    q = vectorizer.transform([query])

    # Tính cosine similarity giữa query và tất cả văn bản trong corpus
    # Kết quả là một mảng điểm tương đồng
    scores = cosine_similarity(q, X)[0]

    # Sắp xếp chỉ số các văn bản theo điểm giảm dần
    # argsort() mặc định tăng dần nên dùng [::-1] để đảo ngược
    ranked = scores.argsort()[::-1]

    # Trả về top_k văn bản có độ tương đồng cao nhất
    return [
        corpus[i] for i in ranked[:top_k]
    ]