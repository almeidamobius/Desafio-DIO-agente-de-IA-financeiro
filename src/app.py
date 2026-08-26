import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import re
import ollama  # Importar a biblioteca ollama

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Bia - Assistente Financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SYSTEM PROMPT DA BIA
# ============================================
SYSTEM_PROMPT = """
Você é a Bia, uma assistente financeira personalizada e consultiva especializada em análise de perfil de investidor e recomendações financeiras personalizadas.

Seu objetivo é analisar o perfil, histórico de transações e atendimentos do cliente para oferecer recomendações personalizadas de produtos financeiros, insights sobre padrões de comportamento e sugestões alinhadas aos objetivos financeiros do cliente.

REGRAS OBRIGATÓRIAS:

SEMPRE baseie suas respostas nos dados fornecidos (transacoes.csv, historico_atendimento.csv, perfil_investidor.json, produtos_financeiros.json)

NUNCA invente informações financeiras ou recomendações sem base nos dados

NUNCA faça recomendações de compra/venda de ativos específicos

NUNCA acesse ou peça dados bancários reais ou senhas

Se não tiver dados suficientes para responder, admita e sugira como o cliente pode fornecer mais informações

SEMPRE contextualize as recomendações com base no perfil de risco do cliente

MANTENHA um tom consultivo, empático e profissional

EXPLIQUE conceitos financeiros de forma acessível quando necessário
"""

