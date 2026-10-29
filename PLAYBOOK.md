# Playbook — operação diária do @parecefakeereal

Este arquivo é a instrução completa para cada execução agendada. Leia inteiro antes de agir.

## Objetivo e regras fixas

- Perfil de curiosidades de ciência, natureza, história, espaço e tecnologia: fatos que parecem inventados, com fundamento real e fontes verificáveis. Público: língua portuguesa. Objetivo: crescimento orgânico de seguidores.
- Formato: **1 Reel por dia**, vertical 9:16, **40–50 s**, narração neural PT-BR (Supertonic 3, vozes M3/M4 alternadas), legendas na tela. Sem Stories por enquanto. Carrosséis voltaram como responsabilidade do `chatgpt` (ver `EQUIPE.md`); antes tiveram mediana de 3 contas alcançadas.
- Estrutura: gancho → pistas → explicação → consequência → 1 CTA.
- **Uma CTA por post** (seguir, enviar a alguém, salvar ou comentar). Até 5 hashtags específicas, sempre incluindo `#PareceFakeEReal`.
- **Confiança acima de tudo:** valide a afirmação principal em fonte primária ou institucional (estudo, universidade, museu, agência científica) com WebSearch/WebFetch *na própria execução*. Diferencie fato, hipótese e interpretação; coloque a ressalva necessária no vídeo e na legenda. Se não conseguir verificar, **troque de tema** — nunca publique alegação não verificada.
- Todo vídeo diz na tela e na legenda que as imagens são ilustração/animação autoral e que a locução é sintética. Não use imagens, vídeos ou músicas de terceiros.
- Não compre seguidores, não faça comentários artificiais, não envie mensagens, não gaste dinheiro.
- Não repita pauta já usada (lista em `queue.json` → `temas_usados`).

## Carrosséis (do `chatgpt`)

- Divisão de tarefas, fluxo de revisão e lista de checagem: `EQUIPE.md`. O `claude` revisa todo carrossel antes da publicação e, se o `chatgpt` não tiver acesso ao Windsor, publica o carrossel aprovado sem mudar o conteúdo.

- Seguem `prompts/carrossel.md`: slide de conclusão que responde a pergunta com frase afirmativa e ponto final, e **último slide sempre o card da página** (`marca/card_final_carrossel.jpg`).
- Imagens 4:5 (1080×1350) em JPEG, publicadas via `create_carousel_post` com links raw do GitHub.
- Por ora os Reels seguem prioridade; carrossel só como conteúdo extra, sem substituir o Reel do dia.

## Teste em andamento: tipo de gancho

- Grupo **A** = gancho em pergunta de mecanismo ("Por que…?", "Como…?").
- Grupo **B** = gancho em afirmação surpreendente.
- Métrica principal: taxa de pulo <3 s (`media_reel_skip_rate`). Secundária: tempo médio assistido ÷ duração.
- Leitura com ≥72 h de cada post. Critério: se a mediana de pulo de A for ≥15 p.p. menor que a de B após 7 posts, A vira padrão. Com poucos posts, é sinal, não prova.
- Mantenha a alternância de grupos definida na fila; ao criar pautas novas, alterne A/B.

## Passo a passo de cada execução

1. **Preparar:** este repositório já deve estar clonado (se não estiver, use `add_repo` para `rickamaral94/parecefakeereal-midia` com acesso push e clone). Leia `queue.json` e `log.md`.
   - **Canal com o `chatgpt`:** busque `collab/channel`, rode a rotina do §2 de `collab/PROMPT.md` (validate, inbox, board) e responda o que estiver para `claude`. Antes de publicar, publique o `claim` de `T-pub-<AAAA-MM-DD>` (lease 24 h) e confira que nenhum `review` com `changes`/`reject` sobre o item do dia está aberto; se houver, troque de item ou corrija antes. Pautas aprovadas no canal entram na fila citando o id da mensagem.
2. **Métricas (Windsor, conector `instagram`, conta `17841423367864963`):**
   - `get_data` com `followers_count` (perfil) e, por mídia, `timestamp, media_id, media_type, media_caption, media_reach, media_views, media_shares, media_saved, media_like_count, media_comments_count, media_reel_avg_watch_time, media_reel_skip_rate` dos últimos 14 dias.
   - Atualize em `queue.json` (Reels) e em `carrosseis/fila.json` (carrosséis) as métricas dos itens publicados (campo `metricas`, com a data da leitura e as horas desde a publicação).
   - Indisponível ≠ zero. Não invente números.
3. **Escolher o item do dia:** o primeiro item da `fila` com `status` = `pronto` é publicado. Se não houver item `pronto`, produza o primeiro `pendente` cuja pauta tenha `review` `approve` do `chatgpt` no canal (passo 4). Se nenhuma tiver, produza o primeiro `pendente` mesmo assim e marque `"revisao": "pos-publicacao"` (`EQUIPE.md` §2).
   - **Carrosséis:** antes do Reel, revise os itens `pronto` de `carrosseis/fila.json` com a lista do `EQUIPE.md` §3 (`review` no canal) e publique o aprovado com `create_carousel_post` (links raw fixados no commit), registrando `media_id` na fila de carrosséis.
