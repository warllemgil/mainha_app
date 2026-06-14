# Mainha Assistant Backend

Backend orquestrador FastAPI para o MVP do Mainha Assistant.

Fluxo:

1. Recebe texto ja transcrito da extensao/app.
2. Chama Gemini pelo backend.
3. Envia a resposta textual para a SuperVoz F5.
4. Retorna texto e audio em base64 para o frontend tocar.

## Rodar localmente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite `.env` com `GEMINI_API_KEY`, `GEMINI_MODEL` e `SUPERVOZ_API_URL`. O modelo padrao atual e `gemini-3.5-flash`.

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Teste:

```bash
curl http://127.0.0.1:8787/health
curl -X POST http://127.0.0.1:8787/assistant/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"Bom dia, Mainha. Resuma o que voce consegue fazer."}'
```

Se `ASSISTANT_AUTH_TOKEN` estiver configurado, envie:

```bash
-H "Authorization: Bearer SEU_TOKEN"
```

## Endpoints

- `GET /health`: status e configuracoes carregadas sem expor segredos.
- `POST /assistant/chat`: texto do usuario -> Gemini -> SuperVoz -> texto + audio.
- `POST /assistant/voice`: placeholder para audio bruto. No MVP, prefira Web Speech API no frontend e use `/assistant/chat`.
- `POST /assistant/tools`: reserva para acoes futuras com execucao segura.

## Gemini atual

O backend usa a SDK nova `google-genai` e chama `client.models.generate_content(...)` com o modelo configurado em `GEMINI_MODEL`.

## Seguranca

Nunca coloque `GEMINI_API_KEY` na extensao Chrome. A chave fica somente no `.env` do backend. O token da SuperVoz tambem deve ficar no backend quando o modo assistente estiver em uso.
