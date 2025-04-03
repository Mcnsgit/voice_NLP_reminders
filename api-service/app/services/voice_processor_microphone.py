import os
import speech_recognition as sr

def recognize_from_microphone():
    """
    Capture audio from microphone and convert to text.
    Returns the recognized text or None if recognition fails.
    """
    # Create a recognizer instance
    r = sr.Recognizer()
    
    # Capture audio from microphone
    with sr.Microphone() as source:
        print("Say something!")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Listen for audio
        audio = r.listen(source)
    
    # Try to recognize the speech
    try:
        text = r.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None

if __name__ == "__main__":
    recognize_from_microphone()