---

# Japanese Pronunciation Feedback API

Este proyecto es un servicio web basado en **Flask** que permite evaluar la pronunciación de frases en japonés a partir de un archivo de audio.
La API utiliza **reconocimiento de voz**, **procesamiento de lenguaje natural** y **modelos de IA** para dar retroalimentación sobre la pronunciación del usuario.

---

## **Características principales**

* **Subida de audio** (formato WAV) y texto de referencia.
* **Reconocimiento de voz en japonés** usando [SpeechRecognition](https://pypi.org/project/SpeechRecognition/).
* **Conversión de texto japonés a romanización (romaji)** mediante [pykakasi](https://pypi.org/project/pykakasi/).
* **Medición de similitud semántica** con [Sentence-BERT](https://www.sbert.net/) (`sonoisa/sentence-bert-base-ja-mean-tokens`).
* **Retroalimentación personalizada** usando la API de OpenAI (modelo `gpt-4o-mini`).

---

## **Requisitos previos**

* Python 3.9+
* Claves de API:

  * **OpenAI API Key** (para la retroalimentación con GPT).

---

## **Instalación**

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tu-usuario/japanese-pronunciation-api.git
   cd japanese-pronunciation-api
   ```
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```
3. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Configura tu clave de OpenAI en variable de entorno:

   ```bash
   export OPENAI_API_KEY="tu_api_key"
   ```

   En Windows (PowerShell):

   ```powershell
   setx OPENAI_API_KEY "tu_api_key"
   ```

---

## **requirements.txt**

```txt
Flask==3.0.3
SpeechRecognition==3.10.1
sentence-transformers==2.2.2
pykakasi==0.96.1
openai==1.42.0
torch>=1.10.0
numpy>=1.21.0
```

---

## **Ejecución**

Inicia el servidor:

```bash
python app.py
```

Por defecto se ejecutará en `http://0.0.0.0:5005`.

---

## **Uso de la API**

### **Endpoint:** `/upload_audio`

**Método:** `POST`
**Parámetros:**

* **file** (form-data): archivo de audio en formato `.wav`
* **jp** (form-data): texto japonés esperado
* **romaji** (form-data, opcional): romanización de referencia

**Ejemplo con cURL:**

```bash
curl -X POST http://localhost:5005/upload_audio \
  -F "file=@ejemplo.wav" \
  -F "jp=迷子ですか？" \
  -F "romaji=maigo desu ka?"
```

**Respuesta JSON:**

```json
{
  "frase_ideal": "迷子ですか？",
  "frase_usuario": "迷子ですか",
  "romaji_usuario": "maigo desu ka",
  "romaji_ref": "maigo desu ka?",
  "similitud": 0.98,
  "feedback": "Great job! Your pronunciation is clear and natural."
}
```

---

## **Estructura del proyecto**

```
.
├── server.py                 # Código principal
├── uploads/               # Carpeta donde se guardan los audios
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación
```

---

## **Dependencias principales**

* Flask
* SpeechRecognition
* sentence-transformers
* pykakasi
* openai
* torch
* numpy

---

## **Posibles mejoras**

* Soporte para múltiples formatos de audio.
* Análisis fonético más detallado.
* Interfaz web de usuario.
* Guardado de historiales de práctica.

---

