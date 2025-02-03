from datetime import datetime, timedelta
from config.settings import executar_query

def determinar_intervalo(periodo: str) -> datetime:
    hoje = datetime.now()
    if periodo == "semanal":
        return hoje - timedelta(weeks=1)
    elif periodo == "quinzenal":
        return hoje - timedelta(days=15)
    elif periodo == "mensal":
        return hoje - timedelta(days=30)
    elif periodo == "trimestral":
        return hoje - timedelta(days=90)
    else:
        raise ValueError("Período inválido. Use 'semanal', 'quinzenal', 'mensal' ou 'trimestral'.")

# Registra um novo gasto com valor, categoria, sub-categoria e descrição.
def registrar_gasto(valor: float, categoria: str, sub_categoria: str = "", descricao: str = "", data: datetime = None) -> str:
    # Validação dos dados
    if valor <= 0:
        return "O valor do gasto deve ser maior que zero."
    
    if not categoria or len(categoria.strip()) == 0:
        return "Categoria inválida. Por favor, insira uma categoria válida."
    
    if descricao and len(descricao.strip()) > 500:
        return "A descrição do gasto é muito longa. O limite é 500 caracteres."

    if data is None:
        data = datetime.now()

    query = """
        INSERT INTO gastos (valor, categoria, sub_categoria, descricao, data)
        VALUES (%s, %s, %s, %s, %s)
    """
    erro, _ = executar_query(query, (valor, categoria, sub_categoria, descricao, data))
    if erro:
        return erro
    return f"Gasto de R${valor:.2f} registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}' em {data}."