# ============================================
# CARREGAMENTO DOS DADOS
# ============================================
@st.cache_data
def load_data():
    """Carrega todos os dados da pasta data/"""
    base_path = "data/"
    
    # Carregar transações
    transacoes = pd.read_csv(
        os.path.join(base_path, "transacoes.csv"),
        parse_dates=['data']
    )
    
    # Carregar histórico de atendimentos
    historico = pd.read_csv(
        os.path.join(base_path, "historico_atendimento.csv"),
        parse_dates=['data']
    )
    
    # Carregar perfil do investidor
    with open(os.path.join(base_path, "perfil_investidor.json"), 'r', encoding='utf-8') as f:
        perfil = json.load(f)
    
    # Carregar produtos financeiros
    with open(os.path.join(base_path, "produtos_financeiros.json"), 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    
    return transacoes, historico, perfil, produtos

# ============================================
# FUNÇÕES DE ANÁLISE
# ============================================
def analyze_transactions(transacoes):
    """Analisa as transações do cliente"""
    if transacoes.empty:
        return {}
    
    entradas = transacoes[transacoes['tipo'] == 'entrada']
    saidas = transacoes[transacoes['tipo'] == 'saida']
    
    # Gastos por categoria
    gastos_categoria = saidas.groupby('categoria')['valor'].sum().to_dict()
    
    return {
        "total_entradas": entradas['valor'].sum() if not entradas.empty else 0,
        "total_saidas": saidas['valor'].sum() if not saidas.empty else 0,
        "saldo": entradas['valor'].sum() - saidas['valor'].sum() if not entradas.empty and not saidas.empty else 0,
        "gastos_categoria": gastos_categoria,
        "top_categorias": sorted(gastos_categoria.items(), key=lambda x: x[1], reverse=True)[:3]
    }

def analyze_attendance(historico):
    """Analisa o histórico de atendimentos"""
    if historico.empty:
        return {}
    
    return {
        "total": len(historico),
        "temas": historico['tema'].value_counts().to_dict(),
        "canais": historico['canal'].value_counts().to_dict(),
        "taxa_resolucao": (historico['resolvido'] == 'sim').sum() / len(historico) * 100,
        "ultimo": historico['data'].max()
    }

def recommend_products(perfil, produtos):
    """Recomenda produtos baseados no perfil do cliente"""
    perfil_risco = perfil['perfil_investidor']
    recomendados = []
    
    for produto in produtos:
        if perfil_risco == 'conservador' and produto['risco'] == 'baixo':
            recomendados.append(produto)
        elif perfil_risco == 'moderado' and produto['risco'] in ['baixo', 'medio']:
            recomendados.append(produto)
        elif perfil_risco == 'arrojado':
            recomendados.append(produto)
    
    # Ordenar por risco
    ordem_risco = {'baixo': 0, 'medio': 1, 'alto': 2}
    recomendados.sort(key=lambda x: ordem_risco.get(x['risco'], 3))
    
    return recomendados

def get_insights(transacoes, historico, perfil):
    """Gera insights personalizados"""
    insights = []
    
    # 1. Análise do perfil
    perfil_risco = perfil['perfil_investidor']
    if perfil_risco == 'conservador':
        insights.append("🛡️ **Perfil Conservador:** Você prioriza segurança e liquidez nos investimentos.")
    elif perfil_risco == 'moderado':
        insights.append("⚖️ **Perfil Moderado:** Equilíbrio entre segurança e rentabilidade é ideal para você.")
    else:
        insights.append("🚀 **Perfil Arrojado:** Você busca maior rentabilidade com maior exposição a risco.")
    
    # 2. Análise da reserva de emergência
    reserva_atual = perfil['reserva_emergencia_atual']
    meta_reserva = perfil['metas'][0]['valor_necessario']
    if reserva_atual < meta_reserva:
        faltam = meta_reserva - reserva_atual
        insights.append(f"💰 **Reserva de Emergência:** Faltam R$ {faltam:,.2f} para atingir sua meta de R$ {meta_reserva:,.2f}.")
        
        # Sugestão de aporte mensal
        meses = 6
        aporte = faltam / meses
        insights.append(f"💡 **Sugestão:** Aporte mensal de R$ {aporte:,.2f} por {meses} meses para completar a reserva.")
    else:
        insights.append("🎉 **Reserva de Emergência:** Parabéns! Você já atingiu sua meta!")
    
    # 3. Análise de gastos
    if not transacoes.empty:
        saidas = transacoes[transacoes['tipo'] == 'saida']
        if not saidas.empty:
            total_gastos = saidas['valor'].sum()
            
            # Maior gasto
            maior_gasto = saidas.loc[saidas['valor'].idxmax()]
            insights.append(f"📉 **Maior Gasto:** R$ {maior_gasto['valor']:,.2f} em {maior_gasto['categoria']}.")
            
            # Categoria com mais gastos
            gastos_categoria = saidas.groupby('categoria')['valor'].sum()
            top_categoria = gastos_categoria.idxmax()
            top_valor = gastos_categoria.max()
            pct = (top_valor / total_gastos) * 100
            insights.append(f"📊 **Categoria Principal:** {top_categoria} representa {pct:.1f}% dos seus gastos.")
    
    # 4. Análise de atendimentos
    if not historico.empty:
        temas_comuns = historico['tema'].value_counts()
        tema_mais_comum = temas_comuns.index[0]
        insights.append(f"💬 **Atendimentos:** Você já teve {len(historico)} atendimentos, com foco em {tema_mais_comum}.")
        
        taxa_resolucao = (historico['resolvido'] == 'sim').sum() / len(historico) * 100
        if taxa_resolucao == 100:
            insights.append("✅ **Resolução:** Todos os seus atendimentos foram resolvidos com sucesso!")
        else:
            insights.append(f"📋 **Resolução:** {taxa_resolucao:.0f}% dos atendimentos foram resolvidos.")
    
    return insights

# ============================================
# FUNÇÃO PARA PERGUNTAR AO OLLAMA
# ============================================
def perguntar(pergunta, perfil, analise_transacoes, analise_atendimentos):
    """
    Função que envia a pergunta para o Ollama e retorna a resposta
    
    Args:
        pergunta: String com a pergunta do usuário
        perfil: Dict com dados do perfil
        analise_transacoes: Dict com análise de transações
        analise_atendimentos: Dict com análise de atendimentos
    
    Returns:
        String com a resposta do Ollama
    """
    
    # Construir contexto com os dados do cliente
    contexto = f"""
Contexto dos dados do cliente:

PERFIL DO INVESTIDOR:
- Nome: {perfil['nome']}
- Idade: {perfil['idade']} anos
- Profissão: {perfil['profissao']}
- Perfil de Investidor: {perfil['perfil_investidor']}
- Objetivo Principal: {perfil['objetivo_principal']}
- Patrimônio Total: R$ {perfil['patrimonio_total']:,.2f}
- Renda Mensal: R$ {perfil['renda_mensal']:,.2f}
- Reserva de Emergência: R$ {perfil['reserva_emergencia_atual']:,.2f}

METAS:
"""
    for meta in perfil['metas']:
        contexto += f"- {meta['meta']}: R$ {meta['valor_necessario']:,.2f} (Prazo: {meta['prazo']})\n"
    
    contexto += f"""
GASTOS:
- Total de Entradas: R$ {analise_transacoes.get('total_entradas', 0):,.2f}
- Total de Saídas: R$ {analise_transacoes.get('total_saidas', 0):,.2f}
- Saldo: R$ {analise_transacoes.get('saldo', 0):,.2f}
- Top 3 Gastos: 
"""
    for categoria, valor in analise_transacoes.get('top_categorias', []):
        contexto += f"  - {categoria}: R$ {valor:,.2f}\n"
    
    contexto += f"""
ATENDIMENTOS:
- Total: {analise_atendimentos.get('total', 0)}
- Taxa de Resolução: {analise_atendimentos.get('taxa_resolucao', 0):.0f}%
- Temas: {', '.join(list(analise_atendimentos.get('temas', {}).keys())[:3])}

Pergunta do cliente: {pergunta}

Por favor, responda de forma consultiva, profissional e baseada nos dados fornecidos. Use o System Prompt fornecido.
"""
    
    try:
        # Chamar o Ollama
        response = ollama.chat(
            model='llama3.1:8b',
            messages=[
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT
                },
                {
                    'role': 'user',
                    'content': contexto
                }
            ],
            options={
                'temperature': 0.7,
                'num_predict': 500
            }
        )
        
        return response['message']['content']
        
    except Exception as e:
        print(f"Erro ao chamar Ollama: {e}")
        return None