4. **Produzir (quando necessário):**
   - Pesquise e valide o tema; anote as fontes (URLs) no item da fila.
   - Escreva o roteiro em trechos `(legenda_na_tela, texto_para_tts, cena)` seguindo `src/reel3_tardigrados.py` como modelo; números por extenso no texto de TTS; legendas com no máximo 3 linhas.
   - Cenas: animações vetoriais desenhadas com PIL via `src/engine.py` (gancho grande no topo nos primeiros segundos, elemento visual em movimento, rótulos curtos).
   - Narração: Supertonic 3 (ver "Ferramentas"). Alterne as vozes **M3** e **M4** a cada Reel, seguindo o campo `voz` da fila (passe `voice="M3"` ou `"M4"` em `engine.render`). Distribua as vozes igualmente entre os grupos A e B para não contaminar o teste de ganchos. Ajuste `speed` (1.1 a 1.25) para caber em 40–50 s.
   - Gere o preview (`preview`), **olhe o sheet.png** e corrija sobreposições de texto antes do render final. Duração final entre 40 e 50 s.
   - Salve o script em `src/`, o vídeo em `videos/`, a legenda em `src/captions.json`, marque o item como `pronto`, faça commit e push.
5. **Publicar:** `execute_action` → `create_video_post` com
   - `video_url`: `https://raw.githubusercontent.com/rickamaral94/parecefakeereal-midia/main/videos/<arquivo>.mp4` (só depois do push),
   - `caption` do `captions.json`, `share_to_feed: true`, `thumb_offset` ≈ 2000 ms (quadro do gancho).
   - Registre `media_id`, data/hora (São Paulo) e `status: publicado` na fila. Commit e push.
6. **Manter a fila abastecida:** se restarem menos de 3 itens `pendente`/`pronto`, proponha pautas novas no canal (`proposal` em `T-pauta-<slug>`, para revisão do `chatgpt`) e adicione-as à fila (tema, pergunta central, grupo A/B, CTA, motivo), variando áreas e evitando `temas_usados`. Prefira temas com mecanismo físico explicável.
7. **Revisão semanal (aos domingos):** escreva em `log.md` uma seção com PARAR / MANTER / AMPLIAR / TESTAR (evidência → interpretação → ação → métrica), a evolução de seguidores e o placar do teste A/B. Ajuste a fila conforme a evidência.
7b. **TikTok:** acrescente ao fim de `tiktok/legendas.md` o bloco do Reel do dia (link raw do vídeo e legenda curta: gancho, explicação em 1–2 frases, ressalva, fonte resumida sem link, uma CTA, até 5 hashtags com `#PareceFakeEReal`) e um item `pronto` em `tiktok/fila.json`. O Rick posta pelo app (ver `tiktok/README.md`); quando ele avisar, marque `postado`.
8. **Registrar:** acrescente uma linha em `log.md` (data, o que foi publicado, media_id, observações). Commit com a mensagem terminando nas linhas de atribuição exigidas pela sessão.
9. **Avisar o dono do perfil** com `SendUserMessage` em 2–4 linhas: o que foi publicado, números relevantes, qualquer bloqueio.

## Se algo falhar

- Erro do Windsor (ex.: ações de escrita desligadas, permissão): não tente outro caminho de publicação; registre em `log.md` e avise com o motivo exato.
- **Erro na publicação não prova que nada foi publicado.** Em 29/10 o `create_carousel_post` respondeu "Application request limit reached" e o carrossel foi ao ar mesmo assim. Antes de qualquer nova tentativa, liste as mídias do dia no Windsor (`timestamp, media_id, media_type, media_caption`) e só tente de novo se o post não estiver lá.
- Falha de render, voz ou verificação de fonte: não publique nada pela metade. Avise e deixe o item `pendente`.
- Nunca apague posts nem comentários.

## Ferramentas

```bash
# Voz neural Supertonic 3 (PT-BR) rodando com sherpa-onnx, baixados do GitHub
export TTS_DIR=/tmp/tts && mkdir -p $TTS_DIR && cd $TTS_DIR
curl -sSL -o so.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.8/sherpa-onnx-v1.13.8-linux-x64-static.tar.bz2 && tar xjf so.tar.bz2
curl -sSL -o st.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2 && tar xjf st.tar.bz2
# engine.py lê TTS_DIR (padrão /tmp/tts). Vozes: M3 = sid 7, M4 = sid 8.
```

Fontes do sistema: Inter (`/usr/share/fonts/opentype/inter/`). Requer ffmpeg, Pillow e numpy.
