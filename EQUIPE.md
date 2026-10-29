# Equipe do @parecefakeereal — quem faz o quê

Decisão do Rick (29/10/2026): **`claude` cuida dos Reels, `chatgpt` cuida dos
posts (carrosséis)**, e cada um revisa o conteúdo do outro antes de ir ao ar,
com foco em **veracidade** e em **temas que façam sentido para o nosso
público**. A coordenação acontece no branch `collab/channel`
(`collab/PROMPT.md`).

## 1. Responsabilidades

| | `claude` — Reels | `chatgpt` — Posts (carrosséis) |
|---|---|---|
| Pautas | Mantém a fila de Reels (`queue.json`) com ≥ 3 itens; cada pauta nova vai ao canal para revisão | Mantém a fila de carrosséis (`carrosseis/fila.json`) com ≥ 3 itens; cada pauta nova vai ao canal para revisão |
| Pesquisa | Verifica fatos em fonte primária na própria execução | Verifica fatos em fonte primária na própria execução |
| Produção | Roteiro, cenas (`src/engine.py`), narração, render 9:16, legenda | Slides 4:5 (1080×1350, JPEG) seguindo `prompts/carrossel.md`, legenda, aviso de imagens |
| Arquivos | `src/reelN_*.py`, `videos/`, `src/captions.json` | `carrosseis/<id>/` (slides `01.jpg`…, `legenda.txt`, `fontes.md`) |
| Publicação | Publica o Reel do dia (Windsor) | Publica o carrossel se tiver acesso ao Windsor; **sem acesso, o `claude` aperta o botão** do carrossel aprovado, sem mudar o conteúdo |
| Métricas | Lê o Windsor diariamente e registra Reels e carrosséis | Analisa o desempenho dos carrosséis e contesta a leitura dos Reels |
| Revisão | Revisa **todo carrossel** antes de publicar | Revisa **toda pauta de Reel** e, quando acordado, o roteiro |
| Semanal (domingo) | Revisão PARAR/MANTER/AMPLIAR/TESTAR dos Reels | Revisão PARAR/MANTER/AMPLIAR/TESTAR dos carrosséis |

## 2. Fluxo de cada conteúdo

```
pauta (autor) ──► review do outro (veracidade + público) ──► produção (autor)
     ──► review do conteúdo pronto ──► publicação ──► métricas ──► revisão semanal
```

1. **Pauta:** o autor publica `proposal` em `T-pauta-<slug>` com tema,
   pergunta central, gancho, CTA, fontes (URLs) e o que cada fonte confirma.
2. **Revisão da pauta:** o outro agente responde com `review` e veredito,
   usando a lista da seção 3. Só pauta com `approve` vai para produção.
3. **Produção** pelo autor, com a verificação própria do PLAYBOOK.
4. **Revisão do conteúdo pronto:**
   - **Carrossel:** o `claude` revisa slides, legenda e fontes **antes** de
     publicar; é obrigatório (o `claude` roda todo dia, então não trava).
   - **Reel:** o `chatgpt` revisa o roteiro quando o Rick o acordar antes da
     publicação. Como ele não roda todo dia, a revisão do roteiro não bloqueia o
     Reel diário; a da pauta sim (passo 2).
5. **Publicação** com `claim` de `T-pub-<AAAA-MM-DD>-reel` ou
   `T-pub-<AAAA-MM-DD>-post`, nunca duas vezes o mesmo item.
6. **Pós-publicação:** o outro agente pode revisar o que já foi ao ar. Erro
   factual encontrado vira P0: avisar o Rick e propor a correção (legenda ou
   comentário fixado); nunca apagar post sem decisão do Rick.

**Sem pauta de Reel aprovada no dia:** o `claude` produz a próxima pauta com a
verificação própria, publica e marca na fila `"revisao": "pos-publicacao"`;
o `chatgpt` revisa na próxima sessão.

## 3. Lista de revisão (vale para os dois)

Veredito `approve`, `changes` ou `reject`, dizendo o que foi conferido.

**Veracidade**
- [ ] Afirmação central confirmada em fonte primária ou institucional que o
      revisor **abriu nesta sessão** (link no review).
- [ ] Números, datas, nomes e unidades batem com a fonte; nada arredondado
      além do que ela diz.
- [ ] Fato, hipótese e interpretação separados; a ressalva necessária está no
      conteúdo e na legenda.
- [ ] Nenhuma generalização além do estudo (espécie, condição, amostra).
- [ ] Imagens autorais ou com selo (ilustração / IA / diagrama sem escala);
      nada que imite foto real de experimento, lugar ou objeto.

**Público e tema**
- [ ] "Parece fake, mas é real": surpreende e tem explicação concreta.
- [ ] Interessa a quem fala português; ganha pontos se tiver ligação com o
      Brasil ou com o dia a dia (cozinha, casa, corpo, natureza próxima).
- [ ] Linguagem clara, sem infantilizar e sem jargão; gancho entendível em 3 s.
- [ ] Não repete `temas_usados` (Reels e carrosséis) nem algo publicado
      recentemente pelo outro formato.
- [ ] Fora do escopo: conselho médico ou de saúde, política, tragédias
      recentes, teorias da conspiração, sensacionalismo, marcas.
- [ ] Uma CTA só; até 5 hashtags, incluindo `#PareceFakeEReal`.

`changes` ou `reject` sobre **veracidade** bloqueia até o autor responder. Sobre
**público/tema**, o autor pode discordar com motivo; se não fecharem, vira
`decision-request` para o Rick.

## 4. Rotina de cada agente

**`claude` (rotina diária agendada, PLAYBOOK):**
1. Ler o canal e responder o que estiver para `claude`.
2. Revisar carrosséis com status `pronto` em `carrosseis/fila.json`; publicar
   o que estiver aprovado e cujo autor não tenha acesso ao Windsor.
3. Métricas de Reels e carrosséis no Windsor; registrar em `queue.json` e
   `carrosseis/fila.json`.
4. Produzir e publicar o Reel do dia.
5. Revisar pautas de carrossel novas; propor pautas de Reel novas.

**`chatgpt` (quando o Rick manda `melancia`):**
1. Ler o canal e responder o que estiver para `chatgpt`.
2. Revisar pautas de Reel pendentes (e roteiros, se houver).
3. Produzir o próximo carrossel aprovado e marcá-lo `pronto`; propor pautas
   de carrossel novas.
4. Analisar as métricas de carrosséis registradas e contestar a leitura dos
   Reels.

## 5. Calendário

- **Reel:** 1 por dia, por volta de 07:20 (horário de São Paulo).
- **Carrossel:** sem cota fixa; sai quando houver um aprovado. Sugestão de
  horário: fim da tarde (≈18:00), para não competir com o Reel.
- Os carrosséis antigos tiveram mediana de 3 contas alcançadas (log de
  23–25/10). O formato volta com a regra nova de fechamento e card fixo; depois
  de 6 carrosséis publicados, o `chatgpt` traz a comparação na revisão
  semanal e o Rick decide se mantém, muda ou para.
