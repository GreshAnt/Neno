"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import os,pygame,requests,time
from pathlib import Path
import google.generativeai as genai
from audio_input.microphone_recognition import text
from PIL import ImageGrab
import threading
import PIL.Image
from settings import *
os.environ['http_proxy'] = 'http://127.0.0.1:7893'
os.environ['https_proxy'] = 'http://127.0.0.1:7893'
genai.configure(api_key=GOOGLE_API)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
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

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Validate that an image is present
# if not (img := Path("apex.png")).exists():
#   raise FileNotFoundError(f"Could not find image: {img}")

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": PR
  },
  {
    "role": "model",
    "parts": "🤖 Yo GreshAnt! Ready to chat like real homies? Let's get this party started! 😎"
  },
])

def capture_screen(x, y, width, height):
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save('screenshot.png')


def get_screenshot():
    screen_width, screen_height = ImageGrab.grab().size
    capture_screen(0, 0, screen_width, screen_height)
    image = PIL.Image.open("screenshot.png")

    # 将图像的大小调整为 1280x720
    image = image.resize((1280, 720))

    # 保存图像，覆盖原图
    image.save("screenshot.png")





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
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{TTS_VOICE}"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": TTS_API
    }

    data = {
      "text": textin,

      "model_id": "eleven_monolingual_v1",

      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
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


def play_sound(music_name):
    try:
      pygame.mixer.music.unload()
    except:
       pass
    pygame.mixer.init()
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy(): # check if the file is playing
    #     pass
    # pygame.mixer.music.load("output_copy.mp3")
    # os.remove("output.mp3")
    # pygame.quit()

        
while True:
    try:
        try:
          while pygame.mixer.music.get_busy(): # check if the file is playing
              pass
        except Exception:
           pass
        
        get_screenshot()
        threading.Thread(target=play_sound, args=('tip.mp3',)).start()


        input_user = text()
        
        image_parts = [
          {
            "mime_type": "image/png",
            "data": Path("screenshot.png").read_bytes()
          },
        ]

        prompt_parts = [
          image_parts[0],
          'Keep your replies short and sweet:' + input_user,
        ]


        if input_user == "Google Speech Recognition could not understand audio":
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
        res = model.generate_content(prompt_parts)
        print(f'Neno>{res.text}')
        play_text(res.text)
        # threading.Thread(target=play_sound, args=('output.mp3',)).start()
        play_sound('output.mp3')
        # os.remove('output.mp3')
        # time.sleep(3)
    except Exception as e:
        print('Neno>DO NOT SAY THAT!')
        print(e)