# Retorna um resumo dos gastos registrados.
def resumo_gastos(periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query = "SELECT COUNT(*), SUM(valor) FROM gastos WHERE data >= %s"
    erro, result = executar_query(query, (data_inicio,))
    if erro:
        return erro
    total_gastos, valor_total = result[0]
    return f"Total de gastos: {total_gastos}, Valor total gasto: R${valor_total:.2f} no período {periodo}."

# Define um orçamento para uma categoria e sub-categoria.
def definir_orcamento(categoria: str, limite: float, sub_categoria: str = "", data_inicio: datetime = None, data_fim: datetime = None) -> str:
    if limite <= 0:
        return "O limite do orçamento deve ser maior que zero."
    if not categoria:
        return "Categoria inválida. Por favor, insira uma categoria válida."

    query = """
        INSERT INTO orcamentos (categoria, sub_categoria, limite, data_inicio, data_fim)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (categoria, sub_categoria) DO UPDATE SET limite = EXCLUDED.limite, data_inicio = EXCLUDED.data_inicio, data_fim = EXCLUDED.data_fim
    """
    erro, _ = executar_query(query, (categoria, sub_categoria, limite, data_inicio, data_fim))
    if erro:
        return erro
    return f"Orçamento de {limite} definido para a categoria '{categoria}' e sub-categoria '{sub_categoria}' de {data_inicio} a {data_fim}."

# Analisa os gastos de uma categoria e sub-categoria em relação ao orçamento definido.
def analisar_gastos(categoria: str, sub_categoria: str = "", periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query_limite = "SELECT limite FROM orcamentos WHERE categoria = %s AND sub_categoria = %s"
    erro, result = executar_query(query_limite, (categoria, sub_categoria))
    if erro:
        return erro
    if not result:
        return f"Nenhum orçamento definido para a categoria '{categoria}' e sub-categoria '{sub_categoria}'."
    
    limite = result[0][0]
    query_gastos = "SELECT SUM(valor) FROM gastos WHERE categoria = %s AND sub_categoria = %s AND data >= %s"
    erro, result = executar_query(query_gastos, (categoria, sub_categoria, data_inicio))
    if erro:
        return erro
    total_gastos = result[0][0] or 0

    if total_gastos > limite:
        return f"Você excedeu o orçamento de {limite} em '{categoria}' e sub-categoria '{sub_categoria}' no período {periodo}. Total gasto: {total_gastos}."
    return f"Você está dentro do orçamento de '{categoria}' e sub-categoria '{sub_categoria}' no período {periodo}. Total gasto: {total_gastos}, Limite: {limite}."

# Gera um relatório com o total gasto em cada categoria e sub-categoria.
def relatorio_gastos(periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query = """
        SELECT categoria, sub_categoria, SUM(valor)
        FROM gastos
        WHERE data >= %s
        GROUP BY categoria, sub_categoria
    """
    erro, result = executar_query(query, (data_inicio,))
    if erro:
        return erro
    if not result:
        return "Nenhum gasto registrado para gerar o relatório."
    
    relatorio_formatado = "\n".join([f"{categoria} - {sub_categoria}: {valor}" for categoria, sub_categoria, valor in result])
    return relatorio_formatado

# Verifica se o total gasto em uma categoria e sub-categoria ultrapassou o limite definido.
def alerta_excesso_gasto(categoria: str, sub_categoria: str, total_gasto: float, limite: float) -> str:
    if total_gasto > limite:
        return f"Atenção: Você ultrapassou o orçamento de {categoria} e sub-categoria {sub_categoria}!"
    return "Sem alertas."

# Registra uma nova receita com valor.
def registrar_receita(valor: float, data: datetime = None) -> str:
    if data is None:
        data = datetime.now()

    query = "INSERT INTO receitas (valor, data) VALUES (%s, %s)"
    erro, _ = executar_query(query, (valor, data))
    if erro:
        return erro
    return f"Receita de {valor} registrada em {data}."

# Retorna um resumo das receitas registradas.
def total_gastos_categoria(categoria: str, sub_categoria: str = "", periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query = "SELECT SUM(valor) FROM gastos WHERE categoria = %s AND sub_categoria = %s AND data >= %s"
    erro, result = executar_query(query, (categoria, sub_categoria, data_inicio))
    if erro:
        return erro
    total_gasto = result[0][0] or 0
    return f"Total de gastos em {categoria} e sub-categoria {sub_categoria} no período {periodo}: {total_gasto}."

# Compara os gastos totais de dois meses.
def comparar_gastos_periodo(periodo1: str, periodo2: str) -> str:
    try:
        data_inicio1 = determinar_intervalo(periodo1)
        data_inicio2 = determinar_intervalo(periodo2)
    except ValueError as e:
        return str(e)

    query1 = "SELECT SUM(valor) FROM gastos WHERE data >= %s"
    erro, result1 = executar_query(query1, (data_inicio1,))
    if erro:
        return erro
    total_periodo1 = result1[0][0] or 0

    query2 = "SELECT SUM(valor) FROM gastos WHERE data >= %s"
    erro, result2 = executar_query(query2, (data_inicio2,))
    if erro:
        return erro
    total_periodo2 = result2[0][0] or 0

    return f"Gastos no período {periodo1}: {total_periodo1}, Gastos no período {periodo2}: {total_periodo2}."

# Retorna o saldo disponível.
def saldo_disponivel(periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query_receitas = "SELECT SUM(valor) FROM receitas WHERE data >= %s"
    erro, result_receitas = executar_query(query_receitas, (data_inicio,))
    if erro:
        return erro
    total_receitas = result_receitas[0][0] or 0

    query_gastos = "SELECT SUM(valor) FROM gastos WHERE data >= %s"
    erro, result_gastos = executar_query(query_gastos, (data_inicio,))
    if erro:
        return erro
    total_gastos = result_gastos[0][0] or 0

    saldo = total_receitas - total_gastos
    return f"Saldo disponível no período {periodo}: {saldo}."

# Sugere uma redução de gastos em uma categoria e sub-categoria.
def sugerir_reducao_gastos(periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query = "SELECT categoria, sub_categoria, SUM(valor) FROM gastos WHERE data >= %s GROUP BY categoria, sub_categoria ORDER BY SUM(valor) DESC LIMIT 1"
    erro, result = executar_query(query, (data_inicio,))
    if erro:
        return erro
    if result:
        categoria, sub_categoria, valor = result[0]
        return f"Considere reduzir gastos na categoria '{categoria}' e sub-categoria '{sub_categoria}' no período {periodo}, onde você gastou {valor}."
    return "Nenhuma sugestão de redução de gastos disponível."

# Salva um gasto ou receita em uma categoria e sub-categoria.
def salvar_gasto_ou_receita(tipo: str, categoria: str, sub_categoria: str, valor: float, data: datetime = None) -> str:
    if data is None:
        data = datetime.now()

    if tipo == "gasto":
        query = "INSERT INTO gastos (categoria, sub_categoria, valor, data) VALUES (%s, %s, %s, %s)"
    elif tipo == "receita":
        query = "INSERT INTO receitas (categoria, sub_categoria, valor, data) VALUES (%s, %s, %s, %s)"
    else:
        return "Tipo inválido. Use 'gasto' ou 'receita'."

    erro, _ = executar_query(query, (categoria, sub_categoria, valor, data))
    if erro:
        return erro
    return f"{tipo.capitalize()} de {valor} registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}' em {data}."

# Retorna o histórico de gastos em uma categoria e sub-categoria.
def historico_gastos(categoria: str, sub_categoria: str = "", periodo: str = "mensal") -> str:
    try:
        data_inicio = determinar_intervalo(periodo)
    except ValueError as e:
        return str(e)

    query = "SELECT data, valor FROM gastos WHERE categoria = %s AND sub_categoria = %s AND data >= %s ORDER BY data DESC"
    erro, result = executar_query(query, (categoria, sub_categoria, data_inicio))
    if erro:
        return erro
    if not result:
        return f"Nenhum gasto registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}' no período {periodo}."
    
    historico_formatado = "\n".join([f"{data}: {valor}" for data, valor in result])
    return historico_formatado