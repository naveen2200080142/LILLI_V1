import speech_recognition as sr
import win32com.client
import os
import google.generativeai as genai
import sys

# Configure Google Gemini API with your key
api_key = os.environ.get("API_KEY")
if not api_key:
    raise EnvironmentError("API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# Configure generation settings for Gemini
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 60,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize the speaker
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def recognize_speech():
    recognizer = sr.Recognizer()
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

def main():
    if '--mic' in sys.argv:
        recognized_text = recognize_speech()
        if recognized_text:
            try:
                response = model.generate_content(recognized_text)
                x= [i for i in response.text if i not in ['*','(',')','"','#']]
                
                r_text=''.join(x)
                print(r_text)
                speaker.Speak(r_text)
            except Exception as e:
                print(f"Error in model generation: {e}")
                speaker.Speak("Sorry, there was an issue generating the response.")
    elif len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        print(f"Received input: {user_input}")

        try:
            response = model.generate_content(user_input)
            x= [i for i in response.text if i not in ['*','(',')','"','#']]
            r_text=''.join(x)
            print(r_text)
            speaker.Speak(r_text)
        except Exception as e:
            print(f"Error in model generation: {e}")
            speaker.Speak("Sorry, there was an issue generating the response.")
    else:
        print("No input received.")

if __name__ == "__main__":
    main()











