# Guia de configuração e execução dos scripts

Este guia fornece instruções detalhadas sobre como configurar o ambiente e executar os scripts `main1.py` e `main2.py`.

## Requisitos do Sistema

- **Sistema Operacional**: Windows, macOS ou Linux
- **Python**: Versão 3.10 ou 3.11 ([Referência](https://github.com/chroma-core/chroma/issues/163?utm_source=chatgpt.com))
- **pip**: Versão 20.2.4 ou superior

## Passos para Configuração

### 1. Verifique a Versão do Python e do pip

Certifique-se de que o Python e o `pip` estão instalados e em versões compatíveis.

```bash
python --version
pip --version
```

Se a versão do Python for 3.12 ou superior, é recomendável fazer o downgrade para a versão 3.11 ou 3.10.

### 2. Crie e Ative um Ambiente Virtual

  - #### Windows:

```bash
python -m venv env
env\Scripts\activate
```

  - #### Linux/macOS:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativo, instale as bibliotecas necessárias listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

**Nota**: A versão `0.3.21` do ChromaDB é recomendada para compatibilidade com Python 3.10 e 3.11.

### 4. Baixe e Configure o Modelo Llama

Os scripts utilizam o modelo Llama para geração de linguagem. Você pode baixar o modelo Llama 2 7B no formato GGUF no link abaixo:

- [Llama 2 7B GGUF](https://huggingface.co/TheBloke/Llama-2-7B-GGUF)

Após o download, extraia o conteúdo para o diretório `./models/llama-2-7b.Q4_K_M.gguf`.

Se estiver usando linux, apenas cole no terminal:
```bash
mkdir -p models
cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf
```

### 5. Execute os Scripts

Após concluir os passos anteriores, você pode executar os scripts `main1.py` e `main2.py` conforme necessário.
O script `main1.py`, apresenta as perguntas pré-definidas. No `main2.py` a pergunta é feita pelo usuário.

- #### Windows:

  ```bash
  python main1.py
  ```
  
  ou
  
  ```bash
  python main2.py
  ```

- #### Linux/macOS:

  ```bash
  python3 main1.py
  ```
  
  ou
  
  ```bash
  python3 main2.py
  ```

Certifique-se de que os scripts estão no mesmo diretório do ambiente virtual ou ajuste os caminhos conforme necessário.

## Possíveis Problemas e Soluções

- **Erro ao instalar o ChromaDB**: Se encontrar erros ao instalar o ChromaDB, verifique se está utilizando uma versão compatível do Python (3.10 ou 3.11). ([Referência](https://github.com/chroma-core/chroma/issues/163?utm_source=chatgpt.com))

- **Erro ao carregar o modelo Llama**: Certifique-se de que o caminho para o modelo está correto e que o arquivo `llama-2-7b.Q4_K_M.gguf` está no formato adequado.

## Referências

- Documentação do ChromaDB: [https://docs.trychroma.com/](https://docs.trychroma.com/)
- Repositório do Llama: [https://github.com/facebookresearch/llama](https://github.com/facebookresearch/llama)

Seguindo este guia, você deverá ser capaz de configurar e executar os scripts `main1.py` e `main2.py` corretamente. Se encontrar problemas adicionais, consulte a documentação das bibliotecas utilizadas ou procure ajuda nas comunidades relacionadas.
