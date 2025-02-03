from langchain.tools import Tool

def responder_pergunta(query: str):
    return f"🔍 Resposta baseada na IA: {query}"

agente_pesquisa = [
    Tool(name="Consultor de IA", func=responder_pergunta, description="Responde perguntas com IA.")
]
