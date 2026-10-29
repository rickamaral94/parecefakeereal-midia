# TikTok — distribuição dos Reels

Rick pediu para avaliar a publicação dos Reels do claude pelo chatgpt. Em T-tiktok, a resposta do claude 20261029T151711352Z-claude-53b7 concorda: claude mantém produção/Instagram e entrega MP4 original + legenda; chatgpt revisa a adaptação e opera TikTok pelo Metricool quando os controles forem verificados.

## Estado verificado em 29/10/2026

- Metricool conectado à marca Parece fake, é real, brandId 7445255, fuso America/Sao_Paulo.
- Teste de escrita confirmado: rascunho da soldagem ID 410199721, UUID -7094515269486949826. [Abrir rascunho](https://app.metricool.com/planner/calendar?blogId=7445255&openWithPostUuid=-7094515269486949826).
- O rascunho foi relido com `draft=true` e `autoPublish=false`. **Não é publicação nem agendamento ativo.** 30/10 às 18h é apenas referência do rascunho.
- Upload confirmado do MP4 original H.264/AAC, 1080×1920, 48,03 s; blob do vídeo conferido na main: aa665c381104041de651156e656565e60286cc84.
- A ferramenta não abriu o URL raw como arquivo de upload; funcionou com caminho local do MP4. Usar `tiktokData.title`, exigido pelo conector. Após cada falha, fila foi consultada antes de tentar novamente; só um rascunho foi criado.
- Consulta de vídeos publicados no período retornou vazia; isso não prova ausência de posts manuais ou histórico completo. Conferir perfil antes de ativar.

## Pendências antes de ativar publicação automática

1. Confirmar o perfil TikTok correto e reconciliar qualquer vídeo já publicado manualmente.
2. Verificar plano e contador real de cota no planner. A documentação do Free informa até 20 posts/mês; não confundir esse limite genérico com saldo disponível da conta.
3. Conferir o rótulo nativo **Conteúdo gerado por IA** (locução sintética). A documentação do Metricool diz que existe para vídeos; a resposta do conector não mostrou um campo de IA no bloco TikTok. Não inventar nome de parâmetro nem considerar o aviso da legenda equivalente ao toggle.
4. Conferir capa do gancho e privacidade. Não adicionar música extra.
5. Rever legenda/fonte na execução e publicar claim `T-pub-<data>-tiktok` antes da ativação. Uma ação por peça e verificação de duplicidade.

Sem essas confirmações, manter o item como rascunho. Sem assinatura, upgrade ou gasto. Nenhum serviço novo ou automação recorrente foi criado. O fluxo manual pelo app continua sendo alternativa; não publicar manualmente o mesmo vídeo sem reconciliar o rascunho.

## Arquivos e rastreio

- Vídeos originais em videos/, sem baixar de Reels publicados ou acrescentar marca de outra rede.
- Legendas em legendas.md; ainda não há review independente de todos os seis resumos nesta rodada. O primeiro foi confrontado com ESA STM-279 (superfícies/óxidos/contato).
- fila.json registra rascunhos, IDs do Metricool, agendamentos e URL/ID TikTok quando verificados. Nunca marcar rascunho ou resposta ambígua como postado.
- Após erro na API, consultar fila e perfil antes de repetir: erro não prova ausência de publicação.
- Distribuição proposta: 1 vídeo por dia para recuperar a fila, começando pela soldagem. O Free de até 20/mês não comporta publicar diariamente o mês inteiro: verificar cota e levar o calendário ao Rick, sem alterar a frequência do Instagram.
- Os carrosséis TikTok permanecem fora do escopo desta etapa.

## Métricas

O conector Metricool oferece catálogo TikTok de métricas por vídeo/conta. Campos disponíveis no catálogo não garantem dados: nesta consulta, linhas por vídeo vieram vazias. Indisponível não é zero. Registrar rede, janela e fonte; não misturar resultados com o A/B do Instagram.

## Documentação consultada

- [Metricool: publicar no TikTok](https://help.metricool.com/schedule-and-post-on-tiktok-bkepi).
- [Metricool: planos e limite Free](https://help.metricool.com/main-differences-between-free-and-paid-plans-bl0v9).
- [ESA STM-279](https://esamultimedia.esa.int/multimedia/publications/STM-279/STM-279.pdf).
