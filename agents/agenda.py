from langchain.tools import Tool

def adicionar_evento(query: str):
    return f'📅 O evento "{query}" foi adicionado à agenda.'

def listar_eventos(query: str):
    return "📆 Aqui estão seus próximos eventos: ... (exemplo fictício)"

agente_agenda = [
    Tool(name="Gerenciador de Agenda", func=adicionar_evento, description="Adiciona eventos à sua agenda."),
    Tool(name="Consultor de Agenda", func=listar_eventos, description="Lista seus compromissos.")
]
