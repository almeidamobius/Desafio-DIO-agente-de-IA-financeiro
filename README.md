# 🤖 Bia - Assistente Financeira Personalizada

## 📋 Sobre o Projeto

A **Bia** é uma assistente financeira personalizada que analisa o perfil, histórico de transações e atendimentos do cliente para oferecer recomendações personalizadas de produtos financeiros, insights sobre padrões de comportamento e sugestões alinhadas aos objetivos financeiros.

### 🎯 Funcionalidades

- 📊 **Análise de Perfil**: Classificação do perfil de investidor (conservador, moderado, arrojado)
- 💰 **Transações**: Análise de padrões de gastos e categorização
- 📝 **Atendimentos**: Histórico e padrões de atendimento
- 🎯 **Recomendações**: Sugestão de produtos financeiros personalizados
- 💡 **Insights**: Análises personalizadas com sugestões acionáveis

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Git (opcional)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/lab-agente-financeiro.git
cd lab-agente-financeiro

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar a aplicação
streamlit run src/app.py

```
##Estrutura do projeto
```
lab-agente-financeiro/
├── data/                    # Dados mockados
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── transacoes.csv
├── docs/                    # Documentação
├── src/                     # Código fonte
│   └── app.py              # Interface Streamlit
├── venv/                    # Ambiente virtual
├── requirements.txt         # Dependências
└── README.md

```
##Dados Utilizados
- historico_atendimento.csv
- perfil_investidor.json
- produtos_financeiros.json
- transacoes.csv
