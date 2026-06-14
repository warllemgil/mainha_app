# Mainha Assistant Android

App Android nativo leve para testar o fluxo:

Usuario fala -> STT Android -> backend Mainha Assistant -> Gemini -> SuperVoz F5 -> audio no celular.

O APK pode sair pronto para uso se voce embutir a URL do seu backend no build. A chave Gemini e o token SuperVoz continuam no backend.

## Build pelo GitHub

1. Envie este repositorio para o GitHub.
2. Em **Settings > Secrets and variables > Actions**, crie:
   - `MAINHA_BACKEND_URL`: URL publica ou da sua rede para o backend.
   - `MAINHA_ASSISTANT_TOKEN`: opcional, somente se `ASSISTANT_AUTH_TOKEN` estiver configurado no backend.
3. Abra a aba **Actions**.
4. Rode o workflow **Build Android APK**.
5. Baixe o artefato `mainha-assistant-debug-apk`.
6. Instale `app-debug.apk` no celular.

Com esses secrets, o app ja abre apontando para o backend correto. O botao **Configuracoes** fica disponivel apenas para ajustes de teste.

## APK local

Nesta etapa tambem foi gerado:

```bash
../dist/mainha-assistant-debug.apk
```

Para recompilar:

```bash
MAINHA_BACKEND_URL="http://SEU_IP_OU_DOMINIO:8787" \
MAINHA_ASSISTANT_TOKEN="" \
gradle assembleDebug --no-daemon
cp app/build/outputs/apk/debug/app-debug.apk ../dist/mainha-assistant-debug.apk
```

## URL do backend no celular

O APK chama a URL configurada na tela inicial.

- Em emulador Android: `http://10.0.2.2:8787`.
- Em celular fisico na mesma rede: use o IP do computador/servidor, por exemplo `http://192.168.1.50:8787`.
- Se hospedar o backend online, use a URL HTTPS dele.

O Gemini e o token SuperVoz ficam somente no backend. O app pode usar apenas `ASSISTANT_AUTH_TOKEN`, se voce configurar essa protecao no backend.
