# Base de Conhecimento

## Dados Utilizados

Para este projeto, estamos utilizando dados mockados disponíveis na pasta `data/` para alimentar nosso agente financeiro. O foco inicial é a análise personalizada do perfil e histórico do cliente.

| Arquivo | Formato | Descrição | Utilização no Agente |
|---------|---------|-----------|---------------------|
| `transacoes.csv` | CSV | Histórico de transações do cliente | Análise de padrões de gastos, frequência de uso, categorização de despesas |
| `historico_atendimento.csv` | CSV | Histórico de atendimentos anteriores | Identificação de demandas recorrentes, preferências de canais, análise de satisfação |
| `perfil_investidor.json` | JSON | Perfil e preferências do cliente | Definição do perfil de risco, objetivos financeiros, recomendações personalizadas |
| `produtos_financeiros.json` | JSON | Produtos e serviços disponíveis | Catálogo de ofertas, matching com perfil do cliente, sugestão de produtos |

### Fonte dos Dados

Todos os dados são mockados (fictícios) e armazenados localmente na estrutura do projeto:
- **Diretório:** `data/`
- **Formato:** CSV e JSON
- **Criação:** Dados gerados para fins de demonstração e testes
- **Atualização:** Estática (dados fixos para desenvolvimento e validação)

### Estrutura Local dos Dados

---

## Adaptações nos Dados

### Mudanças em relação ao projeto original

| Aspecto | Original | Adaptação |
|---------|----------|-----------|
| **Fonte de dados** | Dados reais do Yahoo Finance | Dados mockados (fictícios) |
| **Formato** | Parquet | CSV e JSON |
| **Escopo** | Dados de mercado (ações, finanças) | Dados do cliente (gastos, perfil, atendimentos) |
| **Atualização** | Dinâmico (atualizado via script) | Estático (gerado uma única vez) |
| **Complexidade** | Alta (dados financeiros reais) | Moderada (dados simulados) |
| **Dependências** | DuckDB, Hugging Face | Pandas, JSON nativo |

### Por que essas mudanças?

1. **Simplicidade:** Dados mockados facilitam testes e desenvolvimento inicial, permitindo foco na lógica do agente
2. **Privacidade:** Não utiliza dados reais de clientes ou mercado, evitando questões de compliance
3. **Agilidade:** Permite criar cenários controlados para validação de diferentes perfis e situações
4. **Foco no Agente:** Concentra o desenvolvimento na lógica do agente, não na captura e processamento de dados
5. **Reprodutibilidade:** Qualquer pessoa pode executar o projeto sem necessidade de acessar APIs externas
6. **Flexibilidade:** Facilita a criação de casos de teste e validação de diferentes cenários

---

## Estratégia de Integração

### Como os dados são carregados?

Os dados são carregados usando bibliotecas Python padrão para leitura de arquivos locais:

```python
# Exemplo de carregamento de dados
import pandas as pd
import json
import os

# Definir caminho base
DATA_PATH = 'data/'

# Carregar CSV
transacoes = pd.read_csv(os.path.join(DATA_PATH, 'transacoes.csv'))
historico = pd.read_csv(os.path.join(DATA_PATH, 'historico_atendimento.csv'))

# Carregar JSON
with open(os.path.join(DATA_PATH, 'perfil_investidor.json'), 'r', encoding='utf-8') as f:
    perfil = json.load(f)

with open(os.path.join(DATA_PATH, 'produtos_financeiros.json'), 'r', encoding='utf-8') as f:
    produtos = json.load(f)

# Visualizar dados
print(f"Transações: {len(transacoes)} registros")
print(f"Atendimentos: {len(historico)} registros")
print(f"Perfil: {perfil['nome']} - {perfil['perfil_risco']}")
print(f"Produtos disponíveis: {len(produtos)} itens")

````
projeto/
├── data/
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   └── produtos_financeiros.json
├── src/
│   ├── agent.py          # Lógica principal do agente
│   ├── data_loader.py    # Funções para carregar dados
│   ├── analyzer.py       # Análises e cálculos
│   └── utils.py          # Funções auxiliares
├── notebooks/
│   └── analise_dados.ipynb
├── tests/
│   └── test_agent.py
└── README.md
