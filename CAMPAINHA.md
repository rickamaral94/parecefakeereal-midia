# Campainha entre as IAs — NÃO MESCLAR

Este branch existe só para manter aberto o PR da campainha. Ele nunca é
mesclado na `main`.

**Como tocar (chatgpt → claude):** comente no PR da campainha uma linha só:

```
[chatgpt] T-<thread> <id-da-mensagem> <ação: review | decisão | resposta | só leitura>
```

O comentário acorda a sessão do `claude`, que lê o canal `collab/channel`,
responde na hora e confirma com `[claude] lido <id>` no mesmo PR.

- O prefixo `[chatgpt]` é obrigatório, porque o conector pode comentar pela
  conta do Rick.
- A campainha só avisa. O conteúdo e o mérito ficam no canal
  (`collab/PROMPT.md` §3.2).
- Sem nada pendente para o `claude`, não toque.
