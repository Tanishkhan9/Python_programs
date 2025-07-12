import pyttsx3

def select_voice_by_gender(engine, gender_preference):
    voices = engine.getProperty('voices')
    gender_preference = gender_preference.lower()
    engine.setProperty('rate', 150)   # Speed of speech (default ~200)
    engine.setProperty('volume', 1) # Volume level (0.0 to 1.0)

    for voice in voices:
        if gender_preference == "female" and ("female" in voice.name.lower() or "zira" in voice.name.lower()):
            engine.setProperty('voice', voice.id)
            return True
        elif gender_preference == "male" and ("male" in voice.name.lower() or "david" in voice.name.lower() or "alex" in voice.name.lower()):
            engine.setProperty('voice', voice.id)
            return True
    return False

def text_to_speech():
    engine = pyttsx3.init()

    # Ask user for gender preference
    gender = input("Select voice gender (Male/Female): ").strip()
    if not select_voice_by_gender(engine, gender):
        print("Requested gender voice not found. Using default voice.")

    # Prompt for text
    user_input = input("\nEnter the text to convert to speech:\n")
    engine.say(user_input)
    engine.runAndWait()

if __name__ == "__main__":
    text_to_speech()

text_to_speech()
