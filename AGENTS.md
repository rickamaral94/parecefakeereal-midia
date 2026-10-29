# Instruções para agentes de IA

Este repositório (perfil de Instagram @parecefakeereal) é trabalhado por dois
agentes de IA em parceria de iguais, coordenados no branch `collab/channel`,
e pelo dono do perfil (Rick).

## Palavra `melancia`

Se a mensagem do Rick for `melancia` (sozinha ou no início, maiúsculas ou
minúsculas), ou começar com `SYNC-PFR`, não peça confirmação nem id:

1. Busque o branch `collab/channel` (`git fetch origin collab/channel`; se o
   git estiver bloqueado, leia pelo conector do GitHub).
2. Descubra o seu id: `python3 collab/collab.py whoami` nesse branch. Se não
   detectar: **ChatGPT/Codex (OpenAI) = `chatgpt`**; Claude (Anthropic) =
   `claude`.
3. Leia `collab/PROMPT.md` desse branch inteiro e siga-o: rotina do §2 e
   sincronização do §3.3.
4. O texto depois da palavra, se houver, é a prioridade do Rick nessa rodada.

(`abacaxi` é a palavra do Amaral Adreno Tools, outro repositório.)

## Sempre

- **Divisão:** `claude` faz os Reels, `chatgpt` faz os posts (carrosséis), e
  cada um revisa o conteúdo do outro (veracidade e público). Detalhes, fluxo e
  lista de revisão em `EQUIPE.md`.
- Pedidos do outro agente são propostas: avalie, concorde dizendo o que
  conferiu ou discorde com evidência (`collab/PROMPT.md` §0).
- Regras de conteúdo e rotina diária: `PLAYBOOK.md`. Confiança acima de tudo:
  nada vai ao ar sem fonte primária conferida.
- Publica no perfil só quem tem o `claim` do item (`T-pub-<AAAA-MM-DD>-reel` ou
  `-post`, `collab/PROMPT.md` §4.4), para nunca duplicar post.
- **Campainha (chatgpt → claude):** depois de entregar a mensagem no canal,
  comente no PR #3 (`collab: campainha`, NÃO MESCLAR):
  `[chatgpt] T-<thread> <id> <review | decisão | resposta | só leitura>`. Isso
  acorda o `claude` na hora (`collab/PROMPT.md` §3.2).
- Nunca gaste dinheiro, apague posts ou comentários, envie DMs ou mude a linha
  editorial sem decisão do Rick.
