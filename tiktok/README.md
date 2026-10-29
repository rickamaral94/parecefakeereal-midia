# TikTok — distribuição dos Reels

Rick autorizou o primeiro TikTok em 29/10/2026: “Melancia / Pode publicar”. Conforme T-tiktok, claude mantém produção/Instagram e entrega MP4 original + legenda; chatgpt revisa a adaptação e opera TikTok pelo Metricool.

## Estado verificado em 29/10/2026

- Marca Parece fake, é real, brandId 7445255, fuso America/Sao_Paulo.
- Soldagem a frio: agendamento aceito para 29/10 às 12:34 BRT, ID 410215827, UUID -7094515269486949826. [Abrir no planner](https://app.metricool.com/planner/calendar?blogId=7445255&openWithPostUuid=-7094515269486949826).
- `draft=false`, `autoPublish=true`, privacidade PUBLIC_TO_EVERYONE. Publicação confirmada por releitura: provider `PUBLISHED`, `detailedStatus=Published`, ID final TikTok `7702113481624931590`. O ID intermediário 7702113269397538823 não era o ID final. A URL retornada usa nome de exibição; navegação pública não foi confirmada nesta ferramenta. Não reenviar.
- Rótulo nativo IA: `tiktokData.isAigc=true` enviado e confirmado por releitura do rascunho antes da ativação. Capa: `videoCoverMilliseconds=2000`.
- Upload do MP4 original H.264/AAC, 1080×1920, 48,03 s; blob main aa665c381104041de651156e656565e60286cc84. Sem música adicionada.
- A API exige caminho local no upload e `tiktokData.title`. Ao atualizar, devolve outro ID; UUID permanece. Os blocos twitterData/instagramData retornados como defaults na leitura devem ser omitidos na escrita de um post apenas TikTok: o validador rejeita redes ausentes de providers.
- Claim: T-pub-2026-10-29-tiktok, chatgpt. Não publicar cópia manual enquanto houver este agendamento.

## Operação e rastreio

1. Conferir a fila, respostas no canal e duplicidade antes de cada peça. A consulta de analytics vazia não comprova ausência de posts manuais.
2. Rever afirmação e fonte primária; primeiro vídeo confrontado com ESA STM-279 (contatos, desgaste e superfícies no vácuo).
3. Publicar claim antes da ativação. Preservar mídia, legenda e controles ao atualizar; reler o estado.
4. Registrar agendado quando aceito e postado apenas com confirmação de publicação/URL ou ID TikTok.
5. Após erro ou retorno ambíguo, consultar estado antes de repetir. Erro não prova ausência de publicação.
6. Sem upgrade, assinatura ou gastos. O plano Free informa até 20 posts/mês; o saldo da conta não está exposto pelo conector. Erros reais de cota devem ser registrados; não presumir saldo.
7. **Ritmo decidido pelo Rick (29/10): 1 TikTok por dia.** Os cinco restantes podem ser agendados de uma vez no Metricool, um por dia, no fim da tarde. Assim o ritmo não depende de o `chatgpt` ser acordado todo dia. Atenção à cota do plano Free (até 20 posts/mês): registre o primeiro erro de cota em vez de presumir saldo. Não alterar a frequência do Instagram.

## Plano B pelo app

Se a integração falhar, reconciliar primeiro o estado do Metricool e o perfil para evitar duplicata. Só depois usar o MP4 original de videos/ e a legenda revisada de legendas.md, sem música extra, capa do gancho em aproximadamente 2s, rótulo Conteúdo gerado por IA ativado e privacidade conferida. Registrar URL/ID na fila e avisar o outro agente; nunca publicar manualmente por cima de um agendamento ativo.

## Métricas

Dados indisponíveis não são zero. Registrar rede, janela e fonte; não misturar resultados TikTok com o A/B do Instagram. Os cinco resumos foram revisados em 29/10: quatro aprovados em8ea3; plantas corrigido após changes1319 e resposta claude-f19b, com alteração na main81126e0. Carrosséis TikTok ficam fora desta etapa.

## Fontes

- [Metricool: TikTok](https://help.metricool.com/schedule-and-post-on-tiktok-bkepi).
- [Metricool: planos](https://help.metricool.com/main-differences-between-free-and-paid-plans-bl0v9).
- [ESA STM-279](https://www.esa.int/About_Us/ESA_Publications/STM-279_Assessment_of_the_Cold_Welding_between_Separable_Contact_due_to_Impact_and_Fretting_under_Vacuum).

## Lote ativado em 29/10/2026

Rick autorizou diretamente: “autorizo ativar os 5 rascunhos do TikTok, 1 por dia de 30/10 a 03/11 às 18h”. Os mesmos cinco UUIDs foram convertidos em agendamentos ativos. Releitura confirmou `draft=false`, `autoPublish=true`, IA nativa ligada, capa em 2000 ms, mesmo texto e mesma mídia.

| Data (18h, Brasília) | Vídeo | ID Metricool |
|---|---|---|
| 2026-10-30 | reel6_patos_borracha | 410275751 |
| 2026-10-31 | reel4_mpemba | 410275860 |
| 2026-11-01 | reel5_nitinol | 410275978 |
| 2026-11-02 | reel3_tardigrados | 410276132 |
| 2026-11-03 | reel2_plantas | 410276236 |

O bloqueio anterior de autorização foi resolvido pela mensagem direta de Rick, sem contorno nem reenvio de arquivos. Agendado não significa postado: confirmar o retorno do TikTok em cada data antes de mudar para postado. Não publicar cópia manual.

A revisão de plantas encontrou evidência posterior à fonte original: [Seltzer et al., eLife 2026](https://elifesciences.org/articles/104700v1) demonstra resposta de mariposas aos sons. A legenda limita a ressalva ao estudo de 2023, conforme correção aceita pelo claude. Revisão em `revisao-lote-20261029.md`.
