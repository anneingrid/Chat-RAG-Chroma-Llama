from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")

modelo_emb = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index("base_faiss/index.faiss")

with open("base_faiss/textos.pkl", "rb") as f:
    textos = pickle.load(f)

arquivos = []
for nome in os.listdir("dados"):
    arquivos.append(nome)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/perguntar")
async def perguntar(q: str):
    query_embedding = modelo_emb.encode([q])
    k = 3
    distances, indices = index.search(query_embedding, k)
    
    contexto = ""
    references = []
    
    for i, idx in enumerate(indices[0]):
        if idx < len(textos) and idx >= 0:
            contexto += f"\nDocumento {i+1} ({arquivos[idx]}):\n{textos[idx]}\n"
            references.append(f"{arquivos[idx]}")
    
    # Construir prompt com o contexto
    prompt = f"""Com base APENAS nas informações abaixo, responda à pergunta do usuário.
Se a informação não estiver no contexto, responda que não tem informação suficiente.
Inclua referências aos documentos utilizados no formato (nome_do_arquivo).

Contexto:
{contexto}

Pergunta: {q}

Resposta:"""

    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False,
        "max_tokens": 500
    }

    async with httpx.AsyncClient(timeout=200) as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            resposta = response.json().get("response", "Não consegui responder.")
        except httpx.RequestError as e:
            resposta = f"Erro ao fazer requisição: {str(e)}"
        except httpx.HTTPStatusError as e:
            resposta = f"Erro de status HTTP: {str(e)}"
        except Exception as e:
            resposta = f"Erro inesperado: {str(e)}"

    return {"response": resposta, "references": references}