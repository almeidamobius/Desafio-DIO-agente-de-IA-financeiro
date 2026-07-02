# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |
| **Contextualização** | O agente usou os dados do cliente corretamente? | Responder sobre metas usando dados reais do perfil |
| **Tom e Empatia** | A resposta foi profissional e acolhedora? | Avaliar se o tom é consultivo e respeitoso |
| **Precisão Numérica** | Os valores e cálculos estão corretos? | Verificar se os totais de gastos batem com os dados |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** R$ 570,00 (baseado no transacoes.csv)
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente retornou o valor correto somando as transações de alimentação.

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil moderado
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente recomendou produtos de risco baixo e médio, alinhados ao perfil.

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente redirecionou para temas financeiros.

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente informou que não tem dados sobre o produto.

### Teste 5: Análise de perfil
- **Pergunta:** "Qual meu perfil de investidor?"
- **Resposta esperada:** Moderado (baseado no perfil_investidor.json)
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente identificou corretamente o perfil moderado.

### Teste 6: Metas financeiras
- **Pergunta:** "Como está minha reserva de emergência?"
- **Resposta esperada:** R$ 10.000,00 de R$ 15.000,00 (66,7%)
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observação:** O agente calculou o progresso corretamente.

### Teste 7: Análise completa de gastos com sugestões
- **Pergunta:** "Faça uma análise completa dos meus gastos e me indique onde posso economizar"
- **Resposta esperada:** Análise detalhada por categoria com valores corretos e sugestões práticas
- **Resultado:** [ ] Correto  [ ] Incorreto
- **Observação:** [Preencher após testar]

---

## Resultados dos Testes

### O que funcionou bem:
- O agente conseguiu identificar corretamente o perfil do investidor (moderado)
- As respostas sobre gastos trouxeram os valores corretos do CSV
- O agente manteve um tom consultivo e profissional
- A integração com Ollama funcionou para perguntas mais complexas
- O fallback para respostas pré-definidas funcionou quando necessário
- Os gráficos e visualizações ajudaram na compreensão dos dados

### O que pode melhorar:
- Em alguns momentos, o Ollama gerou respostas muito longas
- O agente poderia ser mais direto em respostas simples
- Sugestões de economia poderiam ser mais específicas
- A resposta poderia incluir mais dados numéricos precisos
- O contexto dos dados poderia ser melhor aproveitado em perguntas complexas

### Média das Notas (1-5):
- Assertividade: 4.5
- Segurança: 5.0
- Coerência: 4.5
- Contextualização: 4.0
- Tom e Empatia: 5.0
- Precisão Numérica: 4.5

---

## Análise da Resposta do Agente (Cenário 7)

**Pergunta:** "faça uma análise completa dos meus gastos me indique onde posso economizar"

**Resposta do Agente:**
> Olá João! É um prazer trabalhar com você para entender melhor seus gastos e identificar oportunidades de economia.
> 
> Ao analisar os dados disponíveis, podemos ver que você tem uma boa compreensão dos seus gastos e já está trabalhando em construir uma reserva de emergência. No entanto, existem alguns pontos que podem ser otimizados para ajudá-lo a alcançar seus objetivos financeiros.
> 
> **Análise dos Gastos**
> 
> Vamos analisar os gastos em cada categoria:
> 
> - **Moradia:** R$ 1.380,00 é um valor razoável para aluguel, mas poderia ser otimizado se você considerasse a opção de compartilhar o espaço com alguém ou procurar um lugar mais barato.
> - **Alimentação:** R$ 570,00 pode ser economizado se você preparar refeições em casa e evitar comer fora frequentemente. Além disso, considere planos de alimentação que ofereçam descontos e promoções.
> - **Transporte:** R$ 295,00 é um valor razoável para o transporte público, mas poderia ser otimizado se você considerasse a opção de usar bicicleta ou caminhar nos trajetos mais curtos.
> 
> **Oportunidades de Economia**
> 
> Com base na análise dos gastos, aqui estão algumas oportunidades de economia que podem ser exploradas:
> 
> - **Reduzir o aluguel:** Pesquise a possibilidade de compartilhar o espaço ou procurar um lugar mais barato.
> - **Economizar com alimentação:** Prepare refeições em casa e considere planos de alimentação que ofereçam descontos e promoções.
> - **Otimizar o transporte:** Considere a opção de usar bicicleta ou caminhar nos trajetos mais curtos.
> 
> **Sugestões**
> 
> Para ajudá-lo a implementar essas mudanças, sugiro:
> 
> - **Crie um orçamento detalhado:** Registre todos os seus gastos em uma planilha para ter uma visão clara de onde está sendo gasto seu dinheiro.
> - **Estabeleça metas realistas:** Defina metas específicas e alcançáveis

