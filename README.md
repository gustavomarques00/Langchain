# Brain Zap

Brain Zap é um projeto que utiliza microserviços conectados ao agente orquestrador usando Langchain. Este README descreve o subagente `financeiro`, que é responsável pelo gerenciamento financeiro, permitindo registrar gastos e receitas, definir orçamentos, analisar gastos e gerar relatórios financeiros. A aplicação utiliza um banco de dados PostgreSQL para armazenar os dados.

## Funcionalidades do Subagente Financeiro

- Registrar gastos com valor, categoria, sub-categoria, descrição e data.
- Registrar receitas com valor e data.
- Definir orçamentos para categorias e sub-categorias com limites e datas de início e fim.
- Analisar gastos em relação aos orçamentos definidos.
- Gerar relatórios de gastos por período (semanal, quinzenal, mensal, trimestral).
- Verificar se os gastos ultrapassaram os limites definidos.
- Comparar gastos entre diferentes períodos.
- Calcular o saldo disponível.
- Sugerir redução de gastos com base nos maiores gastos.

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/financeiro.git
   cd financeiro

2. Crie um ambiente virtual e ative-o:
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

3. Instale as dependências:
    pip install -r requirements.txt

4. Configure as variáveis de ambiente no arquivo .env:
    DB_NAME=seu_banco_de_dados
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_PORT=5432

5. Crie as tabelas no banco de dados PostgreSQL:
    CREATE TABLE gastos (
    id SERIAL PRIMARY KEY,
    valor NUMERIC(10, 2) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    sub_categoria VARCHAR(255),
    descricao VARCHAR(500),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE receitas (
        id SERIAL PRIMARY KEY,
        valor NUMERIC(10, 2) NOT NULL,
        categoria VARCHAR(255),
        sub_categoria VARCHAR(255),
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE orcamentos (
        id SERIAL PRIMARY KEY,
        categoria VARCHAR(255) NOT NULL,
        sub_categoria VARCHAR(255),
        limite NUMERIC(10, 2) NOT NULL,
        data_inicio TIMESTAMP,
        data_fim TIMESTAMP,
        CONSTRAINT orcamentos_categoria_sub_categoria_key UNIQUE (categoria, sub_categoria)
    );

## Uso

- Registrar Gasto
    from financeiro import registrar_gasto

    resultado = registrar_gasto(100.0, "Alimentação", "Restaurantes", "Jantar com amigos")
    print(resultado)

- Registrar Receita
    from financeiro import registrar_receita
    
    resultado = registrar_receita(500.0)
    print(resultado)

- Definir Orçamento
    from financeiro import definir_orcamento
    
    resultado = definir_orcamento("Alimentação", 1000.0, "Restaurantes")
    print(resultado)

- Analisar Gastos
    from financeiro import analisar_gastos
    
    resultado = analisar_gastos("Alimentação", "Restaurantes", "mensal")
    print(resultado)

- Gerar Relatório de Gastos
    from financeiro import relatorio_gastos

    resultado = relatorio_gastos("mensal")
    print(resultado)

- Verificar Saldo Disponível
    from financeiro import saldo_disponivel

    resultado = saldo_disponivel("mensal")
    print(resultado)

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (git checkout -b feature/nova-feature).
3. Commit suas mudanças (git commit -am 'Adiciona nova feature').
4. Faça o push para a branch (git push origin feature/nova-feature).
5. Crie um novo Pull Request.

## licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.