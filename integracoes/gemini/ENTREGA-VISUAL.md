# Escopo confirmado por Rick — 03/11/2026

Rick escolheu: textos e artes/vídeos finais pelo Gemini. Descrição visual não equivale a arte pronta. O adaptador gerar.py cobre apenas o texto; a integração visual ainda precisa ser implementada e testada após configurar acesso. Não existe conteúdo final Gemini nesta entrega.

## Piloto proposto ao claude: GPS

- Curadoria conjunta: confirmar roteiro de briefing-gps.json e usar somente fatos verificados no NIST. Pauta antiga aprovada não equivale a aprovação da arte final.
- Texto: Gemini escreve versão final para revisão conjunta.
- Artes: modelo Gemini de imagem recebe cada texto aprovado e identidade visual; entrega 7 arquivos de conteúdo em proporção 4:5, a validar em 1080×1350, com textos legíveis, amarelo/branco/fundo escuro e selo de diagrama/IA. Não substituir as artes por render próprio e dizer que são Gemini.
- Slide8: reutilizar marca/card_final_carrossel.jpg; não pedir nova geração da marca.
- Inspeção: conferir leitura no celular, contraste, ortografia, fidelidade dos diagramas, fonte, conclusão e card. Reprovar saída com número inventado, arte ilegível ou aparência de foto falsa. Revisão humana/agentes continua necessária, mesmo se o modelo declarar ter cumprido tudo.
- Guardar resposta bruta, arquivo original, modelo e vínculo ao briefing. Não habilitar publicação por consequência da geração.

## Reels posteriores

Produção final de vídeo também precisa de modelo específico, compatível com os formatos/durações do PLAYBOOK, disponibilidade e orçamento de Rick. O script de texto não gera vídeo nem áudio. Não selecionar automaticamente um modelo antigo de Veo: a documentação consultada em03/11 informa mudança/descontinuação de previews; consultar o catálogo atual da conta e custos antes de executar. Não contratar plano nem habilitar cobrança.

Documentação oficial aberta nesta sessão:
- https://ai.google.dev/gemini-api/docs/image-generation
- https://ai.google.dev/gemini-api/docs/video

## Bloqueios concretos

Sem GEMINI_API_KEY e sem liberação de generativelanguage.googleapis.com neste ambiente. Nenhum plugin Gemini encontrado. É necessário configurar o segredo e a permissão de rede pelo fluxo do ambiente; instalar SDK não supre autenticação nem rede. Não inserir chave em mensagem ou arquivo versionado.

Aguardando claude responder à proposta de roteiro/curadoria e informar se tem acesso configurado do lado dele. Sem essa resposta, o piloto continua proposto, não acordado entre os dois.
