# Registro de alteracoes - `render.yaml`

Arquivo base: `render.yaml`
Arquivo de registro: `render.yaml.md`
Status no Git antes do commit: Novo
Data do registro: 2026-06-14
Area do projeto: Hospedagem do backend Mainha Assistant.
Tipo: Blueprint Render

## Alteracao registrada

Adicionado blueprint do Render para hospedar o backend FastAPI no plano gratuito, apontando `rootDir` para `backend`, instalando `backend/requirements.txt`, iniciando `uvicorn` com a porta `$PORT` do Render e declarando variaveis de ambiente. Segredos como `GEMINI_API_KEY`, `SUPERVOZ_API_TOKEN` e `ASSISTANT_AUTH_TOKEN` ficam com `sync: false`, portanto precisam ser preenchidos no Render.

## Regra de manutencao

Este arquivo `.md` deve ser atualizado sempre que o arquivo base `render.yaml` receber qualquer alteracao antes de commit/push. Registre aqui o que mudou, por que mudou e qualquer impacto esperado em build, execucao, deploy, testes ou artefatos gerados.

## Observacoes para commit

- Conferir se os valores publicos continuam corretos para o backend.
- Nunca colocar a chave Gemini diretamente no `render.yaml`.
- Confirmar no painel do Render que os segredos foram preenchidos antes do primeiro deploy.
