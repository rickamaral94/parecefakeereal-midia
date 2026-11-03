# Gemini — produção final do conteúdo

Pedido de Rick em 03/11/2026: chatgpt e claude definem curadoria, tema e roteiro; Gemini produz a versão final. Piloto proposto: carrossel GPS/relatividade, cuja pauta já recebeu approve397b. A nova revisão do roteiro está pendente em T-gemini-producao. Isto não substitui a rotina nem autoriza publicação.

## Estado real

Nenhuma chamada ao Gemini foi feita. Ambiente sem GEMINI_API_KEY, sem google-genai e sem liberação de generativelanguage.googleapis.com na política de rede. Busca por plugin Gemini não retornou integração disponível. A conta do ChatGPT não fornece uma chave de API OpenAI; não é necessária aqui: o briefing é feito nesta conversa, sem chamar GPT-4o novamente.

O exemplo do Rick pede texto e descrição de capa. Ele não gera arquivos JPEG, vídeo nem narração. Este adaptador também entrega texto/direção visual; artes finais produzidas por Gemini exigem uma integração de geração de imagem apropriada, a definir com Rick. Não atribuir uma imagem renderizada por nós ao Gemini.

## Preparação sem acesso externo

    python3 integracoes/gemini/gerar.py integracoes/gemini/briefing-gps.json

O padrão apenas monta o prompt. Não usa chave, SDK, rede ou créditos e não cria uma resposta fictícia do Gemini.

## Conexão e execução real

1. Configurar GEMINI_API_KEY nos segredos do ambiente de execução. Nunca colar em chat, canal ou repositório.
2. Liberar generativelanguage.googleapis.com pela configuração de rede suportada. Não alterar proxy para contornar política.
3. Instalar o SDK: `python3 -m pip install google-genai`.
4. Após resposta do claude, registrar o ID da revisão no campo review_roteiro do briefing. Rever fontes na sessão de geração.
5. Selecionar um modelo disponível na conta. O modelo gemini-2.5-flash veio do exemplo do Rick; sua disponibilidade atual não foi testada. Nenhum faturamento ou plano pago foi habilitado.

Exemplo, quando o acesso estiver configurado e o modelo confirmado:

    python3 integracoes/gemini/gerar.py integracoes/gemini/briefing-gps.json --generate --model gemini-2.5-flash --out /tmp/gps-gemini.json

Uma chamada por execução, sem retry automático. A resposta integral fica em conteudo_original_gemini, com modelo, horário e hash do briefing. O arquivo fica gerado_pendente_revisao; não altera fila e não publica. Revisão dos dois agentes e inspeção de eventual arte continuam necessárias. O código não atesta automaticamente veracidade nem qualidade da saída.

Fontes de implementação: https://ai.google.dev/gemini-api/docs/quickstart e https://github.com/googleapis/python-genai . Fonte factual e evidência no briefing. Nenhuma credencial deve entrar nos arquivos.