# ============================================
# FUNÇÃO PARA GERAR RESPOSTA PRÉ-DEFINIDA (FALLBACK)
# ============================================
def generate_bia_response(pergunta, transacoes, historico, perfil, produtos):
    """Gera resposta pré-definida (fallback quando Ollama não está disponível)"""
    # ... (código já existente) ...
    return "Desculpe, não consegui processar sua pergunta. Tente novamente mais tarde."

# ============================================
# CARREGAR DADOS
# ============================================
try:
    transacoes, historico, perfil, produtos = load_data()
    
    # Análises
    analise_transacoes = analyze_transactions(transacoes)
    analise_atendimentos = analyze_attendance(historico)
    produtos_recomendados = recommend_products(perfil, produtos)
    insights = get_insights(transacoes, historico, perfil)
    
except Exception as e:
    st.error(f"❌ Erro ao carregar os dados: {e}")
    st.stop()

# ============================================
# SIDEBAR - INFORMAÇÕES DO CLIENTE
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/woman.png", width=80)
    st.title(f"👤 {perfil['nome']}")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Idade", f"{perfil['idade']} anos")
    with col2:
        st.metric("Perfil", perfil['perfil_investidor'].upper())
    
    st.write(f"**Profissão:** {perfil['profissao']}")
    st.write(f"**Renda Mensal:** R$ {perfil['renda_mensal']:,.2f}")
    st.write(f"**Patrimônio:** R$ {perfil['patrimonio_total']:,.2f}")
    
    st.markdown("---")
    st.subheader("🎯 Metas")
    for meta in perfil['metas']:
        with st.expander(meta['meta']):
            st.write(f"**Valor:** R$ {meta['valor_necessario']:,.2f}")
            st.write(f"**Prazo:** {meta['prazo']}")
            progresso = (perfil['reserva_emergencia_atual'] / meta['valor_necessario']) * 100
            st.progress(min(progresso/100, 1.0))
            st.caption(f"Progresso: {min(progresso, 100):.1f}%")
    
    st.markdown("---")
    st.caption("💡 Dica: Navegue pelas abas para mais detalhes")

# ============================================
# TABS PRINCIPAIS
# ============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Visão Geral",
    "💰 Transações",
    "📝 Atendimentos",
    "🎯 Recomendações",
    "💡 Insights Detalhados",
    "💬 Conversar com a Bia"
])

