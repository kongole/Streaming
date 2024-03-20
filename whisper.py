import speech_recognition as sr
import openai

# Set up your OpenAI API key


def analyze_sentiment(text):
    # Use OpenAI API to analyze sentiment
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Analyze the sentiment of the following text: '{text}'",
        temperature=0,
        max_tokens=50
    )
    sentiment_analysis = response.choices[0].text.strip()
    return sentiment_analysis

def transcribe_and_analyze():
    recognizer = sr.Recognizer()

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise for better transcription
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen to the audio and transcribe in real-time
            while True:
                audio = recognizer.listen(source)

                try:
                    # Transcribe the audio using Google Web Speech API
                    transcription = recognizer.recognize_google(audio)

                    # Analyze sentiment using OpenAI API
                    sentiment_analysis = analyze_sentiment(transcription)

                    # Print transcription and sentiment analysis
                    print("Transcription:", transcription)
                    print("Sentiment Analysis:", sentiment_analysis)

                    # You can perform other NLP tasks here

                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print("Error occurred; {0}".format(e))

        except KeyboardInterrupt:
            print("Stopped listening.")

# Call the function to start real-time transcription and analysis
transcribe_and_analyze()
