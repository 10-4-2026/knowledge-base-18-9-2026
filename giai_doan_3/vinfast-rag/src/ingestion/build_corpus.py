import json
import os

from pdf_loader import extract_text
from chunker import chunk_text

DATA_DIR = "../../docs"

all_chunks = []

for file in os.listdir(DATA_DIR):

    if file.endswith(".pdf"):

        text = extract_text(
            os.path.join(DATA_DIR, file)
        )

        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):

            all_chunks.append({
                "doc": file,
                "chunk_id": idx,
                "text": chunk
            })

with open(
    "../../data/processed/corpus.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )