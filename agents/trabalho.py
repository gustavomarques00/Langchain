from langchain.tools import Tool

def automatizar_tarefa(query: str):
    return f"⚙️ Automatizando tarefa: {query}"

def organizar_projeto(query: str):
    return f"📁 Criando um plano para o projeto: {query}"

agente_trabalho = [
    Tool(name="Automação de Tarefas", func=automatizar_tarefa, description="Automatiza tarefas repetitivas."),
    Tool(name="Gestão de Projetos", func=organizar_projeto, description="Organiza e planeja projetos.")
]
