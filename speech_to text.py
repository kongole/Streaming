import os
import io
import json
from google.cloud import speech_v1p1beta1 as speech
from textblob import TextBlob

def transcribe_streaming(audio_file):
    client = speech.SpeechClient()

    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    # In streaming transcription, input audio streams continuously
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    # Stream audio input in real-time and get transcription
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in iter(lambda: audio_file.read(1024), b"")
    )

    responses = client.streaming_recognize(
        streaming_config, requests=requests
    )

    # Process transcription and extract insights
    for response in responses:
        for result in response.results:
            if result.is_final:
                transcription = result.alternatives[0].transcript
                print("Transcription:", transcription)

                # Analyze sentiment using TextBlob
                blob = TextBlob(transcription)
                sentiment_score = blob.sentiment.polarity
                print("Sentiment Score:", sentiment_score)

                # You can perform other NLP tasks here such as named entity recognition, topic modeling, etc.
                
                # Structure the data
                data = {
                    "transcription": transcription,
                    "sentiment_score": sentiment_score
                    # Add more fields as needed
                }
                print("Structured Data:", json.dumps(data, indent=4))

# Example usage
audio_file_path = "path/to/your/audio/file.wav"
transcribe_streaming(audio_file_path)
