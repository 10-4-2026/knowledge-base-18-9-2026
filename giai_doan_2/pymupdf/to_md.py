import pymupdf

doc = pymupdf.open("../pdfplumber/report.pdf")

content = []

for page_num, page in enumerate(doc):

    text = page.get_text()

    content.append(
        f"# Page {page_num+1}\n\n{text}"
    )

markdown = "\n\n".join(content)

with open(
    "manual.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(markdown)