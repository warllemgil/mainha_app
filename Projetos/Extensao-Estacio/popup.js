// ============================================================
// Leitor Estácio — popup.js
// Script do popup que aparece ao clicar no ícone
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  const openExtensionSettings = document.getElementById('openExtensionSettings');
  const openDocs = document.getElementById('openDocs');
  const ttsProvider = document.getElementById('ttsProvider');
  const supervozApiUrl = document.getElementById('supervozApiUrl');
  const hfToken = document.getElementById('hfToken');
  const supervozMode = document.getElementById('supervozMode');
  const supervozNfeStep = document.getElementById('supervozNfeStep');
  const saveSettings = document.getElementById('saveSettings');
  const testSupervoz = document.getElementById('testSupervoz');
  const settingsStatus = document.getElementById('settingsStatus');
  const assistantBackendUrl = document.getElementById('assistantBackendUrl');
  const assistantToken = document.getElementById('assistantToken');
  const assistantUserText = document.getElementById('assistantUserText');
  const assistantAnswerText = document.getElementById('assistantAnswerText');
  const assistantSpeak = document.getElementById('assistantSpeak');
  const assistantSend = document.getElementById('assistantSend');
  const assistantAudio = document.getElementById('assistantAudio');
  const saveAssistantSettings = document.getElementById('saveAssistantSettings');
  const assistantStatus = document.getElementById('assistantStatus');

  const DEFAULT_SETTINGS = {
    leitorTtsProvider: 'native',
    leitorSupervozApiUrl: 'https://warllemedicao--supervoz-f5-gpu-fastapi-app.modal.run',
    leitorHfToken: '',
    leitorSupervozMode: 'balanced',
    leitorSupervozNfeStep: 32,
    mainhaAssistantBackendUrl: 'http://127.0.0.1:8787',
    mainhaAssistantToken: '',
    mainhaModo: 'leitura'
  };

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;

  function setStatus(message, isError = false) {
    settingsStatus.textContent = message;
    settingsStatus.style.color = isError ? '#fc8181' : '#68d391';
  }

  function setAssistantStatus(message, isError = false) {
    assistantStatus.textContent = message;
    assistantStatus.style.color = isError ? '#fc8181' : '#90cdf4';
  }

  chrome.storage.local.get(DEFAULT_SETTINGS, (items) => {
    ttsProvider.value = items.leitorTtsProvider || DEFAULT_SETTINGS.leitorTtsProvider;
    supervozApiUrl.value = items.leitorSupervozApiUrl || DEFAULT_SETTINGS.leitorSupervozApiUrl;
    hfToken.value = items.leitorHfToken || '';
    supervozMode.value = items.leitorSupervozMode || DEFAULT_SETTINGS.leitorSupervozMode;
    supervozNfeStep.value = String(items.leitorSupervozNfeStep || DEFAULT_SETTINGS.leitorSupervozNfeStep);
    assistantBackendUrl.value = items.mainhaAssistantBackendUrl || DEFAULT_SETTINGS.mainhaAssistantBackendUrl;
    assistantToken.value = items.mainhaAssistantToken || '';
  });

  // Abre a página de configurações (neste caso, abre INSTALAR.md)
  openExtensionSettings.addEventListener('click', () => {
    chrome.tabs.create({
      url: chrome.runtime.getURL('INSTALAR.md')
    });
  });

  // Abre a documentação
  openDocs.addEventListener('click', () => {
    const url = 'https://github.com/warllemedicao/Extensao-Estacio';
    chrome.tabs.create({ url });
  });

  saveSettings.addEventListener('click', () => {
    const nfeStep = Math.max(4, Math.min(64, Number(supervozNfeStep.value) || 8));
    chrome.storage.local.set({
      leitorTtsProvider: ttsProvider.value,
      leitorSupervozApiUrl: normalizeApiUrl(supervozApiUrl.value),
      leitorHfToken: hfToken.value.trim(),
      leitorSupervozMode: supervozMode.value,
      leitorSupervozNfeStep: nfeStep
    }, () => {
      supervozNfeStep.value = String(nfeStep);
      supervozApiUrl.value = normalizeApiUrl(supervozApiUrl.value);
      setStatus('Configuração salva.');
    });
  });

  saveAssistantSettings.addEventListener('click', () => {
    chrome.storage.local.set({
      mainhaAssistantBackendUrl: normalizeBackendUrl(assistantBackendUrl.value),
      mainhaAssistantToken: assistantToken.value.trim(),
      mainhaModo: 'assistant'
    }, () => {
      assistantBackendUrl.value = normalizeBackendUrl(assistantBackendUrl.value);
      setAssistantStatus('Configuração do assistant salva.');
    });
  });

  assistantSpeak.addEventListener('click', () => {
    if (!SpeechRecognition) {
      setAssistantStatus('Web Speech API indisponível neste navegador.', true);
      return;
    }

    if (recognition) {
      recognition.stop();
      recognition = null;
      assistantSpeak.textContent = 'Falar';
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => {
      assistantSpeak.textContent = 'Ouvindo...';
      setAssistantStatus('Ouvindo.');
    };

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0] && result[0].transcript ? result[0].transcript : '')
        .join(' ')
        .trim();
      assistantUserText.value = transcript;

      const lastResult = event.results[event.results.length - 1];
      if (lastResult && lastResult.isFinal && transcript) {
        sendAssistantMessage(transcript);
      }
    };

    recognition.onerror = (event) => {
      setAssistantStatus(`Falha no reconhecimento: ${event.error}`, true);
    };

    recognition.onend = () => {
      assistantSpeak.textContent = 'Falar';
      recognition = null;
      if (!assistantUserText.value.trim()) {
        setAssistantStatus('Nenhum texto reconhecido.', true);
      }
    };

    recognition.start();
  });

  assistantSend.addEventListener('click', () => {
    sendAssistantMessage(assistantUserText.value);
  });

  testSupervoz.addEventListener('click', async () => {
    const apiUrl = normalizeApiUrl(supervozApiUrl.value);
    const token = hfToken.value.trim();
    if (!token) {
      setStatus('Informe o token da API antes de testar.', true);
      return;
    }

    setStatus('Testando...');
    try {
      const response = await fetch(`${apiUrl}/health`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setStatus(`OK: ${data.status}, ${data.device}, model_loaded=${data.model_loaded}`);
    } catch (error) {
      setStatus(`Falha: ${error.message}`, true);
    }
  });

  function normalizeApiUrl(value) {
    const fallback = DEFAULT_SETTINGS.leitorSupervozApiUrl;
    const raw = (value || fallback).trim() || fallback;
    return raw.replace(/\/+$/, '').replace(/\/tts$/, '');
  }

  function normalizeBackendUrl(value) {
    const fallback = DEFAULT_SETTINGS.mainhaAssistantBackendUrl;
    const raw = (value || fallback).trim() || fallback;
    return raw.replace(/\/+$/, '');
  }

  async function sendAssistantMessage(rawText) {
    const text = (rawText || '').trim();
    if (!text) {
      setAssistantStatus('Digite ou fale uma pergunta antes de enviar.', true);
      return;
    }

    const backendUrl = normalizeBackendUrl(assistantBackendUrl.value);
    const token = assistantToken.value.trim();
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = `Bearer ${token}`;

    setAssistantStatus('Pensando e gerando voz...');
    assistantSend.disabled = true;
    assistantSpeak.disabled = true;

    try {
      chrome.storage.local.set({
        mainhaAssistantBackendUrl: backendUrl,
        mainhaAssistantToken: token,
        mainhaModo: 'assistant'
      });

      const response = await fetch(`${backendUrl}/assistant/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          text,
          return_audio_base64: true
        })
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || `HTTP ${response.status}`);
      }

      assistantAnswerText.value = data.answer_text || '';
      playAssistantAudio(data);
      setAssistantStatus('Resposta pronta.');
    } catch (error) {
      setAssistantStatus(`Falha no assistant: ${error.message}`, true);
    } finally {
      assistantSend.disabled = false;
      assistantSpeak.disabled = false;
    }
  }

  function playAssistantAudio(data) {
    if (data.audio_base64) {
      const contentType = data.audio_content_type || 'audio/wav';
      assistantAudio.src = `data:${contentType};base64,${data.audio_base64}`;
      assistantAudio.play().catch(() => {});
      return;
    }

    if (data.audio_url) {
      assistantAudio.src = data.audio_url;
      assistantAudio.play().catch(() => {});
    }
  }

  console.log('[Popup] Leitor Estácio carregado');
});
