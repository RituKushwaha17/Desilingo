from flask import Flask, render_template, request, redirect, url_for,jsonify
from googletrans import Translator
from gtts import gTTS
import os
import base64
import io
from PIL import Image
import uuid

app = Flask(__name__)

translator = Translator()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        return redirect("/select-language")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        return redirect("/login")
    return render_template("signup.html")

@app.route("/select-language", methods=["GET", "POST"])
def select_language():
    return render_template("select_language.html")

@app.route("/select-mode", methods=["POST"])
def select_mode():
    selected_language = request.form["language"]
    return render_template("select_mode.html", language=selected_language)

@app.route("/start-learning", methods=["POST"])
def start_learning():
    language = request.form["language"]
    mode = request.form["mode"]

    if mode == "voice":
        return render_template("voice_learning.html", language=language)
    elif mode == "gesture":
        return render_template("gesture_learning.html", language=language)
    else:
        return "Invalid mode selected", 400

@app.route("/voice-learning", methods=["POST"])
def voice_learning():
    language = request.form["language"]
    return render_template("voice_learning.html", language=language)

@app.route("/gesture-learning", methods=["POST"])
def gesture_learning():
    language = request.form["language"]
    return render_template("gesture_learning.html", language=language)



@app.route("/translate", methods=["POST"])
def translate_word():
    data = request.json
    hindi_word = data.get("hindi_word")
    target_lang = data.get("target_lang")

    lang_map = {
        "tamil": "ta",
        "bengali": "bn",
        "marathi": "mr",
        "telugu": "te",
        "gujarati": "gu",
        
    }

    target_code = lang_map.get(target_lang.lower(), "hi")
    translated = translator.translate(hindi_word, src="hi", dest=target_code).text


    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")

    tts = gTTS(translated, lang=target_code)
    audio_file = f"static/audio/translated.mp3"
    tts.save(audio_file)

    return jsonify({"translated": translated, "audio_url": "/" + audio_file})

@app.route("/predict-gesture", methods=["POST"])
def predict_gesture():
    data = request.get_json()
    image_data = data.get("image")
    target_lang = data.get("target_lang")

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

  
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))

    
    predicted_hindi_word = "नमस्ते" 
    
    translated = translate_word(predicted_hindi_word, target_lang)

    
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join("static", "audio", audio_filename)
    tts = gTTS(translated, lang=target_lang_code(target_lang))
    tts.save(audio_path)

    return jsonify({
        "hindi_word": predicted_hindi_word,
        "translated": translated,
        "audio_url": f"/static/audio/{audio_filename}"
    })


def target_lang_code(language):
    lang_map = {
        "english": "en",
        "tamil": "ta",
        "telugu": "te",
        "bengali": "bn",
        "kannada": "kn",
        "marathi": "mr",
        "gujarati": "gu",
        "punjabi": "pa",
        "odia": "or"
    }
    return lang_map.get(language.lower(), "en")


def translate_word(hindi_word, target_lang):
    translations = {
        "नमस्ते": {
            "english": "Hello",
            "tamil": "வணக்கம்",
            "telugu": "నమస్తే",
            "bengali": "নমস্তে",
            "kannada": "ನಮಸ್ಕಾರ",
            "marathi": "नमस्कार",
            "gujarati": "નમસ્તે",
            "punjabi": "ਨਮਸਤੇ",
            "odia": "ନମସ୍କାର"
        }
    }
    return translations.get(hindi_word, {}).get(target_lang.lower(), hindi_word)




if __name__ == "__main__":
    app.run(debug=True)
