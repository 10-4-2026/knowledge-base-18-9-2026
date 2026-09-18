import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    print("Số trang:", len(pdf.pages))
    page1 = pdf.pages[0]
    print(page1.extract_text())