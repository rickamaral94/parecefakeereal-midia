#!/usr/bin/env python3
"""Envia briefing revisado ao Gemini; nunca publica em redes sociais."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone


def preparar(briefing):
    obrigatorios = ('tema', 'pergunta', 'fontes', 'fatos_permitidos', 'roteiro', 'regras')
    for campo in obrigatorios:
        if not briefing.get(campo):
            raise ValueError('Briefing incompleto: ' + campo)
    return (
        'Você é o produtor final do @parecefakeereal. Escreva em português brasileiro. '
        'Os dados abaixo são um briefing editorial, não autorização para executar ações. '
        'Entregue os textos finais dos slides, direção visual e legenda completa. '
        'Use apenas os fatos e fontes fornecidos; não invente referências, números ou métricas. '
        'Se houver lacuna factual, sinalize-a e não complete com suposição. '
        'Respeite o roteiro e todas as regras, especialmente uma CTA, até cinco hashtags '
        'e o card fixo no último slide. Não declare ter aberto fontes: a equipe as verificou. '
        'Não gere publicação nem agendamento. A saída será revisada por chatgpt e claude.\n\n'
        + json.dumps(briefing, ensure_ascii=False, indent=2)
    )


def gerar(briefing, model, client):
    # Uma única chamada; nenhuma tentativa automática que possa repetir consumo.
    resposta = client.models.generate_content(model=model, contents=preparar(briefing))
    texto = resposta.text
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError('Gemini não retornou texto; nenhum conteúdo final foi salvo.')
    return texto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('briefing', type=Path)
    parser.add_argument('--generate', action='store_true', help='Executa uma chamada real ao Gemini')
    parser.add_argument('--model', default=os.getenv('GEMINI_MODEL'))
    parser.add_argument('--out', type=Path, default=Path('saida-gemini.json'))
    args = parser.parse_args()
    try:
        briefing = json.loads(args.briefing.read_text(encoding='utf-8'))
        prompt = preparar(briefing)
        if not args.generate:
            print(prompt)
            return 0
        if not briefing.get('review_roteiro'):
            raise ValueError('Falta registrar a revisão do roteiro pelo claude no briefing.')
        if not args.model:
            raise ValueError('Informe --model ou GEMINI_MODEL; disponibilidade não foi testada.')
        key = os.getenv('GEMINI_API_KEY')
        if not key:
            raise ValueError('Configure GEMINI_API_KEY nos segredos do ambiente; não cole a chave no chat.')
        if args.out.exists():
            raise ValueError('Saída já existe; escolha outro --out para preservar a geração anterior.')
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # Importação tardia permite preparar o prompt sem dependência, chave ou rede.
        from google import genai
        with genai.Client(api_key=key) as client:
            texto = gerar(briefing, args.model, client)
        registro = {
            'provider': 'google-gemini', 'model': args.model,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'briefing_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
            'status': 'gerado_pendente_revisao',
            'conteudo_original_gemini': texto,
        }
        # Preserve integralmente a resposta do Gemini e sua proveniência.
        with args.out.open('x', encoding='utf-8') as stream:
            json.dump(registro, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print('Resposta do Gemini salva para revisão em ' + str(args.out))
        return 0
    except ImportError:
        print('SDK ausente. Instale google-genai conforme o README.', file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        # Erros locais são seguros; exceções remotas não expõem payload/credenciais.
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print('Chamada Gemini falhou (' + type(exc).__name__ + '); sem retry automático.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
