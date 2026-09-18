import pdfplumber
import pprint

with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]

    words = page.extract_words()

    for word in words[:5]:
        print(word)

    print(pdf.metadata)
    
    print('------------')
    chars = page.chars
    pprint.pprint(chars[:3])