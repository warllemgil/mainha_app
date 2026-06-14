# Registro de alteracoes - `config.py`

Arquivo base: `backend/app/config.py`
Arquivo de registro: `backend/app/config.py.md`
Status no Git antes do commit: Novo
Data do registro: 2026-06-14
Area do projeto: Backend FastAPI do Mainha Assistant.
Tipo: Codigo-fonte
Tamanho atual: 2140 bytes; 78 linhas; sha256 curto: `af508b80942cb3f5`

## Alteracao registrada

Atualizado o valor padrao de `GEMINI_MODEL` para `gemini-3.5-flash` e removida a dependencia de `GEMINI_API_BASE_URL` da configuracao, alinhando o backend com a SDK nova da Google.

## Regra de manutencao

Este arquivo `.md` deve ser atualizado sempre que o arquivo base `backend/app/config.py` receber qualquer alteracao antes de commit/push. Registre aqui o que mudou, por que mudou e qualquer impacto esperado em build, execucao, deploy, testes ou artefatos gerados.

## Observacoes para commit

- Conferir se o arquivo base deve mesmo entrar no commit.
- Para binarios e artefatos gerados, confirmar se o repositorio deve versionar esse conteudo.
- Para arquivos com tokens, endpoints ou configuracoes, confirmar que nenhum segredo real foi incluido.
