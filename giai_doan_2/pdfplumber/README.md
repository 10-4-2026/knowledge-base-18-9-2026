Nếu bạn đang làm AI/document processing, pdfplumber là một trong những thư viện Python tốt nhất để trích xuất text, table và vị trí (layout) từ PDF. Nó được xây dựng trên pdfminer.six và đặc biệt hữu ích khi xử lý hóa đơn, hợp đồng, báo cáo tài chính, tài liệu kỹ thuật,...

1. Cài đặt
pip install pdfplumber


Kiểm tra:

import pdfplumber

print(pdfplumber.__version__)

2. Đọc text đơn giản từ PDF

Giả sử có file:

report.pdf

Đọc toàn bộ text
import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)


Output:

Company Report

Revenue: 100000
Profit: 25000

3. Đọc từng trang

Nhiều khi PDF có hàng trăm trang.

import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    print("Số trang:", len(pdf.pages))

    page1 = pdf.pages[0]

    print(page1.extract_text())

4. Trích xuất từng dòng
with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]

    text = page.extract_text()

    lines = text.split("\n")

    for line in lines:
        print(line)


Output:

Company Report
Revenue: 100000
Profit: 25000

5. Lấy từng từ và tọa độ

Đây là tính năng rất mạnh của pdfplumber.

import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]

    words = page.extract_words()

    for word in words[:5]:
        print(word)


Output:

{
 'text': 'Company',
 'x0': 72.0,
 'x1': 120.0,
 'top': 50.0,
 'bottom': 62.0
}


Có thể dùng để:

Highlight text
Layout analysis
OCR post-processing
RAG theo vùng tài liệu
6. Tìm kiếm keyword trong PDF

Ví dụ tìm "Revenue".

with pdfplumber.open("report.pdf") as pdf:

    for page_num, page in enumerate(pdf.pages):

        words = page.extract_words()

        for w in words:
            if "Revenue" in w["text"]:
                print(
                    f"Page {page_num+1}",
                    w
                )


Output:

Page 1
{
 'text': 'Revenue',
 'x0': 100.2,
 'top': 200
}

7. Trích xuất bảng (Table Extraction)

Giả sử PDF có bảng:

Year	Revenue	Profit2023	100	20
2024	150	35
Cách đơn giản nhất
with pdfplumber.open("table.pdf") as pdf:

    page = pdf.pages[0]

    table = page.extract_table()

    print(table)


Output:

[
 ['Year', 'Revenue', 'Profit'],
 ['2023', '100', '20'],
 ['2024', '150', '35']
]

Chuyển sang Pandas
import pandas as pd

df = pd.DataFrame(
    table[1:],
    columns=table[0]
)

print(df)


Output:

   Year Revenue Profit
0  2023     100     20
1  2024     150     35

8. Trích xuất nhiều bảng
with pdfplumber.open("report.pdf") as pdf:

    page = pdf.pages[0]

    tables = page.extract_tables()

    print("Số bảng:", len(tables))

    for table in tables:
        print(table)

9. Chuyển toàn bộ PDF Table sang Excel
import pdfplumber
import pandas as pd

all_tables = []

with pdfplumber.open("report.pdf") as pdf:

    for page in pdf.pages:

        tables = page.extract_tables()

        for table in tables:

            df = pd.DataFrame(
                table[1:],
                columns=table[0]
            )

            all_tables.append(df)

writer = pd.ExcelWriter("output.xlsx")

for i, df in enumerate(all_tables):
    df.to_excel(
        writer,
        sheet_name=f"Table_{i+1}",
        index=False
    )

writer.close()

10. Crop một vùng PDF trước khi đọc

Giả sử chỉ muốn đọc phần header.

with pdfplumber.open("report.pdf") as pdf:

    page = pdf.pages[0]

    crop = page.crop(
        (
            0,
            0,
            page.width,
            100
        )
    )

    print(crop.extract_text())


Ý nghĩa:

(x0, top, x1, bottom)

11. Đọc Invoice

Ví dụ hóa đơn:

Invoice No: INV001
Date: 2025-01-01
Total Amount: $5000

Trích xuất bằng Regex
import re
import pdfplumber

with pdfplumber.open("invoice.pdf") as pdf:

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

invoice_no = re.search(
    r"Invoice No:\s*(\S+)",
    text
)

amount = re.search(
    r"Total Amount:\s*\$?([\d,.]+)",
    text
)

print(invoice_no.group(1))
print(amount.group(1))


Output:

INV001
5000

12. Trích xuất Metadata
with pdfplumber.open("report.pdf") as pdf:

    print(pdf.metadata)


Output:

{
 'Author': 'Long',
 'Title': 'Financial Report'
}

13. Xem cấu trúc đối tượng PDF

Để debug:

with pdfplumber.open("report.pdf") as pdf:

    page = pdf.pages[0]

    print(page.objects.keys())


Output:

dict_keys([
    'char',
    'line',
    'rect',
    'curve'
])

14. Lấy từng ký tự (Character Level)
with pdfplumber.open("report.pdf") as pdf:

    page = pdf.pages[0]

    chars = page.chars

    print(chars[:3])


Output:

[
 {'text':'C'},
 {'text':'o'},
 {'text':'m'}
]


Rất hữu ích khi:

Layout analysis
OCR correction
Building Document AI
15. Trường hợp thực tế cho AI/RAG

Một pipeline phổ biến:

import pdfplumber

documents = []

with pdfplumber.open("manual.pdf") as pdf:

    for page_num, page in enumerate(pdf.pages):

        text = page.extract_text()

        documents.append({
            "page": page_num + 1,
            "content": text
        })


Sau đó:

documents

[
 {
   "page":1,
   "content":"..."
 },
 {
   "page":2,
   "content":"..."
 }
]


Đưa vào:

LangChain
LlamaIndex
Azure AI Search
RAG Pipeline
16. Kết hợp pdfplumber + OCR cho PDF scan

Lưu ý:

✅ pdfplumber rất mạnh với PDF chứa text thật.

❌ Không hiệu quả với PDF scan (mỗi trang là ảnh).

Ví dụ:

text = page.extract_text()

if text is None:
    print("PDF scan")


Khi đó nên kết hợp:

pdfplumber
    ↓
Page image
    ↓
Tesseract
hoặc
Azure Document Intelligence
    ↓
Structured Data

Ví dụ hoàn chỉnh: Đọc PDF và xuất JSON
import pdfplumber
import json

result = []

with pdfplumber.open("report.pdf") as pdf:

    for page_num, page in enumerate(pdf.pages):

        text = page.extract_text()

        result.append({
            "page": page_num + 1,
            "content": text
        })

with open(
    "output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )


Output:

[
  {
    "page": 1,
    "content": "Company Report ..."
  },
  {
    "page": 2,
    "content": "Financial Data ..."
  }
]


Lời khuyên cho công việc AI tại VinFast: nếu anh đang xây dựng các pipeline Document AI/RAG, hãy dùng:

pdfplumber để lấy text + tọa độ.
Azure Document Intelligence khi PDF có form phức tạp hoặc scan.
pdfplumber + LangChain để chia chunk theo trang và giữ metadata (page, bbox, section).
pdfplumber.extract_tables() để lấy bảng trước khi embedding, tránh mất cấu trúc dữ liệu.