# Mainha Assistant - Plano Tecnico

## 1. Arquitetura atual da extensao

A extensao Chrome ativa fica em `Projetos/Extensao-Estacio/` e usa Manifest V3.

- `manifest.json`: declara MV3, `storage`, `activeTab`, `scripting`, `offscreen`, permissoes HTTP/HTTPS e injeta `content.js` + `player.css`.
- `popup.html`: interface de configuracao da extensao.
- `popup.js`: salva configuracoes em `chrome.storage.local`.
- `content.js`: injeta o player flutuante na pagina, extrai blocos de texto, conversa com iframes via `postMessage`, chama TTS nativo ou SuperVoz F5, faz cache/prefetch e toca audio.
- `player.css`: estilo do player flutuante.

Configuracoes atuais importantes:

- `leitorTtsProvider`: alterna entre voz nativa e SuperVoz.
- `leitorSupervozApiUrl`: URL base da SuperVoz F5.
- `leitorHfToken`: token Bearer usado pela extensao para chamar a SuperVoz.
- `leitorSupervozMode`: `fast`, `balanced` ou `quality`.
- `leitorSupervozNfeStep`: passos de inferencia do F5.

Contrato atual da SuperVoz usado pela extensao:

- `POST {SUPERVOZ_API_URL}/tts`
- Headers: `Content-Type: application/json`, `Authorization: Bearer <token>` quando configurado.
- Body: `voice`, `text`, `speed`, `mode`, `nfe_step`.
- Resposta preferida no Space/Modal atual: audio WAV binario (`audio/wav`) tocado com `new Audio(URL.createObjectURL(blob))`.

## 2. Arquitetura nova proposta

O Mainha Assistant adiciona um backend orquestrador leve em `backend/`, sem substituir a SuperVoz F5.

Componentes:

- Extensao/Web app: captura fala, faz STT no frontend via Web Speech API no MVP, mostra texto/resposta e toca audio.
- Backend Mainha Assistant: recebe texto, chama Gemini, chama SuperVoz e retorna resposta.
- Gemini API: cerebro conversacional e futura camada de tool calling.
- SuperVoz F5: TTS com voz neural personalizada.

O backend passa a guardar segredos:

- `GEMINI_API_KEY` nunca fica na extensao.
- `SUPERVOZ_API_TOKEN` pode ficar no backend para o modo assistente.
- `ASSISTANT_AUTH_TOKEN` pode proteger chamadas da extensao/app ao backend.

## 3. Fluxo completo de voz

1. Usuario clica em "Falar" no popup ou app.
2. Frontend usa Web Speech API para transformar fala em texto.
3. Frontend envia `POST /assistant/chat` para o backend.
4. Backend envia texto para Gemini.
5. Gemini retorna resposta textual.
6. Backend envia a resposta para `POST /tts` da SuperVoz F5.
7. SuperVoz retorna WAV binario ou JSON com audio.
8. Backend retorna `answer_text` e `audio_base64` ou `audio_url`.
9. Frontend mostra a resposta e toca o audio.

`POST /assistant/voice` fica criado para evolucao futura, mas o MVP recomenda STT no frontend para reduzir complexidade.

## 4. Arquivos reaproveitados

- `Projetos/Extensao-Estacio/content.js`: mantem leitura de pagina, extracao de texto, cache e playback SuperVoz.
- `Projetos/Extensao-Estacio/popup.html`: recebe nova area do Assistant.
- `Projetos/Extensao-Estacio/popup.js`: passa a salvar URL/token do backend e chamar `/assistant/chat`.
- `Projetos/Extensao-Estacio/manifest.json`: mantem MV3 e permissoes existentes.
- `SuperVoz-F5-Space/app.py`: referencia principal do contrato `/tts` com audio WAV.
- `SuperVoz-F5-Server/server.py`: referencia local do servidor F5.

## 5. Arquivos novos criados

- `backend/app/main.py`: endpoints FastAPI.
- `backend/app/config.py`: leitura de variaveis de ambiente.
- `backend/app/services/gemini_service.py`: camada isolada Gemini.
- `backend/app/services/supervoz_service.py`: camada isolada SuperVoz.
- `backend/app/services/stt_service.py`: ponto substituivel de STT.
- `backend/app/services/tools_service.py`: estrutura futura de ferramentas.
- `backend/app/schemas/assistant_schema.py`: schemas Pydantic.
- `backend/app/utils/audio_utils.py`: utilitarios de audio.
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/README.md`

## 6. Variaveis de ambiente necessarias

- `GEMINI_API_KEY`: chave Gemini no backend.
- `GEMINI_MODEL`: modelo Gemini, padrao `gemini-3.5-flash`.
- `SUPERVOZ_API_URL`: URL base da SuperVoz F5.
- `SUPERVOZ_API_TOKEN`: token Bearer da SuperVoz, se exigido.
- `SUPERVOZ_VOICE`: voz, padrao `warllem`.
- `SUPERVOZ_MODE`: `fast`, `balanced` ou `quality`.
- `SUPERVOZ_NFE_STEP`: passos de inferencia.
- `SUPERVOZ_SPEED`: velocidade.
- `ASSISTANT_AUTH_TOKEN`: token opcional do orquestrador.
- `CORS_ALLOW_ORIGINS`: origens permitidas.
- `STT_PROVIDER`: `frontend` no MVP.
- `REQUEST_TIMEOUT_SECONDS`: timeout para Gemini/SuperVoz.

## 7. Riscos tecnicos

- Latencia: Gemini + F5 podem somar varios segundos por resposta.
- Custo: chamadas frequentes ao F5/Gemini devem ter limites e logs.
- CORS/Auth: a extensao precisa conseguir chamar o backend local/remoto sem expor segredos sensiveis.
- STT Web Speech API: depende do suporte do navegador e pode variar por plataforma.
- Formato da SuperVoz: hoje o Space retorna WAV binario; o servidor local antigo retorna JSON com caminho local. O orquestrador ja aceita binario, `audio_base64` ou `audio_url`, mas URL local pode nao ser acessivel ao frontend.
- Tool calling: antes de executar acoes reais, sera necessario allowlist, auditoria, confirmacao e limites de seguranca.

## 8. Sequencia de desenvolvimento recomendada

1. Rodar backend local e validar `/health`.
2. Configurar `.env` com Gemini e SuperVoz.
3. Testar `/assistant/chat` via `curl`.
4. Carregar extensao em modo desenvolvedor no Chrome.
5. Configurar URL do backend no popup (`http://127.0.0.1:8787`).
6. Testar "Falar" com Web Speech API.
7. Medir latencia e ajustar prompt, `SUPERVOZ_MODE` e `SUPERVOZ_NFE_STEP`.
8. Adicionar historico curto de conversa por `session_id`.
9. Implementar tools apenas com allowlist e dry-run primeiro.
10. Avaliar app Android ou PWA depois do MVP web/extensao estar estavel.