### Avaliação da Resposta:

| Critério | Nota (1-5) | Justificativa |
|----------|------------|---------------|
| **Assertividade** | 4.5 | Respondeu diretamente à pergunta sobre análise de gastos e economia |
| **Segurança** | 5.0 | Não inventou dados, usou informações reais do CSV |
| **Coerência** | 4.5 | As sugestões fazem sentido para o perfil moderado |
| **Contextualização** | 4.0 | Usou os dados do cliente, mas poderia ser mais específico |
| **Tom e Empatia** | 5.0 | Tom consultivo, profissional e acolhedor |
| **Precisão Numérica** | 5.0 | Valores corretos, mas poderia mostrar mais detalhes |

### Pontos Fortes:
- ✅ Tom profissional e acolhedor
- ✅ Valores corretos baseados nos dados
- ✅ Sugestões práticas e relevantes
- ✅ Estrutura clara e organizada

### Pontos a Melhorar:
- ⚠️ Poderia incluir mais detalhes numéricos (porcentagens, comparações)
- ⚠️ Sugestões de economia poderiam ser mais específicas (valores estimados)
- ⚠️ Poderia mencionar as metas do cliente para contextualizar melhor
- ⚠️ Poderia sugerir um plano de ação com prazos

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

### Métricas de Performance
- **Latência:** Tempo de resposta do Ollama (média de 2-5 segundos)
- **Taxa de Erro:** ~5% das requisições (quando Ollama não está disponível)
- **Tempo de Processamento:** ~3 segundos para respostas complexas

### Métricas de Uso
- **Consumo de Tokens:** ~200-500 tokens por resposta
- **Modelo Utilizado:** llama3.1:8b (local)
- **Fallback Rate:** ~10% das respostas usam fallback (quando Ollama offline)

### Ferramentas Recomendadas
Ferramentas especializadas em LLMs podem ajudar no monitoramento:

- **[LangWatch](https://langwatch.ai/):** Monitoramento e avaliação de LLMs
- **[LangFuse](https://langfuse.com/):** Observabilidade para aplicações LLM
- **[LangSmith](https://smith.langchain.com/):** Depuração e testes de LLMs
- **[PromptLayer](https://promptlayer.com/):** Rastreamento de prompts e respostas
- **[Weights & Biases](https://wandb.ai/):** Rastreamento de experimentos

Entretanto, fique à vontade para usar qualquer outra ferramenta que você já conheça!

---

## Checklist de Testes

Antes de considerar o agente pronto, verifique:

- [x] O agente responde corretamente sobre perfil do cliente
- [x] O agente analisa transações corretamente
- [x] O agente recomenda produtos baseados no perfil
- [x] O agente reconhece quando não sabe a resposta
- [x] O agente não inventa dados financeiros
- [x] O agente mantém tom profissional e empático
- [x] O agente usa os dados da pasta data/ corretamente
- [x] O agente funciona com Ollama (quando disponível)
- [x] O agente tem fallback sem Ollama
- [x] A interface Streamlit é intuitiva

---

## Próximos Passos

1. **Coletar Feedback:** Pedir para mais pessoas testarem
2. **Analisar Resultados:** Identificar padrões de erro
3. **Ajustar Prompts:** Refinar o system prompt para respostas mais diretas
4. **Melhorar Dados:** Expandir dados mockados com mais categorias
5. **Documentar Aprendizados:** Registrar o que funcionou e o que pode melhorar
6. **Aprimorar Respostas:** Incluir mais detalhes numéricos e planos de ação
