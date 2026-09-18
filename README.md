# knowledge-base-18-9-2026

Dựa trên mô tả dự án, đây không đơn thuần là một chatbot mà là một Enterprise Knowledge Base Platform phục vụ Robot Q&A Bot của VinFast/Vingroup. Người tham gia dự án cần hiểu cả quy trình dữ liệu, AI Retrieval, vận hành sản phẩm và đánh giá chất lượng tri thức.

1. Hiểu bức tranh tổng thể của hệ thống

Kiến trúc dự án có thể hình dung như sau:

                KNOWLEDGE BASE

     Documents / Policies / Manuals / FAQs
                        │
                        ▼
                  01. INGEST
                        │
                        ▼
                  02. CLEAN
                        │
                        ▼
              03. QUALITY CONTROL
                        │
                        ▼
                 Knowledge Store
                        │
                        ▼
              Retrieval Capability
                        │
                        ▼
                Robot Q&A Bot
                        │
                        ▼
       Answers + Sources + References


Mục tiêu cuối cùng:

User asks question
        ↓
System finds relevant knowledge
        ↓
Generate answer
        ↓
Provide answer with source references

2. Lộ trình học tập theo 4 cấp độ
Giai đoạn 1: Foundation (2-3 tuần)
Mục tiêu

Hiểu Knowledge Base là gì và dữ liệu vận hành như thế nào.

Kiến thức cần học
Data Fundamentals
Structured Data
Semi-Structured Data
Unstructured Data

Ví dụ:

Excel          → Structured
JSON           → Semi-Structured
PDF/Word/PPT   → Unstructured

Knowledge Management
Knowledge Base
FAQ System
Enterprise Search
Metadata
Taxonomy
Version Control
Document Lifecycle
Create
 ↓
Review
 ↓
Publish
 ↓
Update
 ↓
Archive

Kết quả đầu ra

Phải trả lời được:

Knowledge Base khác Database thế nào?
Tại sao tài liệu cũ gây lỗi cho chatbot?
Metadata dùng để làm gì?
3. Giai đoạn 2: Ingest & Clean Data (3-4 tuần)

Đây là phần sát với bước:

01. INGEST
02. CLEAN

2.1 Data Ingestion
Học cách lấy dữ liệu từ
PDF
Word
Excel
SharePoint
Confluence
Website
Internal Wiki
Công cụ

Python:

pandas
pdfplumber
pymupdf
beautifulsoup

2.2 Data Cleaning

Các loại lỗi phổ biến:

Duplicate Content
Policy A
Policy B

Nội dung trùng lặp 95%

Broken Content
Mất định dạng
Mất bảng
Lỗi OCR

Outdated Content
Policy 2023
Policy 2026


Bot có thể lấy nhầm nội dung cũ.

Missing Metadata

Ví dụ thiếu:

Owner
Version
Published Date
Department

Đóng góp được cho dự án
Làm pipeline làm sạch dữ liệu
Loại bỏ duplicate documents
Chuẩn hóa metadata
4. Giai đoạn 3: Retrieval System (4-6 tuần)

Đây là phần quan trọng nhất.

Tương ứng:

Knowledge Base
      ↓
Retrieval Capability
      ↓
Q&A Bot

3.1 Information Retrieval
Keyword Search

Hiểu:

TF-IDF
BM25
Inverted Index

Workflow:

Question
 ↓
Keyword Search
 ↓
Top Documents

3.2 Semantic Search
Embedding

Biến văn bản thành vector.

Ví dụ:

"Pin xe VF8"

↓

[0.234, 0.781, ...]

Similarity Search
Cosine Similarity
Nearest Neighbor Search
3.3 Vector Database

Nên học:

Cơ bản
FAISS
Qdrant
Enterprise
Azure AI Search

Đặc biệt nếu hướng VinFast:

Azure AI Search
=
Ưu tiên số 1

3.4 RAG Architecture

RAG là nền tảng của các Q&A Bot hiện đại.

Question
    ↓
Retriever
    ↓
Relevant Documents
    ↓
LLM
    ↓
Answer with Citation


Hiểu các khái niệm:

Chunking
Document
     ↓
Chunks

Top-K Retrieval
Top 3
Top 5
Top 10

Hybrid Search
BM25
+
Vector Search

