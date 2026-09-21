# defaultdict là một kiểu dictionary đặc biệt
# Khi truy cập một key chưa tồn tại, nó tự động tạo giá trị mặc định
from collections import defaultdict

# Tạo inverted index
# Mỗi key là một từ
# Mỗi value là một tập hợp (set) các document chứa từ đó
index = defaultdict(set)


# Hàm xây dựng inverted index từ corpus
def build(corpus):

    # enumerate() trả về:
    # (0, corpus[0])
    # (1, corpus[1])
    # ...
    # doc_id là số thứ tự của document
    for doc_id, text in enumerate(corpus):

        # Tách văn bản thành các từ
        for token in text.split():

            # Chuyển từ về chữ thường
            # Sau đó thêm doc_id vào tập hợp của từ đó
            index[token.lower()].add(doc_id)


# Hàm tìm kiếm một từ trong inverted index
def lookup(word):

    # Chuyển từ cần tìm về chữ thường
    # Trả về tập hợp các document chứa từ đó
    return index[word.lower()]