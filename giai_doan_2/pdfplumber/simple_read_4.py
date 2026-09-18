import pdfplumber
with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]

    text = page.extract_text()

    lines = text.split("\n")

    for line in lines:
        print(line + "--")