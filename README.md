# Mainha

Mainha e a base da extensao Chrome que le paginas em voz alta usando voz nativa do navegador ou SuperVoz F5. Esta versao tambem inicia o MVP do **Mainha Assistant**, um assistente conversacional leve com Gemini no backend e resposta falada pela SuperVoz.

## Estrutura principal

- `Projetos/Extensao-Estacio/`: extensao Chrome Manifest V3.
- `SuperVoz-F5-Space/`: API SuperVoz F5 usada em Modal/Space, com `/tts` retornando WAV.
- `SuperVoz-F5-Server/`: servidor local SuperVoz F5.
- `backend/`: novo orquestrador FastAPI do Mainha Assistant.
- `android-app/`: app Android nativo leve para testar o assistente no celular.
- `dist/mainha-assistant-debug.apk`: APK debug gerado para instalacao manual.
- `docs/MAINHA_ASSISTANT_PLANO.md`: plano tecnico da nova fase.

## Rodar o backend do Assistant

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Edite `backend/.env` antes de usar:

- `GEMINI_API_KEY`: chave Gemini, somente no backend.
- `SUPERVOZ_API_URL`: URL base da SuperVoz F5.
- `SUPERVOZ_API_TOKEN`: token SuperVoz, se exigido.
- `ASSISTANT_AUTH_TOKEN`: opcional para proteger o orquestrador.

## Usar a extensao

1. Abra `chrome://extensions`.
2. Ative o modo desenvolvedor.
3. Clique em "Carregar sem compactacao".
4. Selecione `Projetos/Extensao-Estacio/`.
5. No popup, mantenha a leitura de pagina como antes ou configure `Mainha Assistant` com `http://127.0.0.1:8787`.

## Endpoints do Assistant

- `GET /health`
- `POST /assistant/chat`
- `POST /assistant/voice`
- `POST /assistant/tools`

Detalhes tecnicos e sequencia de evolucao estao em `docs/MAINHA_ASSISTANT_PLANO.md`.

## APK Android

O APK de teste fica em:

```bash
dist/mainha-assistant-debug.apk
```

Para gerar novamente localmente:

```bash
cd android-app
MAINHA_BACKEND_URL="http://SEU_IP_OU_DOMINIO:8787" \
MAINHA_ASSISTANT_TOKEN="" \
gradle assembleDebug --no-daemon
cp app/build/outputs/apk/debug/app-debug.apk ../dist/mainha-assistant-debug.apk
```

Para baixar pelo GitHub, configure os Secrets `MAINHA_BACKEND_URL` e, se usar autenticacao, `MAINHA_ASSISTANT_TOKEN`. Depois rode o workflow **Build Android APK** na aba Actions. O artefato gerado se chama `mainha-assistant-debug-apk`.
