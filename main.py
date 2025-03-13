import chromadb
from llama_cpp import Llama
import os

def setup_chroma():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("rag_collection")
    return collection

def add_documents(collection, texts):
    for i, text in enumerate(texts):
        collection.add(documents=[text], ids=[str(i)])

def retrieve_documents(collection, query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0] if results["documents"] else []

def load_llm():
    model_path = "./models/llama-2-7b.Q4_K_M.gguf"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Baixe um modelo GGUF compatível e coloque na pasta ./models")
    return Llama(model_path=model_path)

def generate_response(llm, context, query):
    prompt = f"""Use as informações abaixo para responder:
    {context}
    Pergunta: {query}
    Resposta:"""
    
    output = llm(prompt, max_tokens=200)
    return output["choices"][0]["text"].strip()

if __name__ == "__main__":
    collection = setup_chroma()
    
    documents = [
        "O céu é azul porque a luz do sol se espalha na atmosfera.",
        "A água ferve a 100 graus Celsius ao nível do mar."
    ]
    add_documents(collection, documents)
    
    llm = load_llm()

    while True:
        query = input("\nDigite sua pergunta (ou 'sair' para encerrar): ").strip()
        if query.lower() == "sair":
            print("Encerrando...")
            break
        
        retrieved_docs = retrieve_documents(collection, query)
        context = "\n".join(retrieved_docs) if retrieved_docs else "Não encontrei informações relevantes."
        
        response = generate_response(llm, context, query)
        print("\nResposta:", response)
