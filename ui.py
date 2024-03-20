import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import openai

# Set up your OpenAI API key
# openai.api_key = ''

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

                    # Display transcription and sentiment analysis on the GUI
                    transcription_text.configure(state='normal')
                    transcription_text.insert(tk.END, "Transcription: " + transcription + "\n")
                    transcription_text.insert(tk.END, "Sentiment Analysis: " + sentiment_analysis + "\n\n")
                    transcription_text.configure(state='disabled')

                except sr.UnknownValueError:
                    print("Could not understand audio.")

        except KeyboardInterrupt:
            print("Stopped listening.")

# Create the main GUI window
root = tk.Tk()
root.title("Real-time Transcription and Sentiment Analysis")

# Create a text widget to display transcriptions and sentiment analysis
transcription_text = scrolledtext.ScrolledText(root, width=50, height=20)
transcription_text.grid(row=0, column=0, padx=10, pady=10)

# Create a button to start transcription and analysis
start_button = tk.Button(root, text="Start Transcription", command=transcribe_and_analyze)
start_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
