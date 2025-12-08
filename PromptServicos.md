---

## PROMPT PRINCIPAL - Estrutura Padrão (limpezaservicos.mdc linhas 65-79)

Esta é a estrutura PRINCIPAL que deve ser seguida para padronizar TODOS os serviços:

{estrutura_principal}

---

## Serviço a Processar

**Texto de entrada (texto livre):**

{texto_entrada}

---

## Instruções

Analise o texto livre acima e extraia/processe as informações para criar uma descrição completa.

Siga TODAS as regras especificadas no início deste prompt, mas use a estrutura principal acima como referência PRINCIPAL para o formato de saída.
A linguagem deverá ser simples, sem jargões ou termos complexos, voltadas para uma população comum.

Retorne APENAS um JSON com os seguintes campos (use os nomes exatos das chaves):

- `descricao_resumida`: string (resumo curto, 1-2 frases)
- `descricao_completa`: string (Markdown com as 3 seções: "O que é", "Para que serve", "Quem pode solicitar")
- `servico_nao_cobre`: string ou lista Markdown (limitações)
- `tempo_atendimento`: string (prazos, ex: "72 horas", "até 20 dias")
- `custo`: string (valores ou "isento"/"gratuito")
- `resultado_solicitacao`: string (resultado/entregáveis esperados)
- `documentos_necessarios`: string ou Markdown list (lista de documentos)
- `instrucoes_solicitante`: string ou Markdown (instruções passo a passo)
- `canais_digitais`: string ou Markdown (URLs / plataformas)
- `canais_presenciais`: string ou Markdown (endereços e horários)
- `legislacao_relacionada`: string ou Markdown (referências legais)

        Cada campo deve ser preenchido — se uma informação não estiver disponível no texto de entrada, retorne uma string vazia para esse campo. Retorne o JSON puro (pode estar dentro de um bloco de código ```json```).

        ---

        Regras específicas por campo (siga rigorosamente):

        descricao_resumida
        - Objetivo: Resumo curto e direto do serviço em 1-2 frases.
        - Fontes: descricao, detalhes.
        - Regras: Texto sucinto; sem listas/seções; linguagem simples, sem jargões ou termos complexos, voltadas para uma população comum; sem prazos/documentos/canais/legislação.

        descricao_completa
        - Objetivo: Texto detalhado e estruturado em Markdown com as seções "O que é", "Para que serve", "Quem pode solicitar".
        - Fontes: descricao, detalhes, como_funciona, informacoes.
        - Regras: Preservar toda a informação do original; linguagem simples, sem jargões ou termos complexos, voltadas para uma população comum; manter prazos, exceções e observações; usar apenas as 3 seções; não incluir instruções/documentos/canais/legislação.
        - Limites por subseção: "O que é" (1-2 parágrafos, 3-4 linhas cada), "Para que serve" (1 parágrafo, 2-3 linhas), "Quem pode solicitar" (1 parágrafo, 2-3 linhas).
        - Regras do campo `descricao_completa` (composto pelas 3 subseções abaixo):

            1. **## O que é**
                - **LIMITE OBRIGATÓRIO:** 1-2 parágrafos, cada um com 3-4 linhas
                - Seja conciso e direto; explicação clara e objetiva do serviço
                - NÃO exceda 2 parágrafos; campo obrigatório (não pode ficar em branco)

            2. **## Para que serve**
                - **LIMITE OBRIGATÓRIO:** 1 parágrafo de 2-3 linhas
                - Seja OBJETIVO e centrado na ENTREGA do serviço
                - NÃO use textos genéricos como "visa melhorar" ou "busca garantir"
                - Exemplos de entrega: "Fiscalização efetiva das frotas de ônibus", "Coleta/Remoção dos entulhos"

            3. **## Quem pode solicitar**
                - **LIMITE OBRIGATÓRIO:** 1 parágrafo de 2-3 linhas
                - Campo obrigatório; sempre deve haver público-alvo
                - Caso não esteja explícito, usar o cidadão carioca como público padrão
                - Descrever público-alvo e requisitos de forma clara

                **ATENÇÃO ESPECIAL:** A seção "O que é" DEVE ser curta e objetiva. Se o texto de entrada for extenso, extraia apenas as informações essenciais e resuma em no máximo 2 parágrafos de 3-4 linhas cada. NÃO inclua todos os detalhes, apenas o essencial para explicar o que é o serviço.

        servico_nao_cobre
        - Objetivo: Listar o que o serviço NÃO cobre.
        - Fontes: detalhes, informacoes.
        - Regras: Itens curtos em lista; não misturar com instruções ou documentos.

        tempo_atendimento
        - Objetivo: Informar prazo/tempo estimado (ex.: 72 horas, até 20 dias).
        - Fontes: detalhes, informacoes.
        - Regras: Apenas o prazo; discriminar prazos por etapa se existirem; não colocar este conteúdo em descricao_completa.

        custo
        - Objetivo: Informar custo/taxa quando aplicável.
        - Fontes: detalhes, informacoes.
        - Regras: Especificar valores e quando são cobrados; se não houver custo, usar "isento" ou "gratuito".

        resultado_solicitacao
        - Objetivo: Descrever o resultado esperado após a conclusão (entregáveis/ações concluídas).
        - Fontes: detalhes, informacoes.
        - Regras: Ser objetivo e listar o output final.

        documentos_necessarios
        - Objetivo: Listar documentos exigidos.
        - Fontes: detalhes, informacoes.
        - Regras: Lista de itens; incluir somente documentos explicitamente mencionados.

        instrucoes_solicitante
        - Objetivo: Instruções passo a passo.
        - Fontes: como_funciona, detalhes.
        - Regras: Permite lista ordenada; não incluir conteúdo de descricao_completa nem legislação.

        canais_digitais
        - Objetivo: Canais digitais oficiais (URLs, plataformas, APIs).
        - Fontes: informacoes, detalhes.
        - Regras: Fornecer URLs/identificadores oficiais; não usar links dentro de descricao_completa.

        canais_presenciais
        - Objetivo: Locais físicos e horários.
        - Fontes: informacoes, detalhes.
        - Regras: Endereços completos e horários; não colocar endereços em descricao_completa.

        legislacao_relacionada
        - Objetivo: Referências legais, decretos ou normas.
        - Fontes: detalhes, informacoes.
        - Regras: Listar leis/decretos com identificação (nº, ano) e breve nota quando necessário; não inserir textos legais longos.
        """
