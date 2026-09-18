import pymupdf

pdf = pymupdf.open("../pdfplumber/report.pdf")

print(pdf.page_count)


for page in pdf:
    print(page.get_text())


page = pdf[0]

pix = page.get_pixmap()

pix.save("page1.png")

#---------------------------------------
zoom = 3

mat = pymupdf.Matrix(zoom, zoom)

pix = page.get_pixmap(matrix=mat)

pix.save("high_res.png")

pdf.close()