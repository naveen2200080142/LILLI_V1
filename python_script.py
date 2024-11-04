import speech_recognition as sr
import win32com.client
import time
import os
import google.generativeai as genai

# Configure Google Gemini API with your key
api_key = os.environ.get("API_KEY")
if not api_key:
    raise EnvironmentError("API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# Upload function for Gemini (not used yet)
def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Configure generation settings for Gemini
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize the speaker
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Reduce noise
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()  # Convert to lowercase for consistency
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speaker.Speak("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speaker.Speak("Sorry, I could not connect to the speech recognition service.")
        return None

# Main interaction loop
def main():
    print("Speech recognition and text-to-speech system starting up...")

    while True:
        print("Say something or say 'exit' to stop:")
        recognized_text = recognize_speech()
        
        if recognized_text:
            if "exit" in recognized_text:
                print("Exiting...")
                speaker.Speak("Exiting...")
                break

            try:
                response = model.generate_content(recognized_text)
                print(response)
                speaker.Speak(response.text)
            except Exception as e:
                print(f"Error in model generation: {e}")
                speaker.Speak("Sorry, there was an issue generating the response.")
        else:
            speaker.Speak("I didn't catch that, could you please repeat?")

        time.sleep(1)  # Delay between listening sessions

if __name__ == "__main__":
    main()
