import chromadb
from llama_cpp import Llama
import os
import whisper

def transcreve_audio(audioEnviado):
    model = whisper.load_model("turbo")
    audio = whisper.load_audio(audioEnviado)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    return(result.text)

def setup_chroma():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    collection = chroma_client.get_or_create_collection("rag_collection")
    return collection

def read_documents_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        documents = content.split("\n")
        documents = [doc.strip() for doc in documents if doc.strip()]
    return documents

def add_documents(collection, texts):
    for i, text in enumerate(texts):
        collection.add(documents=[text], ids=[str(i)])

def retrieve_documents(collection, query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0] if results["documents"] else []

def load_llm():
    model_path = "./models/llama-2-7b-chat.Q2_K.gguf"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Baixe um modelo GGUF compatível e coloque na pasta ./models")
    return Llama(model_path=model_path, n_threads=4, device="cpu")

def generate_response(llm, context, query):
    prompt = f"""Use as informações abaixo para responder:
    {context}
    Pergunta: {query}
    Resposta:"""
    
    output = llm(prompt, max_tokens=200)
    return output["choices"][0]["text"].strip()

if __name__ == "__main__":
    collection = setup_chroma()

    txt_file_path = "./audio.mp3" 
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"Arquivo {txt_file_path} não encontrado.")
    
    documents = [transcreve_audio("audio.mp3")]
    print(documents)
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
