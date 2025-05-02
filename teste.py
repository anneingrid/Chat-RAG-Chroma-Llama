from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
import whisper

# Função para transcrever áudio com Whisper
def transcrever_audio(caminho_audio):
    modelo = whisper.load_model("base")
    resultado = modelo.transcribe(caminho_audio)
    return resultado['text']

# Modelo LLaMA local
llm = LlamaCpp(
    model_path="./modelos/llama-2-7b.Q4_K_M.gguf",
    temperature=0.7,
    max_tokens=512,
    n_ctx=2048,
    verbose=True,
)

# Carrega documentos da web
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()

# Transcreve áudio e adiciona como documento
texto_transcrito = transcrever_audio("audio.mp3")  # <-- substitua pelo seu caminho
documento_audio = Document(page_content=texto_transcrito)
docs.append(documento_audio)

# Divide os documentos
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

# Gera embeddings e indexa com FAISS
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Prompt para reescrever perguntas com contexto
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt para resposta
qa_system_prompt = (
    "Você é um assistente para tarefas de perguntas e respostas. "
    "Use os trechos de contexto recuperados a seguir para responder à pergunta. "
    "Se não souber a resposta, diga que não sabe. Use no máximo três frases "
    "e mantenha a resposta concisa."
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Recuperador com memória
history_aware_retriever = create_history_aware_retriever(
    llm=llm,
    retriever=retriever,
    prompt=contextualize_q_prompt
)

# Cadeia de resposta final (RAG)
rag_chain = create_retrieval_chain(
    retriever=history_aware_retriever,
    combine_docs_chain=qa_prompt | llm | StrOutputParser()
)

# Histórico e perguntas
chat_history = []

while True:
    pergunta = input("\nUsuário: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando a conversa.")
        break

    resposta = rag_chain.invoke({"input": pergunta, "chat_history": chat_history})
    
    print(f"Assistente: {resposta['answer']}")

    chat_history.extend([
        HumanMessage(content=pergunta),
        AIMessage(content=resposta["answer"]),
    ])
