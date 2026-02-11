## PROMPT ALTERNATIVO - SCRIPT DE INFORMAÇÃO

Ajuste o texto fornecido para o formato de SCRIPT DE INFORMAÇÃO da Prefeitura do Rio de Janeiro.
Não crie, complete, interprete nem acrescente informações: utilize exclusivamente o conteúdo enviado como base, apenas reorganizando e reescrevendo.

### Contexto

Diferente dos Scripts de Serviço (focados em ação/solicitação), os Scripts de Informação focam na compreensão, orientação e contextualização. O cidadão lê para entender, não para pedir.

### 🚨 REGRAS CRÍTICAS - PRESERVAÇÃO DE CONTEÚDO

- **🚨 NUNCA invente ou adicione informações que não estejam no original**
- **Use APENAS o que está explícito nos dados**
- **PRESERVE TODAS as informações do original** - não remova nada
- **MANTENHA todos os prazos específicos** (se houver)
- **MANTENHA todas as observações importantes** (contatos, endereços, horários)
- **PRESERVE a formatação original** (listas, parágrafos) quando fizer sentido
- **NÃO remova detalhes técnicos ou específicos** se forem relevantes para a compreensão
- **NÃO adicione textos genéricos** que não estejam no original

### Regras de Formato e Escrita

- **Use Markdown para ESTRUTURAÇÃO** (bullet points, negrito para destaque).
- **Paragrafação:** Use parágrafos curtos (3-4 linhas) para facilitar a leitura.
- **Linguagem:** Simples, clara e cidadã. Evite termos técnicos, jurídicos ou burocráticos.
- **PROIBIDO:** Não use linguagem de solicitação, pedido ou atendimento (ex: "solicite", "agende", "clique aqui para acessar").
- **PROIBIDO:** Não utilize os tópicos “Para que serve” ou “Quem pode solicitar”.

### Estrutura Obrigatória

Utilize exatamente os seguintes tópicos, nesta ordem e retorne um JSON com estas chaves:

1. **`o_que_e`**: O que é
   - Definição clara do tema/política/equipamento.
   - Explique o conceito principal.

2. **`como_funciona`**: Como funciona
   - Funcionamento, regras gerais, aplicação prática na vida do cidadão.
   - Detalhes operacionais relevantes.

3. **`publico_alvo`**: Público-alvo
   - Para quem a informação é relevante.
   - **Importante:** Não use como critério de elegibilidade/restrição ("quem pode solicitar"), mas como direcionamento de interesse ("a quem interessa").

4. **`informacoes_importantes`**: Informações importantes
   - Contexto, observações relevantes, dados complementares.

### Objetivo

Traduzir o conteúdo fornecido para um formato informativo padronizado, permitindo que o cidadão compreenda o tema de forma rápida e acessível, eliminando a lógica de "serviço solicitado".
