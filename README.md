# RAG Langchain com PG Vector 

Este projeto é a resolução do primeiro desafio técico do MBA em Engenharia de Sofware com I.A da FullCycle.

O objetivo é realizar o embedding de um documento em PDF e depois realizar consultas no banco de dados vetorial PG Vector.

## Tecnologias utilizadas

- Linguagem: Python
- Framework: Langchain
- Banco de dados: Postgres + Extenção PG Vector
- Execução do banco de dados: Docker & Docker Compose
## Como executar

Abaixo listo um passo a passo de como executar este projeto da melhor maneira no seu ambiente local

### 1 - Ambiente

Antes de executar o projeto precisamos configurar o ambiente. Certifique de ter o docker e o python instalado.
No momento estou usando o python 3.10.12

Após instalar, configure um ambiente virtual para o python, basta executar o comando `python3 -m venv venv`.

Para ativar o ambiente virtual, execute o comando `source venv/bin/activate` na raiz do projeto.

Após executar este comando, já estará no ambiente python isolado usado o venv.

Depois certifique de criar o arquivo `.env` com base no `.env.example` e preencher todas as variáveis.

### 2 - Subir o container do banco de dados
Basta dar um docker compose up e vai subir o banco de dados com as configurações do `docker-compose.yml`

Para testar a conexão, use seu banco de dados de preferencia, no meu caso usei dbeaver com as seguintes configurações
![!\[\[dbeaver rag challenge.png\]\]](assets/image.png)

### 3 - Execução do Ingest dos Documentos
Para executar o script de ingest dos documentos, usando o comando `python3 src/ingest.py`.

Se ocorrer tudo certo, vai exibir a mensagem :
> EMBEDDING FINISHED WITH SUCCESS


### 4 - Executando o chat

Após o ingest, basta executar o script chat.py que o mesmo abrir um terminal interativo que ira ficar recebendo e respondendo as perguntas que você fizer, sobre o documento.

Ex de interações no CLI

```
Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

Perguntas fora do contexto:

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

### Ordem de execução dos scripts 

Ordem de execução
Subir o banco de dados:

<pre>
docker compose up -d

Executar ingestão do PDF:

<pre>
python src/ingest.py

Rodar o chat:

<pre>
python src/chat.py



