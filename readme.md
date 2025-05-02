# Projeto de Perguntas com RAG usando FastAPI + Ollama

Este projeto é uma aplicação de perguntas e respostas com suporte a RAG, utilizando:

- **FastAPI** como backend  
- **Ollama** como servidor local de LLM  
- **Modelo LLM usado:** `gemma:2b`

---

## ✅ Pré-requisitos

- Python 3.10+  
- Ollama instalado ([https://ollama.com](https://ollama.com))  
- Modelo `gemma:2b` baixado via `ollama`  

---

## 🔧 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/anneingrid/Chat-RAG-Chroma-Llama.git
cd Chat-RAG-Chroma-Llama
```

---

## 🚀 Backend (FastAPI)

### 2. Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o indexador

Antes de iniciar a API, rode o script de indexação dos dados:

```bash
python indexador.py
```

### 5. Iniciar o servidor FastAPI

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

---

## 🤖 Iniciar o servidor LLM com Ollama

### 6. Rodar o modelo `gemma:2b` no Ollama

```bash
ollama run gemma:2b
```

(O Ollama iniciará o servidor do modelo em segundo plano automaticamente.)

---

## 🔄 Fluxo da Aplicação

1. Usuário envia uma pergunta.
2. O FastAPI recebe a requisição em `/perguntar?q=...`.
3. O backend utiliza RAG para buscar contexto relevante e envia para o modelo via Ollama.
4. O modelo gera a resposta e ela é retornada ao usuário.

---

## 🧪 Teste Rápido

```bash
curl "http://localhost:8000/perguntar?q=O que é fotossíntese?"
```
