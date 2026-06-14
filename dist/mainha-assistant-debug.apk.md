# Registro de alteracoes - `mainha-assistant-debug.apk`

Arquivo base: `dist/mainha-assistant-debug.apk`
Arquivo de registro: `dist/mainha-assistant-debug.apk.md`
Status no Git antes do commit: Novo
Data do registro: 2026-06-14
Area do projeto: Distribuicao/artefatos gerados.
Tipo: APK/artefato binario gerado
Tamanho atual: 1505631 bytes; binario ou nao textual; sha256 curto: `9be1d4a7ef1613c2`

## Alteracao registrada

APK debug do Mainha Assistant atualizado e recompilado com `MAINHA_BACKEND_URL=https://mainha-assistant-backend.onrender.com`, apontando o app Android para o backend hospedado no Render. O token `ASSISTANT_AUTH_TOKEN` nao foi embutido no APK; deve ser informado no campo de token do app quando a autenticacao estiver ativa no backend.

## Regra de manutencao

Este arquivo `.md` deve ser atualizado sempre que o arquivo base `dist/mainha-assistant-debug.apk` receber qualquer alteracao antes de commit/push. Registre aqui o que mudou, por que mudou e qualquer impacto esperado em build, execucao, deploy, testes ou artefatos gerados.

## Observacoes para commit

- Conferir se o arquivo base deve mesmo entrar no commit.
- Para binarios e artefatos gerados, confirmar se o repositorio deve versionar esse conteudo.
- Para arquivos com tokens, endpoints ou configuracoes, confirmar que nenhum segredo real foi incluido.
