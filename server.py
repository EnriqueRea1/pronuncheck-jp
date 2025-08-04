from flask import Flask, request, jsonify
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
import pykakasi
from openai import OpenAI
import os, datetime

app = Flask(__name__)

# ---- Config ----
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---- Inicializar componentes ----
model = SentenceTransformer("sonoisa/sentence-bert-base-ja-mean-tokens")
kks = pykakasi.kakasi()

# API key desde variable de entorno
client = OpenAI(api_key=("API_KEY"))

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        # -------- Validaciones básicas --------
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el archivo de audio (campo "file").'}), 400

        frase_ideal = request.form.get('jp', '').strip()
        romaji_ref = request.form.get('romaji', '').strip()

        if not frase_ideal:
            return jsonify({'error': 'Falta el texto esperado (expected_jp).'}), 400

        # -------- Guardar archivo --------
        file = request.files['file']
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # -------- Reconocimiento de voz --------
        r = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio = r.record(source)

        try:
            frase_usuario = r.recognize_google(audio, language="ja-JP")
        except sr.UnknownValueError:
            return jsonify({"error": "No se entendió el audio."}), 400

        # -------- Romanización detectada --------
        result = kks.convert(frase_usuario)
        romaji_user = " ".join([item["hepburn"] for item in result])

        # -------- Similitud --------
        emb1 = model.encode(frase_ideal, convert_to_tensor=True)
        emb2 = model.encode(frase_usuario, convert_to_tensor=True)
        sim = util.cos_sim(emb1, emb2).item()

        # -------- Prompt GPT --------
        prompt = f"""
Estás ayudando a un estudiante que practica japonés oral. Evalúa su pronunciación.

Línea objetivo: 「{frase_ideal}」
El estudiante dijo: 「{frase_usuario}」
Romanji detectado: "{romaji_user}"
Romanji de referencia: "{romaji_ref}"

Reglas:
- Si está bien, elogia y motiva (breve).
- Si hubo diferencias, menciona la parte (usa romanji) y sugiere cómo sonar más natural.
- Nada de traducciones literales.
- Tono cálido, <=30 palabras.
- Que el feedback sea en inglés
"""

        feedback = ""
        if client.api_key:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            feedback = resp.choices[0].message.content.strip()
        else:
            feedback = "(Sin feedback: falta OPENAI_API_KEY.)"

        return jsonify({
            "frase_ideal": frase_ideal,
            "frase_usuario": frase_usuario,
            "romaji_usuario": romaji_user,
            "romaji_ref": romaji_ref,
            "similitud": sim,
            "feedback": feedback
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)