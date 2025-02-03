from langchain.tools import Tool
from config.settings import conectar_db

def registrar_gasto(valor: float, categoria: str, descricao: str = "") -> str:
    # Validação dos dados
    if valor <= 0:
        return "O valor do gasto deve ser maior que zero."
    
    if not categoria or len(categoria.strip()) == 0:
        return "Categoria inválida. Por favor, insira uma categoria válida."
    
    if descricao and len(descricao.strip()) > 500:
        return "A descrição do gasto é muito longa. O limite é 500 caracteres."

    # Conectar ao banco de dados
    conn = conectar_db()
    if conn is None:
        return "Erro ao conectar ao banco de dados."

    try:
        # Usando uma consulta parametrizada (para prevenir SQL Injection)
        query = """
            INSERT INTO gastos (valor, categoria, descricao)
            VALUES (%s, %s, %s)
        """

        # Preparando os dados para a consulta
        cursor = conn.cursor()
        cursor.execute(query, (valor, categoria, descricao))
        conn.commit()  # Confirmar a transação

        cursor.close()
        return f"Gasto de R${valor:.2f} registrado na categoria '{categoria}'."
    
    except Exception as e:
        print(f"Erro ao registrar gasto: {e}")
        return "Erro ao registrar o gasto."
    
    finally:
        # Fechar a conexão com o banco de dados
        if conn:
            conn.close()

# Função para gerar um resumo dos gastos
def resumo_gastos() -> str:
    # Conectar ao banco de dados
    conn = conectar_db()
    if conn is None:
        return "Erro ao conectar ao banco de dados."

    try:
        # Consultar o número total de gastos e o total de valor dos gastos
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*), SUM(valor) FROM gastos;
        """
        cursor.execute(query)
        resultado = cursor.fetchone()  # Pega o primeiro resultado
        
        cursor.close()

        if resultado[0] == 0:
            return "Nenhum gasto registrado até o momento."

        total_gastos = resultado[1] if resultado[1] else 0
        total_gastos_count = resultado[0]

        return f"Você registrou um total de {total_gastos_count} gastos. Valor total: R${total_gastos:.2f}."

    except Exception as e:
        print(f"Erro ao consultar o resumo dos gastos: {e}")
        return "Erro ao consultar os gastos."
    
    finally:
        # Fechar a conexão com o banco de dados
        if conn:
            conn.close()

# Simulando um banco de dados de orçamentos
orcamentos = {}

def definir_orcamento(categoria: str, limite: float) -> str:
    if limite <= 0:
        return "O limite do orçamento deve ser maior que zero."
    if not categoria:
        return "Categoria inválida. Por favor, insira uma categoria válida."
    
    orcamentos[categoria] = limite
    return f"Orçamento de {limite} definido para a categoria '{categoria}'."

def analisar_gastos(categoria: str) -> str:
    if categoria not in orcamentos:
        return f"Nenhum orçamento definido para a categoria '{categoria}'."
    
    # Filtrando os gastos da categoria
    gastos_categoria = [gasto["valor"] for gasto in gastos_registrados if gasto["categoria"] == categoria]
    total_gastos = sum(gastos_categoria)
    limite = orcamentos[categoria]
    
    if total_gastos > limite:
        return f"Você excedeu o orçamento de {limite} em '{categoria}'. Total gasto: {total_gastos}."
    return f"Você está dentro do orçamento de '{categoria}'. Total gasto: {total_gastos}, Limite: {limite}."


def relatorio_gastos() -> str:
    if not gastos_registrados:
        return "Nenhum gasto registrado para gerar o relatório."
    
    # Agrupando os gastos por categoria
    relatorio = {}
    for gasto in gastos_registrados:
        categoria = gasto["categoria"]
        relatorio[categoria] = relatorio.get(categoria, 0) + gasto["valor"]
    
    # Formatando o relatório
    relatorio_formatado = "\n".join([f"{categoria}: {valor}" for categoria, valor in relatorio.items()])
    return f"Relatório de Gastos:\n{relatorio_formatado}"


def alerta_excesso_gasto(categoria: str, total_gasto: float, limite: float) -> str:
    if total_gasto > limite:
        return f"Atenção: Você ultrapassou o orçamento de {categoria}!"
    return "Sem alertas."

def registrar_receita(valor: float) -> str:
    return f"Receita de {valor} registrada."

def total_gastos_categoria(categoria: str, total_gasto: float) -> str:
    return f"Total de gastos em {categoria}: {total_gasto}."

def comparar_gastos_mes(mes1: str, mes2: str, gasto_mes1: float, gasto_mes2: float) -> str:
    if gasto_mes1 > gasto_mes2:
        return f"Você gastou mais em {mes1} do que em {mes2}."
    elif gasto_mes1 < gasto_mes2:
        return f"Você gastou menos em {mes1} do que em {mes2}."
    return f"Os gastos de {mes1} e {mes2} são iguais."

def saldo_disponivel(limite: float, total_gasto: float) -> str:
    saldo = limite - total_gasto
    return f"Saldo disponível: {saldo}."

def sugerir_reducao_gastos(categoria: str, total_gasto: float, limite: float) -> str:
    if total_gasto > limite * 1.2:  # 20% acima do limite
        return f"Considere reduzir seus gastos em {categoria}."
    return "Gastos dentro do esperado."

def salvar_gasto_ou_receita(tipo: str, valor: float) -> str:
    return f"{tipo.capitalize()} de {valor} salva com sucesso!"

def historico_gastos() -> str:
    return "Histórico de gastos: Gasto 1 - 100, Gasto 2 - 50, Gasto 3 - 20."


agente_financeiro = [
    Tool(name="Rastreador Financeiro", func=rastrear_gastos, description="Registra um gasto financeiro."),
    Tool(name="Analista Financeiro", func=analisar_gastos, description="Analisa padrões de gastos.")
]
