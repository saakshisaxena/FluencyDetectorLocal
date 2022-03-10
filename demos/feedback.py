# from demo2 import map
from gtts import gTTS
from playsound import playsound
import os

text = "This is feedback!!"
tts = gTTS(text, lang = 'en')
# save the audio file
tts.save("feedback.mp3")
os.system("feedback.mp3")

# importing the module
import json

# Opening JSON file
with open('map.txt') as json_file:
    data = json.load(json_file)

    # Print the type of data variable
    print("Type:", type(data))

    # Print the data of dictionary
    print(data)