5. Giai đoạn 4: Quality Control (4 tuần)

Tương ứng:

03. QUALITY CONTROL


Đây là phần được nhấn mạnh trong mô tả dự án.

4.1 Data Quality

Các vấn đề thực tế:

Duplicated Knowledge

Một thông tin tồn tại ở nhiều nơi.

Source Conflict

Ví dụ:

HR Policy:
WFH 2 ngày

Department Guideline:
WFH 3 ngày


Bot phải tin nguồn nào?

4.2 Knowledge Governance

Hiểu:

Source Authority
Official Policy
    >
Department Portal
    >
Email
    >
Chat

Version Ranking
2026 Version
    >
2025 Version
    >
2024 Version

4.3 Data Validation

Kiểm tra:

Nguồn còn hiệu lực?
Nội dung có bị trùng?
Metadata đầy đủ?
Có mâu thuẫn không?
Đóng góp được
Thiết kế rule kiểm tra dữ liệu
Phát hiện tài liệu mâu thuẫn
Xây dashboard chất lượng dữ liệu
6. Giai đoạn 5: Measure Answer Quality (3-4 tuần)

Đây là yêu cầu trực tiếp trong JD:

Measure answer quality

5.1 Retrieval Evaluation

Đánh giá hệ thống tìm kiếm.

Recall@K
Tài liệu đúng có xuất hiện trong Top K không?

Precision@K
Top K có bao nhiêu tài liệu đúng?

MRR

Đánh giá thứ hạng tài liệu đúng.

5.2 Answer Evaluation

Đánh giá câu trả lời.

Accuracy

Trả lời đúng hay sai?

Relevance

Có đúng câu hỏi không?

Completeness

Có đủ ý không?

Groundedness

Có dựa trên nguồn không?

Citation Quality

Nguồn tham chiếu có chính xác không?

5.3 User Feedback

Theo dõi:

👍 Helpful
👎 Not Helpful


Từ đó cải thiện Knowledge Base.

7. Giai đoạn 6: Product Operation (Liên tục)

Đúng với mô tả:

Operate, maintain and optimise a live product

Monitoring

Theo dõi:

Hệ thống
Query Volume
Latency
Error Rate
Bot
Answer Rate
Fallback Rate
Satisfaction Rate
Incident Handling

Ví dụ:

Bot trả lời sai
↓
Xác định nguồn dữ liệu
↓
Sửa Knowledge Base
↓
Re-index
↓
Deploy

8. Tech Stack nên học
Bắt buộc
Python
Pandas
Regex
FastAPI
Database
SQL
PostgreSQL
Search
Azure AI Search
Elasticsearch (nên biết)
AI
Embedding
RAG
Prompt Engineering
Framework
LangChain
LlamaIndex
Evaluation
Ragas
DeepEval
Dashboard
Power BI
Grafana
Roadmap 3 Tháng Cho Dự Án Này
Tháng 1: Data & Knowledge
Knowledge Management
Document Processing
Data Ingestion
Data Cleaning
Metadata

Tháng 2: Retrieval
Information Retrieval
BM25
Embedding
Vector Search
Azure AI Search
RAG

Tháng 3: Quality & Operation
Data Quality
Source Conflict
Evaluation Metrics
Ragas
Monitoring
Product Operation

Năng lực quan trọng nhất để thành công trong dự án

Xếp theo mức độ ưu tiên:

1. Data Quality & Governance     ⭐⭐⭐⭐⭐
2. Information Retrieval         ⭐⭐⭐⭐⭐
3. RAG & Citation                ⭐⭐⭐⭐⭐
4. Answer Evaluation             ⭐⭐⭐⭐⭐
5. Product Operation             ⭐⭐⭐⭐
6. Azure AI Search               ⭐⭐⭐⭐
7. LangChain/LlamaIndex          ⭐⭐⭐⭐
8. Agentic AI                    ⭐⭐⭐


Nếu mục tiêu của anh Long là tham gia dự án này trong team AI của VinFast, tôi khuyến nghị tập trung 70% thời gian vào Data Quality + Retrieval + Evaluation, vì đây chính là 3 năng lực cốt lõi được thể hiện trực tiếp trong mô tả dự án hơn là việc xây chatbot hay fine-tune LLM.
