package br.com.mainha.assistant;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.text.InputType;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Locale;

import javax.net.ssl.HttpsURLConnection;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {
    private static final int REQUEST_SPEECH = 10;
    private static final int REQUEST_RECORD_AUDIO = 11;

    private EditText backendUrlInput;
    private EditText tokenInput;
    private EditText userTextInput;
    private TextView answerText;
    private TextView statusText;
    private Button speakButton;
    private Button sendButton;
    private Button settingsButton;
    private LinearLayout settingsPanel;
    private MediaPlayer mediaPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
        loadSettings();
    }

    private void buildUi() {
        int bg = Color.rgb(16, 24, 32);
        int panel = Color.rgb(24, 35, 45);
        int text = Color.rgb(235, 244, 245);
        int muted = Color.rgb(150, 170, 180);
        int accent = Color.rgb(0, 183, 194);
        int coral = Color.rgb(255, 112, 96);

        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(bg);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(24), dp(20), dp(24));
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        scroll.addView(root);

        ImageView logo = new ImageView(this);
        logo.setImageResource(getResources().getIdentifier("mainha_assistant_logo", "drawable", getPackageName()));
        LinearLayout.LayoutParams logoParams = new LinearLayout.LayoutParams(dp(112), dp(112));
        logoParams.bottomMargin = dp(14);
        root.addView(logo, logoParams);

        TextView title = label("Mainha Assistant", 28, text);
        title.setGravity(Gravity.CENTER);
        root.addView(title);

        TextView subtitle = label("Gemini + sua voz neural SuperVoz F5", 14, muted);
        subtitle.setGravity(Gravity.CENTER);
        subtitle.setPadding(0, dp(4), 0, dp(18));
        root.addView(subtitle);

        backendUrlInput = input("URL do backend", false);
        tokenInput = input("Token do backend (opcional)", true);
        userTextInput = multiInput("Fale ou digite sua pergunta");
        answerText = label("A resposta da IA aparecerá aqui.", 16, text);
        answerText.setBackgroundColor(panel);
        answerText.setPadding(dp(14), dp(14), dp(14), dp(14));

        statusText = label("Pronto.", 13, muted);

        root.addView(fieldLabel("Texto reconhecido", muted));
        root.addView(userTextInput);

        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.setPadding(0, dp(12), 0, dp(12));
        root.addView(actions);

        speakButton = button("Falar", accent);
        sendButton = button("Enviar", coral);
        actions.addView(speakButton, new LinearLayout.LayoutParams(0, dp(48), 1));
        LinearLayout.LayoutParams sendParams = new LinearLayout.LayoutParams(0, dp(48), 1);
        sendParams.leftMargin = dp(10);
        actions.addView(sendButton, sendParams);

        root.addView(fieldLabel("Resposta", muted));
        root.addView(answerText, new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        root.addView(statusText);

        settingsButton = button("Configurações", Color.rgb(45, 60, 70));
        LinearLayout.LayoutParams settingsButtonParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, dp(44));
        settingsButtonParams.topMargin = dp(18);
        root.addView(settingsButton, settingsButtonParams);

        settingsPanel = new LinearLayout(this);
        settingsPanel.setOrientation(LinearLayout.VERTICAL);
        settingsPanel.setVisibility(View.GONE);
        settingsPanel.setPadding(0, dp(8), 0, 0);
        root.addView(settingsPanel);

        TextView configHint = label("Esses dados ja podem vir embutidos no APK. Altere aqui apenas para teste.", 12, muted);
        configHint.setPadding(0, 0, 0, dp(8));
        settingsPanel.addView(configHint);
        settingsPanel.addView(fieldLabel("Backend", muted));
        settingsPanel.addView(backendUrlInput);
        settingsPanel.addView(fieldLabel("Token", muted));
        settingsPanel.addView(tokenInput);

        setContentView(scroll);

        speakButton.setOnClickListener(v -> startSpeech());
        sendButton.setOnClickListener(v -> sendChat(userTextInput.getText().toString()));
        settingsButton.setOnClickListener(v -> {
            boolean show = settingsPanel.getVisibility() != View.VISIBLE;
            settingsPanel.setVisibility(show ? View.VISIBLE : View.GONE);
            settingsButton.setText(show ? "Ocultar configurações" : "Configurações");
        });
    }

    private EditText input(String hint, boolean password) {
        EditText editText = new EditText(this);
        editText.setHint(hint);
        editText.setSingleLine(true);
        editText.setTextColor(Color.WHITE);
        editText.setHintTextColor(Color.rgb(120, 140, 150));
        editText.setInputType(password ? InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD : InputType.TYPE_CLASS_TEXT);
        editText.setPadding(dp(12), 0, dp(12), 0);
        return editText;
    }

    private EditText multiInput(String hint) {
        EditText editText = input(hint, false);
        editText.setSingleLine(false);
        editText.setMinLines(3);
        editText.setGravity(Gravity.TOP);
        return editText;
    }

    private TextView fieldLabel(String value, int color) {
        TextView view = label(value, 12, color);
        view.setPadding(0, dp(12), 0, dp(4));
        return view;
    }

    private TextView label(String value, int size, int color) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(color);
        return view;
    }

    private Button button(String value, int color) {
        Button button = new Button(this);
        button.setText(value);
        button.setTextColor(Color.rgb(10, 18, 24));
        button.setBackgroundColor(color);
        return button;
    }

    private void loadSettings() {
        SharedPreferences prefs = getSharedPreferences("mainha", MODE_PRIVATE);
        backendUrlInput.setText(prefs.getString("backend_url", BuildConfig.MAINHA_BACKEND_URL));
        tokenInput.setText(prefs.getString("assistant_token", BuildConfig.MAINHA_ASSISTANT_TOKEN));
        String backend = normalizeBackendUrl();
        if (backend.contains("10.0.2.2")) {
            status("Pronto. Configure o backend se for testar em celular físico.");
        } else {
            status("Pronto para falar.");
        }
    }

    private void saveSettings() {
        getSharedPreferences("mainha", MODE_PRIVATE)
                .edit()
                .putString("backend_url", normalizeBackendUrl())
                .putString("assistant_token", tokenInput.getText().toString().trim())
                .apply();
    }

    private void startSpeech() {
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, REQUEST_RECORD_AUDIO);
            return;
        }

        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR");
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Fale com a Mainha");
        status("Ouvindo...");
        startActivityForResult(intent, REQUEST_SPEECH);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_SPEECH && resultCode == RESULT_OK && data != null) {
            ArrayList<String> results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (results != null && !results.isEmpty()) {
                String recognized = results.get(0);
                userTextInput.setText(recognized);
                sendChat(recognized);
            }
        } else if (requestCode == REQUEST_SPEECH) {
            status("Nada reconhecido.");
        }
    }

    private void sendChat(String text) {
        String trimmed = text == null ? "" : text.trim();
        if (trimmed.isEmpty()) {
            status("Digite ou fale uma pergunta.");
            return;
        }

        saveSettings();
        setBusy(true);
        status("Pensando e gerando voz...");

        new Thread(() -> {
            HttpURLConnection connection = null;
            try {
                URL url = new URL(normalizeBackendUrl() + "/assistant/chat");
                connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                connection.setConnectTimeout(15000);
                connection.setReadTimeout(180000);
                connection.setDoOutput(true);
                connection.setRequestProperty("Content-Type", "application/json; charset=utf-8");
                String token = tokenInput.getText().toString().trim();
                if (!token.isEmpty()) {
                    connection.setRequestProperty("Authorization", "Bearer " + token);
                }

                JSONObject payload = new JSONObject();
                payload.put("text", trimmed);
                payload.put("return_audio_base64", true);

                try (OutputStream os = connection.getOutputStream()) {
                    os.write(payload.toString().getBytes(StandardCharsets.UTF_8));
                }

                int code = connection.getResponseCode();
                String body = new String(
                        (code >= 200 && code < 300 ? connection.getInputStream() : connection.getErrorStream()).readAllBytes(),
                        StandardCharsets.UTF_8
                );
                if (code < 200 || code >= 300) {
                    throw new IllegalStateException("HTTP " + code + ": " + body);
                }

                JSONObject result = new JSONObject(body);
                runOnUiThread(() -> {
                    answerText.setText(result.optString("answer_text", ""));
                    playAudio(result);
                    status("Resposta pronta.");
                    setBusy(false);
                });
            } catch (Exception ex) {
                runOnUiThread(() -> {
                    status("Falha: " + ex.getMessage());
                    setBusy(false);
                });
            } finally {
                if (connection != null) connection.disconnect();
            }
        }).start();
    }

    private void playAudio(JSONObject result) {
        try {
            if (mediaPlayer != null) {
                mediaPlayer.release();
                mediaPlayer = null;
            }

            String audioBase64 = result.optString("audio_base64", "");
            if (!audioBase64.isEmpty()) {
                byte[] bytes = Base64.decode(audioBase64, Base64.DEFAULT);
                File file = new File(getCacheDir(), "mainha-answer.wav");
                try (FileOutputStream output = new FileOutputStream(file)) {
                    output.write(bytes);
                }
                mediaPlayer = MediaPlayer.create(this, Uri.fromFile(file));
                if (mediaPlayer != null) mediaPlayer.start();
                return;
            }

            String audioUrl = result.optString("audio_url", "");
            if (!audioUrl.isEmpty()) {
                mediaPlayer = new MediaPlayer();
                mediaPlayer.setDataSource(audioUrl);
                mediaPlayer.prepareAsync();
                mediaPlayer.setOnPreparedListener(MediaPlayer::start);
            }
        } catch (Exception ex) {
            status("Resposta recebida, mas o audio falhou: " + ex.getMessage());
        }
    }

    private String normalizeBackendUrl() {
        String raw = backendUrlInput.getText().toString().trim();
        if (raw.isEmpty()) raw = BuildConfig.MAINHA_BACKEND_URL;
        return raw.replaceAll("/+$", "");
    }

    private void setBusy(boolean busy) {
        sendButton.setEnabled(!busy);
        speakButton.setEnabled(!busy);
    }

    private void status(String value) {
        statusText.setText(value);
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
