# 🤖 Bia - Assistente Financeira Personalizada

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-0.1.6-green.svg)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Sobre o Projeto

**Bia** é uma assistente financeira personalizada que analisa o perfil, histórico de transações e atendimentos do cliente para oferecer recomendações personalizadas de produtos financeiros, insights sobre padrões de comportamento e sugestões alinhadas aos objetivos financeiros.

O projeto foi desenvolvido como parte do **DIO Lab - Bia do Futuro**, utilizando dados mockados para demonstração e testes.

---

## 🎯 Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 📊 **Visão Geral** | Resumo completo da situação financeira com métricas e gráficos |
| 💰 **Transações** | Análise detalhada com filtros por tipo e categoria |
| 📝 **Atendimentos** | Histórico e estatísticas de atendimentos |
| 🎯 **Recomendações** | Sugestão de produtos financeiros personalizados |
| 💡 **Insights** | Análises personalizadas com sugestões acionáveis |
| 💬 **Chat com IA** | Conversa com a Bia usando Ollama (LLM local) |

---

## 🧠 Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3.8+** | Linguagem principal |
| **Streamlit** | Interface interativa e dashboards |
| **Pandas** | Manipulação e análise de dados |
| **Plotly** | Visualizações interativas |
| **Ollama** | LLM local para respostas inteligentes |
| **Llama 3.1** | Modelo de linguagem (8B parâmetros) |

---
## LINK DO VIDEO:
https://drive.google.com/file/d/1BBCx5n0zqa87jwi2GSxwZZvQ13Z4p1a2/view?usp=drive_link
## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Git (opcional)
- Ollama (para o chat com IA - opcional)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/almeidamobius/Desafio-DIO-agente-de-IA-financeiro.git
cd Desafio-DIO-agente-de-IA-financeiro

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Instalar e configurar Ollama (opcional - para chat com IA)
# Baixe em: https://ollama.com/download
ollama pull llama3.1:8b

# 6. Executar a aplicação
streamlit run src/app.py
