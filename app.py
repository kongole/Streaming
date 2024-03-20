from flask import Flask, request, jsonify
import speech_recognition as sr
import openai

app = Flask(__name__)

# Set up your OpenAI API key
# openai.api_key = ''

def analyze_sentiment(text):
    # Use OpenAI API to analyze sentiment
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Analyze the sentiment of the following text: '{text}'",
        max_tokens=50
    )
    sentiment_analysis = response.choices[0].text.strip()
    return sentiment_analysis

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided.'}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    with audio_data as source:
        audio = recognizer.record(source)
    
    try:
        transcription = recognizer.recognize_google(audio)
        return jsonify({'transcription': transcription}), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio.'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f"Error occurred; {e}"}), 500

@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Text data not provided.'}), 400

    text = data['text']
    sentiment_analysis = analyze_sentiment(text)
    return jsonify({'sentiment_analysis': sentiment_analysis}), 200

if __name__ == '__main__':
    app.run(debug=True)
