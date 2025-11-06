import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_similar_documents

load_dotenv()

required_environment = [
    "OPENAI_API_KEY",
    "OPENAI_CHAT_MODEL",
]

for key in required_environment:
    if not os.getenv(key):
        raise RuntimeError(f"Environment variable {key} is not set")
    
llm = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano"),
    temperature=0.3
)

SYSTEM_PROMPT = """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def format_context_from_results(results):
    """Formata os resultados da busca em um contexto concatenado"""
    if not results:
        return "Nenhum contexto relevante encontrado."
    
    context_parts = []

    for i, (doc, score) in enumerate(results, start=1):
        context_parts.append(f"[Documento {i} - Score: {score:.2f}]\n{doc.page_content.strip()}")
    
    return "\n\n".join(context_parts)

def chat(question: str) -> str:
    """Processa uma pergunta e retorna a resposta baseada no contexto."""

    results = search_similar_documents(question, k=10)

    context = format_context_from_results(results)

    prompt = SYSTEM_PROMPT.format(context=context, question=question)

    response = llm.invoke(prompt)

    return str(response.content)

def main():
    """Loop principal do chat"""
    print("="*60)
    print("RAG CHAT - Façã sua pergunta ou Digite 'sair' para encerrar")
    print("="*60)
    print()

    while True:
        try:
            question = input("Você: ").strip()

            if not question:
                continue

            if question.lower() == 'sair':
                print("\nEncerrando o chat. Até breve!")
                break

            print("\nAssistente: ", end="")
            answer = chat(question)
            print(answer)
            print("\n" + "-"*60 + "\n")

        except KeyboardInterrupt:
            print("\n\nEncerrando chat. Até logo!")
            break
        except Exception as e:
            print("f\nErro ao processar pergunta: {e}\n")

if __name__ == "__main__":
    main()
