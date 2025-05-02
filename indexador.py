from sentence_transformers import SentenceTransformer
import faiss, os, pickle

modelo_emb = SentenceTransformer('all-MiniLM-L6-v2')

textos, arquivos = [], []
for nome in os.listdir("dados"):
    with open(os.path.join("dados", nome), "r", encoding="utf-8") as f:
        textos.append(f.read())
        arquivos.append(nome)

embeddings = modelo_emb.encode(textos)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "base_faiss/index.faiss")
with open("base_faiss/textos.pkl", "wb") as f:
    pickle.dump(textos, f)