# ============================================
# TAB 1: VISÃO GERAL
# ============================================
with tab1:
    st.header("📊 Visão Geral da Situação Financeira")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Saldo do Mês",
            f"R$ {analise_transacoes.get('saldo', 0):,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "📈 Total de Entradas",
            f"R$ {analise_transacoes.get('total_entradas', 0):,.2f}"
        )
    
    with col3:
        st.metric(
            "📉 Total de Saídas",
            f"R$ {analise_transacoes.get('total_saidas', 0):,.2f}"
        )
    
    with col4:
        st.metric(
            "📞 Atendimentos",
            analise_atendimentos.get('total', 0)
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Distribuição de Gastos")
        if analise_transacoes.get('gastos_categoria'):
            gastos = analise_transacoes['gastos_categoria']
            df_gastos = pd.DataFrame({
                'Categoria': list(gastos.keys()),
                'Valor': list(gastos.values())
            })
            
            fig = px.pie(
                df_gastos,
                values='Valor',
                names='Categoria',
                title='Gastos por Categoria',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Nenhum gasto registrado no período")
    
    with col2:
        st.subheader("📈 Top 3 Gastos")
        for categoria, valor in analise_transacoes.get('top_categorias', []):
            st.metric(
                categoria,
                f"R$ {valor:,.2f}",
                delta=f"{(valor / analise_transacoes.get('total_saidas', 1)) * 100:.1f}% do total"
            )
    
    st.markdown("---")
    
    # Insights rápidos
    st.subheader("💡 Insights Rápidos")
    for insight in insights[:3]:
        st.info(insight)
    
    # Últimas transações
    st.markdown("---")
    st.subheader("🔄 Últimas Transações")
    ultimas = transacoes.sort_values('data', ascending=False).head(5)
    st.dataframe(
        ultimas.style.format({
            'data': lambda x: x.strftime('%d/%m/%Y'),
            'valor': lambda x: f'R$ {x:,.2f}'
        }),
        width='stretch',
        hide_index=True
    )

# ============================================
# TAB 2: TRANSAÇÕES
# ============================================
with tab2:
    st.header("💰 Análise de Transações")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tipos = st.multiselect(
            "Filtrar por Tipo",
            options=['entrada', 'saida'],
            default=['entrada', 'saida']
        )
    
    with col2:
        categorias_disponiveis = transacoes['categoria'].unique().tolist()
        categorias = st.multiselect(
            "Filtrar por Categoria",
            options=categorias_disponiveis,
            default=categorias_disponiveis
        )
    
    with col3:
        data_filtro = st.date_input(
            "Período",
            value=(transacoes['data'].min(), transacoes['data'].max()),
            min_value=transacoes['data'].min(),
            max_value=transacoes['data'].max()
        )
    
    # Aplicar filtros
    df_filtrado = transacoes.copy()
    if tipos:
        df_filtrado = df_filtrado[df_filtrado['tipo'].isin(tipos)]
    if categorias:
        df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias)]
    if len(data_filtro) == 2:
        df_filtrado = df_filtrado[
            (df_filtrado['data'] >= pd.to_datetime(data_filtro[0])) &
            (df_filtrado['data'] <= pd.to_datetime(data_filtro[1]))
        ]
    
    # Métricas filtradas
    col1, col2, col3 = st.columns(3)
    with col1:
        entradas_filtradas = df_filtrado[df_filtrado['tipo'] == 'entrada']['valor'].sum()
        st.metric("Entradas", f"R$ {entradas_filtradas:,.2f}")
    with col2:
        saidas_filtradas = df_filtrado[df_filtrado['tipo'] == 'saida']['valor'].sum()
        st.metric("Saídas", f"R$ {saidas_filtradas:,.2f}")
    with col3:
        saldo_filtrado = entradas_filtradas - saidas_filtradas
        st.metric("Saldo", f"R$ {saldo_filtrado:,.2f}")
    
    # Tabela de transações
    st.markdown("---")
    st.subheader("📋 Histórico de Transações")
    st.dataframe(
        df_filtrado.sort_values('data', ascending=False).style.format({
            'data': lambda x: x.strftime('%d/%m/%Y'),
            'valor': lambda x: f'R$ {x:,.2f}'
        }),
        width='stretch',
        hide_index=True
    )
    
    # Gráfico de evolução
    if not df_filtrado.empty:
        st.markdown("---")
        st.subheader("📈 Evolução dos Gastos")
        
        df_evolucao = df_filtrado[df_filtrado['tipo'] == 'saida'].groupby('data')['valor'].sum().reset_index()
        df_evolucao['acumulado'] = df_evolucao['valor'].cumsum()
        
        fig = px.line(
            df_evolucao,
            x='data',
            y='acumulado',
            title='Evolução Acumulada dos Gastos',
            labels={'data': 'Data', 'acumulado': 'Total Gasto (R$)'}
        )
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Total Gasto (R$)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, width='stretch')

