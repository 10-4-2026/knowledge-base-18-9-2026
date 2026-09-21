# Import hàm tính độ tương đồng cosine giữa các vector
from sklearn.metrics.pairwise import cosine_similarity


# Hàm tính điểm tương đồng giữa query và tập document
def score(q, docs):

    # cosine_similarity yêu cầu dữ liệu dạng ma trận 2 chiều
    # q thường là vector 1 chiều có dạng:
    # [0.2, 0.5, 0.1, ...]
    #
    # reshape(1, -1) chuyển thành:
    # [[0.2, 0.5, 0.1, ...]]
    #
    # nghĩa là:
    # 1 hàng, số cột được suy ra tự động
    # Do chỉ có 1 query nên chỉ có 1 hàng
    return cosine_similarity(
        q.reshape(1, -1),  # Query vector
        docs              # Ma trận các document vector
    )[0]                  # Lấy hàng đầu tiên của kết quả, 
