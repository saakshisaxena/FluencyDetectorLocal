from gtts import gTTS
from playsound import playsound
import os
from numpy import random

questions=["What is your name?", "Tell me something about your favourite movie.",
"How is the weather today", "What is your favourite fruit?"]

def play(text):
    # make request to google to get synthesis
    # text can also be
    # text = input("Enter your choice of text: ")
    # text = "Hello! I am Saakshi's project. Test 1 2 3. Hello World!!"
    tts = gTTS(text, lang = 'en')
    # save the audio file
    tts.save("hi.mp3")
    # play the audio file
    # playsound("hi.mp3")
    # OS doesn't work ???
    os.system("hi.mp3")
    # os.remove(music_file)

def randomQuesGenerator():
    x = random.randint(len(questions))
    print(questions[x])
    play(str(questions[x]))

randomQuesGenerator()



# play from a temporary file!!


# myText = "Hehe hello welcome Namaste Heheheehe!!"
# language = "en"
# output = gTTS(text=myText, lang=language, slow=False)
# output.save("output.mp3")
# os.system("start output.mp3")



# # Import the required module for text
# # to speech conversion
# from gtts import gTTS
#
# # This module is imported so that we can
# # play the converted audio
# import os
#
# # The text that you want to convert to audio
# mytext = 'Welcome to geeksforgeeks!'
#
# # Language in which you want to convert
# language = 'en'
#
# # Passing the text and language to the engine,
# # here we have marked slow=False. Which tells
# # the module that the converted audio should
# # have a high speed
# myobj = gTTS(text=mytext, lang=language, slow=False)
#
# # Saving the converted audio in a mp3 file named
# # welcome
# myobj.save("welcome.mp3")
#
# # Playing the converted file
# os.system("mpg321 welcome.mp3")
