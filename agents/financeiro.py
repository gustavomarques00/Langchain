from langchain.tools import Tool
from config.settings import executar_query

def registrar_gasto(valor: float, categoria: str, sub_categoria: str = "", descricao: str = "") -> str:
    # Validação dos dados
    if valor <= 0:
        return "O valor do gasto deve ser maior que zero."
    
    if not categoria or len(categoria.strip()) == 0:
        return "Categoria inválida. Por favor, insira uma categoria válida."
    
    if descricao and len(descricao.strip()) > 500:
        return "A descrição do gasto é muito longa. O limite é 500 caracteres."

    query = """
        INSERT INTO gastos (valor, categoria, sub_categoria, descricao)
        VALUES (%s, %s, %s, %s)
    """
    erro, _ = executar_query(query, (valor, categoria, sub_categoria, descricao))
    if erro:
        return erro
    return f"Gasto de R${valor:.2f} registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}'."

def resumo_gastos() -> str:
    query = """
        SELECT COUNT(*), SUM(valor) FROM gastos
    """
    erro, result = executar_query(query)
    if erro:
        return erro
    total_gastos, valor_total = result[0]
    return f"Total de gastos: {total_gastos}, Valor total gasto: R${valor_total:.2f}"

def definir_orcamento(categoria: str, limite: float, sub_categoria: str = "") -> str:
    if limite <= 0:
        return "O limite do orçamento deve ser maior que zero."
    if not categoria:
        return "Categoria inválida. Por favor, insira uma categoria válida."

    query = """
        INSERT INTO orcamentos (categoria, sub_categoria, limite)
        VALUES (%s, %s, %s)
        ON CONFLICT (categoria, sub_categoria) DO UPDATE SET limite = EXCLUDED.limite
    """
    erro, _ = executar_query(query, (categoria, sub_categoria, limite))
    if erro:
        return erro
    return f"Orçamento de {limite} definido para a categoria '{categoria}' e sub-categoria '{sub_categoria}'."

def analisar_gastos(categoria: str, sub_categoria: str = "") -> str:
    query_limite = "SELECT limite FROM orcamentos WHERE categoria = %s AND sub_categoria = %s"
    erro, result = executar_query(query_limite, (categoria, sub_categoria))
    if erro:
        return erro
    if not result:
        return f"Nenhum orçamento definido para a categoria '{categoria}' e sub-categoria '{sub_categoria}'."
    
    limite = result[0][0]
    query_gastos = "SELECT SUM(valor) FROM gastos WHERE categoria = %s AND sub_categoria = %s"
    erro, result = executar_query(query_gastos, (categoria, sub_categoria))
    if erro:
        return erro
    total_gastos = result[0][0] or 0

    if total_gastos > limite:
        return f"Você excedeu o orçamento de {limite} em '{categoria}' e sub-categoria '{sub_categoria}'. Total gasto: {total_gastos}."
    return f"Você está dentro do orçamento de '{categoria}' e sub-categoria '{sub_categoria}'. Total gasto: {total_gastos}, Limite: {limite}."

def relatorio_gastos() -> str:
    query = "SELECT categoria, sub_categoria, SUM(valor) FROM gastos GROUP BY categoria, sub_categoria"
    erro, result = executar_query(query)
    if erro:
        return erro
    if not result:
        return "Nenhum gasto registrado para gerar o relatório."
    
    relatorio_formatado = "\n".join([f"{categoria} - {sub_categoria}: {valor}" for categoria, sub_categoria, valor in result])
    return relatorio_formatado

def alerta_excesso_gasto(categoria: str, sub_categoria: str, total_gasto: float, limite: float) -> str:
    if total_gasto > limite:
        return f"Atenção: Você ultrapassou o orçamento de {categoria} e sub-categoria {sub_categoria}!"
    return "Sem alertas."

def registrar_receita(valor: float) -> str:
    query = "INSERT INTO receitas (valor) VALUES (%s)"
    erro, _ = executar_query(query, (valor,))
    if erro:
        return erro
    return f"Receita de {valor} registrada."

def total_gastos_categoria(categoria: str, sub_categoria: str = "") -> str:
    query = "SELECT SUM(valor) FROM gastos WHERE categoria = %s AND sub_categoria = %s"
    erro, result = executar_query(query, (categoria, sub_categoria))
    if erro:
        return erro
    total_gasto = result[0][0] or 0
    return f"Total de gastos em {categoria} e sub-categoria {sub_categoria}: {total_gasto}."

def comparar_gastos_mes(mes1: str, mes2: str) -> str:
    query = "SELECT SUM(valor) FROM gastos WHERE strftime('%Y-%m', data) = %s"
    erro, result1 = executar_query(query, (mes1,))
    if erro:
        return erro
    total_mes1 = result1[0][0] or 0

    erro, result2 = executar_query(query, (mes2,))
    if erro:
        return erro
    total_mes2 = result2[0][0] or 0

    return f"Gastos em {mes1}: {total_mes1}, Gastos em {mes2}: {total_mes2}."

def saldo_disponivel() -> str:
    query_receitas = "SELECT SUM(valor) FROM receitas"
    erro, result_receitas = executar_query(query_receitas)
    if erro:
        return erro
    total_receitas = result_receitas[0][0] or 0

    query_gastos = "SELECT SUM(valor) FROM gastos"
    erro, result_gastos = executar_query(query_gastos)
    if erro:
        return erro
    total_gastos = result_gastos[0][0] or 0

    saldo = total_receitas - total_gastos
    return f"Saldo disponível: {saldo}."

def sugerir_reducao_gastos() -> str:
    query = "SELECT categoria, sub_categoria, SUM(valor) FROM gastos GROUP BY categoria, sub_categoria ORDER BY SUM(valor) DESC LIMIT 1"
    erro, result = executar_query(query)
    if erro:
        return erro
    if result:
        categoria, sub_categoria, valor = result[0]
        return f"Considere reduzir gastos na categoria '{categoria}' e sub-categoria '{sub_categoria}', onde você gastou {valor}."
    return "Nenhuma sugestão de redução de gastos disponível."

def salvar_gasto_ou_receita(tipo: str, categoria: str, sub_categoria: str, valor: float) -> str:
    if tipo == "gasto":
        query = "INSERT INTO gastos (categoria, sub_categoria, valor) VALUES (%s, %s, %s)"
    elif tipo == "receita":
        query = "INSERT INTO receitas (categoria, sub_categoria, valor) VALUES (%s, %s, %s)"
    else:
        return "Tipo inválido. Use 'gasto' ou 'receita'."

    erro, _ = executar_query(query, (categoria, sub_categoria, valor))
    if erro:
        return erro
    return f"{tipo.capitalize()} de {valor} registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}'."

def historico_gastos(categoria: str, sub_categoria: str = "") -> str:
    query = "SELECT data, valor FROM gastos WHERE categoria = %s AND sub_categoria = %s ORDER BY data DESC"
    erro, result = executar_query(query, (categoria, sub_categoria))
    if erro:
        return erro
    if not result:
        return f"Nenhum gasto registrado na categoria '{categoria}' e sub-categoria '{sub_categoria}'."
    
    historico_formatado = "\n".join([f"{data}: {valor}" for data, valor in result])
    return historico_formatado