# ============================================
# TAB 3: ATENDIMENTOS
# ============================================
with tab3:
    st.header("📝 Histórico de Atendimentos")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total de Atendimentos",
            analise_atendimentos.get('total', 0)
        )
    
    with col2:
        st.metric(
            "Taxa de Resolução",
            f"{analise_atendimentos.get('taxa_resolucao', 0):.0f}%"
        )
    
    with col3:
        ultimo = analise_atendimentos.get('ultimo')
        if ultimo:
            st.metric(
                "Último Atendimento",
                ultimo.strftime('%d/%m/%Y')
            )
    
    st.markdown("---")
    
    # Tabela de atendimentos
    st.subheader("📋 Lista de Atendimentos")
    st.dataframe(
        historico.sort_values('data', ascending=False).style.format({
            'data': lambda x: x.strftime('%d/%m/%Y')
        }),
        width='stretch',
        hide_index=True
    )
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Temas de Atendimento")
        temas = analise_atendimentos.get('temas', {})
        if temas:
            df_temas = pd.DataFrame({
                'Tema': list(temas.keys()),
                'Quantidade': list(temas.values())
            })
            fig = px.bar(
                df_temas,
                x='Tema',
                y='Quantidade',
                title='Distribuição por Tema',
                color='Quantidade',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("📱 Canais Utilizados")
        canais = analise_atendimentos.get('canais', {})
        if canais:
            df_canais = pd.DataFrame({
                'Canal': list(canais.keys()),
                'Quantidade': list(canais.values())
            })
            fig = px.pie(
                df_canais,
                values='Quantidade',
                names='Canal',
                title='Distribuição por Canal',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, width='stretch')

# ============================================
# TAB 4: RECOMENDAÇÕES
# ============================================
with tab4:
    st.header("🎯 Recomendações Personalizadas")
    
    st.info(f"📊 **Perfil Identificado:** {perfil['perfil_investidor'].upper()} - Recomendações baseadas no seu perfil de risco")
    
    st.markdown("---")
    
    if produtos_recomendados:
        for i, produto in enumerate(produtos_recomendados[:4]):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Badge de risco
                    risco_badge = {
                        'baixo': '🟢 Baixo',
                        'medio': '🟡 Médio',
                        'alto': '🔴 Alto'
                    }
                    
                    st.subheader(f"📈 {produto['nome']}")
                    st.write(f"**Categoria:** {produto['categoria'].upper()}")
                    st.write(f"**Risco:** {risco_badge.get(produto['risco'], produto['risco'])}")
                    st.write(f"**Rentabilidade:** {produto['rentabilidade']}")
                    st.write(f"**Aporte mínimo:** R$ {produto['aporte_minimo']:,.2f}")
                    st.write(f"**Indicado para:** {produto['indicado_para']}")
                
                with col2:
                    if st.button(f"👍 Tenho Interesse", key=f"produto_{i}"):
                        st.success("✅ Ótimo! Preparei mais informações sobre este produto.")
                        st.balloons()
                
                st.markdown("---")
    else:
        st.warning("Nenhum produto encontrado para seu perfil.")

# ============================================
# TAB 5: INSIGHTS DETALHADOS
# ============================================
with tab5:
    st.header("💡 Insights Detalhados")
    
    # Exibir todos os insights
    for insight in insights:
        with st.container():
            st.info(insight)
            st.markdown("---")
    
    # Análise da reserva de emergência
    st.subheader("💰 Reserva de Emergência")
    reserva_atual = perfil['reserva_emergencia_atual']
    meta_reserva = perfil['metas'][0]['valor_necessario']
    progresso = (reserva_atual / meta_reserva) * 100
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Atual:** R$ {reserva_atual:,.2f}")
        st.write(f"**Meta:** R$ {meta_reserva:,.2f}")
        st.progress(min(progresso/100, 1.0))
        st.write(f"**Progresso:** {min(progresso, 100):.1f}%")
    
    with col2:
        if progresso < 100:
            faltam = meta_reserva - reserva_atual
            st.warning(f"⚠️ Faltam R$ {faltam:,.2f}")
            
            # Sugestão de aporte
            meses = 6
            aporte = faltam / meses
            st.success(f"💡 Aporte mensal sugerido: R$ {aporte:,.2f}")
        else:
            st.success("🎉 Meta alcançada!")
    
    st.markdown("---")
    
    # Análise de objetivos
    st.subheader("🎯 Progresso das Metas")
    
    for meta in perfil['metas']:
        with st.expander(f"📌 {meta['meta']}"):
            st.write(f"**Valor necessário:** R$ {meta['valor_necessario']:,.2f}")
            st.write(f"**Prazo:** {meta['prazo']}")
            
            # Progresso simulado (baseado na reserva)
            progresso_meta = min((perfil['reserva_emergencia_atual'] / meta['valor_necessario']) * 100, 100)
            st.progress(progresso_meta/100)
            st.caption(f"Progresso: {progresso_meta:.1f}%")
    
    st.markdown("---")
    
    # Resumo executivo
    st.subheader("📋 Resumo Executivo")
    
    resumo = f"""
    **Cliente:** {perfil['nome']} ({perfil['idade']} anos, {perfil['profissao']})
    
    **Perfil Financeiro:**
    - Perfil de Investidor: {perfil['perfil_investidor'].upper()}
    - Patrimônio Total: R$ {perfil['patrimonio_total']:,.2f}
    - Renda Mensal: R$ {perfil['renda_mensal']:,.2f}
    
    **Situação Atual:**
    - Reserva de Emergência: R$ {perfil['reserva_emergencia_atual']:,.2f} (Meta: R$ {meta_reserva:,.2f})
    - Saldo do Mês: R$ {analise_transacoes.get('saldo', 0):,.2f}
    - Atendimentos: {analise_atendimentos.get('total', 0)} (Resolução: {analise_atendimentos.get('taxa_resolucao', 0):.0f}%)
    
    **Principais Insights:**
    """
    for insight in insights[:3]:
        resumo += f"- {insight}\n"
    
    st.text(resumo)
    
    # Botão para exportar
    if st.button("📥 Baixar Resumo"):
        st.success("Resumo gerado com sucesso!")
        st.download_button(
            label="📄 Baixar como Texto",
            data=resumo,
            file_name=f"resumo_{perfil['nome'].replace(' ', '_')}.txt",
            mime="text/plain"
        )

# ============================================
# TAB 6: CONVERSAR COM A BIA (COM OLLAMA)
# ============================================
with tab6:
    st.header("💬 Conversar com a Bia")
    
    # Verificar se o Ollama está disponível
    try:
        # Verificar se o modelo existe
        ollama.list()
        ollama_disponivel = True
        st.success("🟢 Ollama disponível - Usando modelo llama3.1:8b")
    except:
        ollama_disponivel = False
        st.warning("🟡 Ollama não disponível - Usando respostas pré-definidas")
    
    # Exibir o system prompt
    with st.expander("📋 Ver System Prompt da Bia"):
        st.code(SYSTEM_PROMPT, language="markdown")
    
    st.markdown("---")
    
    # Inicializar histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"""Olá! Sou a Bia, sua assistente financeira personalizada. 

📊 Tenho acesso ao seu perfil de investidor, histórico de transações e atendimentos. 

Como posso ajudar você hoje? Posso:
- Analisar seu perfil de investidor
- Recomendar produtos financeiros personalizados
- Mostrar insights sobre seus gastos
- Explicar conceitos financeiros
- Acompanhar suas metas

O que você gostaria de saber?"""}
        ]
    
    # Exibir mensagens do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta para a Bia..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analisando dados..."):
                
                # Tentar usar Ollama se disponível
                if ollama_disponivel:
                    try:
                        resposta = perguntar(
                            pergunta=prompt,
                            perfil=perfil,
                            analise_transacoes=analise_transacoes,
                            analise_atendimentos=analise_atendimentos
                        )
                        
                        if resposta:
                            st.markdown(resposta)
                        else:
                            st.warning("⚠️ Erro ao gerar resposta com Ollama. Usando resposta pré-definida.")
                            resposta = generate_bia_response(prompt, transacoes, historico, perfil, produtos)
                            st.markdown(resposta)
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao usar Ollama: {e}")
                        st.info("💡 Usando resposta pré-definida...")
                        resposta = generate_bia_response(prompt, transacoes, historico, perfil, produtos)
                        st.markdown(resposta)
                else:
                    # Usar resposta pré-definida
                    resposta = generate_bia_response(prompt, transacoes, historico, perfil, produtos)
                    st.markdown(resposta)
        
        # Adicionar resposta ao histórico
        if resposta:
            st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    # Botão para limpar conversa
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Limpar Conversa"):
            st.session_state.messages = [
                {"role": "assistant", "content": f"""Olá! Sou a Bia, sua assistente financeira personalizada. 

📊 Tenho acesso ao seu perfil de investidor, histórico de transações e atendimentos. 

Como posso ajudar você hoje? Posso:
- Analisar seu perfil de investidor
- Recomendar produtos financeiros personalizados
- Mostrar insights sobre seus gastos
- Explicar conceitos financeiros
- Acompanhar suas metas

O que você gostaria de saber?"""}
            ]
            st.rerun()

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.caption("💡 Bia - Assistente Financeira Personalizada | Desenvolvido por Mobius")