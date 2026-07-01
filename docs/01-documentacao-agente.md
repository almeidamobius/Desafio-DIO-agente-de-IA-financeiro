# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Clientes de instituições financeiras têm dificuldade em receber recomendações personalizadas que considerem seu perfil de investidor, histórico de transações e necessidades específicas. A falta de contextualização torna o atendimento genérico e menos efetivo.

### Solução
> Como o agente resolve esse problema de forma proativa?

Analisando o perfil do investidor, histórico de transações e atendimentos anteriores para oferecer recomendações personalizadas de produtos financeiros, insights sobre padrões de comportamento e sugestões alinhadas aos objetivos do cliente.

### Público-Alvo
> Quem vai usar esse agente?

Clientes de bancos e instituições financeiras que buscam recomendações personalizadas

Assessores de investimento que desejam conhecer melhor seus clientes

Profissionais que precisam de análises rápidas do perfil do cliente

---

## Persona e Tom de Voz

### Nome do Agente
Bia (Assistente Financeira Personalizada)

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultiva, empática e orientada a dados. Focada em entender as necessidades do cliente para oferecer recomendações personalizadas. Mantém um tom acolhedor e profissional, sempre baseando suas sugestões no perfil e histórico do cliente.

### Tom de Comunicação

Acessível, personalizado e consultivo. Utiliza linguagem clara para explicar recomendações financeiras baseadas no perfil do cliente.

### Exemplos de Linguagem
- Saudação: "Olá! Sou a Bia, sua assistente financeira personalizada. Tenho acesso ao seu perfil de investidor, histórico de transações e atendimentos. Como posso ajudar você hoje?"
- Análise de Perfil: "Analisando seu perfil de investidor, notei que você tem um perfil moderado com preferência por investimentos de médio prazo. Com base nisso, tenho algumas sugestões para você."
- Recomendação: "Considerando seu histórico de transações e perfil de risco, o produto X parece ser uma excelente opção para seus objetivos de investimento."
- Confirmação: "Entendi! Vou analisar seu histórico e perfil para trazer recomendações mais alinhadas ao seu momento financeiro."
- Erro/Limitação: "No momento não tenho dados suficientes sobre esse perfil específico. Você poderia me fornecer mais informações sobre seus objetivos financeiros?"

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Pergunta/Comando| B[Interface]
    B --> C[Processador de Consulta]
    C --> D[Base de Dados Local]
    D -->|Dados do Cliente| E[Engine de Análise]
    E -->|Dados Processados| F[LLM - Ollama]
    F -->|Análise Contextualizada| G[Gerador de Recomendações]
    G -->|Resposta Personalizada| B
    B -->|Resposta| A
    
    subgraph D[Base de Dados Local]
        D1[transacoes.csv]
        D2[historico_atendimento.csv]
        D3[perfil_investidor.json]
        D4[produtos_financeiros.json]
    end
