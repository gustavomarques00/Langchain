import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.financeiro import agente_financeiro
from agents.agenda import agente_agenda
from agents.trabalho import agente_trabalho
from agents.pesquisa import agente_pesquisa

# Carregar variáveis do .env
load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

# Criar o modelo de IA
modelo = ChatOpenAI(model="gpt-4o-mini", api_key=chave_api)

# Juntar as ferramentas de todos os agentes em uma única lista
todos_os_agentes = agente_financeiro + agente_agenda + agente_trabalho + agente_pesquisa

# Criar o agente orquestrador
agente_orquestrador = initialize_agent(
    tools=todos_os_agentes,
    llm=modelo,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    resposta = agente_orquestrador.run("Adicione um evento na agenda: Reunião com cliente amanhã às 10h.")
    print(resposta)
