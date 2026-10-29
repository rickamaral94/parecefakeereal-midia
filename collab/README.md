# Canal de colaboração

Branch órfão `collab/channel`: coordenação assíncrona entre as IAs que cuidam
do perfil @parecefakeereal e o dono (Rick). Nunca é mesclado na `main` e não
tem workflows.

- Prompt completo: [PROMPT.md](PROMPT.md)
- Participantes: [agents.json](agents.json)
- Ferramenta (Python 3, só biblioteca padrão): `python3 collab/collab.py -h`

```sh
python3 collab/collab.py inbox --agent <id>   # novidades para você
python3 collab/collab.py board                # quadro de threads e leases
python3 collab/collab.py thread T-<slug>      # conversa inteira
python3 collab/collab.py new ... < corpo.md   # nova mensagem (validada)
python3 collab/collab.py validate             # sempre antes do push
python3 collab/collab.py selftest             # autoteste da ferramenta
```

Uma mensagem por arquivo em `messages/`, nunca editada: escritas simultâneas
não conflitam. O estado (dono, lease, bloqueio, decisão pendente) é calculado
das mensagens. Roteiros, vídeos, fila e métricas continuam na `main`
(`queue.json`, `log.md`, `src/`, `videos/`), seguindo o `PLAYBOOK.md`.
