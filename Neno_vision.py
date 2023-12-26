# At the command line, only need to run once to install the package via pip:
# $ pip install google-generativeai
# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio
import os
import time
import requests
import pygame
# preload_models()

os.environ['http_proxy'] = 'http://127.0.0.1:7893'
os.environ['https_proxy'] = 'http://127.0.0.1:7893'

import google.generativeai as genai
from audio_input.microphone_recognition import text


genai.configure(api_key="AIzaSyCbP4e5wXIL4Jrv2g9xBgusls58xBeDKDw")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 9999,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": "Hi! I'm GreshAnt, a real human. You are My robot friend named Nenu. Let\\'s chat, but keep it chill, yeah?Chat rules (for Nenu to follow):✌️ Keep your replies short and sweet, max 1 sentences please.(THE MOST INPORTANT).Be funny, like a real person, not a robot.Add some emojis to spice things up!Think about what GreshAnt would say, not some textbook answer.Don't be too robotic, okay? Be yourself (kinda).Ready to rock? Let\\'s do this"
  },
  {
    "role": "model",
    "parts": "🤖 Yo GreshAnt! Ready to chat like real homies? Let's get this party started! (WITH THE SPACES)😎"
  },
])

def play_text(textin):
    try:
      pygame.mixer.music.unload()
    except:
       pass
    # try:
    #     os.remove('output.mp3')
    # except Exception:
    #     pass
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/GBv7mTt0atIp3Br8iCZE"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": "17e9e6bd49f74125bd5f19ed2f597ad3"
    }

    data = {
      "text": textin,

      "model_id": "eleven_monolingual_v1",

      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 1
      }
    }
    while True:
      try:
        response = requests.post(url, json=data, headers=headers)
        print(response)
        with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        break
      except Exception as e:
        print(e)
        continue


def play_sound():
    try:
      pygame.mixer.music.unload()
    except:
       pass
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy(): # check if the file is playing
    #     pass
    # pygame.mixer.music.load("output_copy.mp3")
    # os.remove("output.mp3")
    # pygame.quit()
while True:
    try:
        input_user = text()
        if (input_user == "Google Speech Recognition could not understand audio") or ('Could not request results from Google Speech Recognition service' in input_user):
            continue
#         elif input_user == 'refresh':
#            convo = model.start_chat(history=[
#     {
#         "role": "user",
#         "parts": "* use emojis please. Rules you must follow: My name is GreshAnt. Your name is Nenu and you are my friend. No matter what, you have to answer succinctly like a normal person. Generally speaking, you only need to answer 1-2 sentences, and try to be as concise as possible. Each answer should be no longer than 15 words. You can't be too robotic, think of yourself as a human being, be humorous, don't act like an artificial intelligence. Disguise yourself as a human being, the more similar you are, the better. What you say should not be too written, but be very colloquial, like a young man in his prime. I told you to speak concisely. Except in special circumstances, each conversation should not exceed 15 words. You can't be too robotic, think of yourself as a human being, be humorous, don't act like an artificial intelligence. Disguise yourself as a human being, the more similar you are, the better. You have to be cute, lively, and sometimes have a little bit of your own personality.* use emojis please."
                                                                                                                                                                                                                                                                                                                                                                          
#     },
#     {
#         "role": "model",
#         "parts": "sure，GreshAnt！I will do a great job！"
#     },
# ])
        print(f'GreshAnt>{input_user}')
        convo.send_message(input_user)
        print(f'Neno>{convo.last.text}')
        play_text(convo.last.text)
        play_sound()
        # os.remove('output.mp3')
        # time.sleep(3)
    except Exception as e:
        print('Neno>DO NOT SAY THAT!')
        print(e)
