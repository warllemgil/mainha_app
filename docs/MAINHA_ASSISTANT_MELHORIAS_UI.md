# Mainha Assistant - Plano de Melhorias de Interface e Acesso

## Objetivo

Reduzir atrito no uso diario do app Android e da interface do Mainha Assistant, eliminando a necessidade de digitar o token a cada abertura e tornando a tela inicial mais direta para falar, ouvir e revisar respostas.

## Problema atual

- O usuario precisa preencher o token do backend manualmente quando o backend usa autenticacao.
- A tela atual funciona, mas ainda exige configuracao demais antes do primeiro uso.
- O acesso ao assistente nao tem um fluxo de desbloqueio simples para uso recorrente no celular.

## Proposta

1. Guardar o token do backend de forma local e protegida.
2. Desbloquear o token com uma senha curta, PIN ou biometria antes de usar o app.
3. Manter o token oculto na interface normal.
4. Separar claramente "conectar", "falar", "enviar" e "ouvir resposta".
5. Reduzir campos visiveis na primeira tela e deixar configuracoes avancadas em uma area secundaria.

## Fluxo sugerido

1. Usuario abre o app.
2. O app mostra a tela principal com estado de conexao e um botao de desbloqueio.
3. Usuario digita a senha local ou usa biometria.
4. O app libera o token armazenado de forma segura.
5. O assistente fica pronto para uso sem novo preenchimento de credenciais.
6. O token pode ser bloqueado novamente por timeout, saida do app ou bloqueio manual.

## Melhorias de interface

- Tela inicial mais limpa, com foco no botao de fala.
- Indicador visivel de backend conectado, autenticado e pronto.
- Area de resposta com historico curto da conversa.
- Botao unico de acao principal e botoes secundarios menores para configuracao.
- Ajuste visual para reduzir cliques ate a primeira interacao util.

## Melhorias de seguranca

- Armazenar o token em `EncryptedSharedPreferences` ou equivalente no Android.
- Proteger o desbloqueio com senha, PIN ou biometria.
- Nao exibir o token na tela principal.
- Permitir limpar o token salvo.
- Manter a senha local apenas no dispositivo.

## Sequencia recomendada

1. Implementar armazenamento local protegido do token.
2. Adicionar tela de desbloqueio.
3. Reorganizar a tela principal do app Android.
4. Tornar o fluxo de fala/resposta mais direto.
5. Revisar contraste, espaçamento e hierarquia visual.
6. Validar no celular fisico com backend Render.

## Resultado esperado

O app deve abrir pronto para uso diario, sem exigir redigitar token toda vez, e a interface deve ficar mais objetiva para falar com o assistente em poucos toques.
