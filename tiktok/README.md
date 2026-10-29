# TikTok — publicação manual dos Reels

Os Reels do Instagram são publicados também no TikTok. **O Rick posta pelo
app**, porque não há integração de publicação no TikTok (o Windsor só publica no
Instagram). O `claude` deixa tudo pronto: vídeo, legenda e checklist.

- **Vídeos:** os mesmos arquivos de `videos/` (9:16, 1080×1920, 47–49 s, sem
  marca d'água). O link de download de cada um está em `legendas.md`.
- **Legendas:** `legendas.md`, um bloco por vídeo, pronto para copiar.
- **Controle:** `fila.json` registra o que já foi para o TikTok. Depois de
  postar, avise o `claude` (ou o canal), que marca a data e o link.

## Checklist ao postar (app do TikTok)

1. Baixe o vídeo pelo link em `legendas.md` e salve na galeria.
2. Toque em **+** → **Carregar** → escolha o vídeo. Não acrescente música: o
   vídeo já tem narração.
3. **Capa:** escolha o quadro do gancho, por volta de 2 s, com o texto grande.
4. Cole a legenda do bloco correspondente.
5. **Mais opções → ligue "Conteúdo gerado por IA"**, porque a locução é
   sintética. Isso evita penalidade por falta de rótulo.
6. Publicar. Copie o link do vídeo e mande para o `claude` registrar.

## Ordem e ritmo

Para recuperar os 6 vídeos já feitos: 1 por dia, no fim da tarde, para não
coincidir com o Reel do Instagram (07:20). A ordem segue o desempenho no
Instagram: soldagem a frio, que teve o menor pulo, vem primeiro. Depois disso,
o Reel do dia vai para o TikTok no mesmo dia, e a rotina diária acrescenta o
bloco dele em `legendas.md`.

## Diferenças em relação ao Instagram

- Legenda curta: gancho, explicação em 1–2 frases, ressalva e fonte resumida.
  Links não são clicáveis no TikTok, por isso cito só a instituição e o ano;
  os links completos ficam na legenda do Instagram e em `src/captions.json`.
- Uma CTA só. Até 5 hashtags, sempre com `#PareceFakeEReal`.
- Métricas do TikTok: ainda não há leitura automática. Para medir, conecte o
  TikTok orgânico no Windsor, só leitura. Até lá, os números vêm de você
  pelo app.
