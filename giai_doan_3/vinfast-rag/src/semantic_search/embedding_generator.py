from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

def encode(texts):

    return model.encode(
        texts,
        normalize_embeddings=True
    )