import tkinter as tk
import speech_recognition as sr
from gtts import gTTS
import openai
import pydub
from pydub.playback import play

openai.api_key = 'insert key here'
model_id = 'gpt-3.5-turbo' #or 4 

# Create a recognizer object
r = sr.Recognizer()

def get_response(prompt):
    prompt = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=prompt,
        temperature=0.7,
    )
    return response.choices[0].message.content

def capture_speech():
    global text_label
    button.config(state=tk.DISABLED, relief=tk.SUNKEN, text="Listening...")

    with sr.Microphone() as source:
        print("Speak something...")
        r.pause_threshold = 0.75
        r.phrase_time_limit = 5
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")

        response = get_response(text)

        tts = gTTS(text=response, lang='en')
        tts.save("output.mp3")

        audio = pydub.AudioSegment.from_file("output.mp3")
        speed_up_audio = audio.speedup(playback_speed=1.5)

        # Play the speech
        play(speed_up_audio)

        # Update the text label in the GUI
        text_label.config(text=response)

    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except sr.RequestError as e:
        print(f"Error: {e}")

    button.config(state=tk.NORMAL, relief=tk.RAISED, text="Capture Speech")

window = tk.Tk()
window.title("Jarvis")
window.geometry("400x200")

# Create a label for displaying the response text
text_label = tk.Label(window, text="", wraplength=350)
text_label.pack(pady=20)

# Create a button to capture speech
button = tk.Button(window, text="Capture Speech", command=capture_speech)
button.pack()

# Start the GUI event loop
window.mainloop()
