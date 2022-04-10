from gtts import gTTS
from playsound import playsound
import os
from numpy import random

# questions=["What is your name?", "Tell me something about your favourite movie.",
# "How is the weather today", "What is your favourite fruit?"]

summer = [
"What is your favorite summer memory?",
"What is your most memorable summer vacation?",
"What is your favorite way to cool off in the summertime?",
"What is your favorite family activity for summertime?",
"If you were invited to a cookout, what would you bring and why?",
"Which do you prefer, summer or winter?"
]

fall = [
"What is your favorite Fall festival?",
"Have you ever made apple cider or any other special drink from scratch?",
"If you could, would you like go experience Oktoberfest in Munich?",
"What is the scariest movie you’ve ever seen?",
"What is your favorite way to spend a lazy day?",
"If you could have it be warm year round, would you?",
]

winter = [
"What is your favorite winter sport?",
"If you had the chance to go to the north pole would you take it?",
"Would you ever go ice-fishing?",
"Did you ever have the chance to make a snowman? If so, what was your best one? If not, what would you start with?",
"What do you think about Santa Claus?",
"What is your favorite food to eat on a snowy date?"
]

spring = [
"What food would be at your ideal picnic?",
"Jogging, cycling, or swimming?",
"Have you ever been horseback riding?",
"You’re on your way to an important meeting and you get caught in the rain without an umbrella, what do you do?",
"If you could build a garden with only 3 plants, which ones would you grow?",
"Do you believe in spring cleaning?"
]

fun = [
"How do you feel about putting mayonnaise on french fries?",
"What’s the strangest thing a friend has ever done at your house?",
"Should you eat pizza with your hands or with a fork and knife?",
"What is now considered classy, but used to be very trashy?",
"If animals could talk, which would be the most charming?",
"What is something that is popular now, but in 10 years we might be ashamed of?",
# "If you time traveled naked 200 years in the past, how would you prove that you were from the future?",
# "What are a few fun ways to answer the boring question of “what do you do for work?”",
# "What was your favorite thing to do as a child that you would love to still be able to do as an adult?",
# "What is a dance move that everyone looks stupid doing?",
# "What is the most surprising thing you have seen in someone else’s home?",
# "What’s worst smell you have ever experienced?"
]

interesting = [
"Who inspires you?",
"If you could switch lives with anyone currently living for an entire day who would it be?",
"Whitewater rafting, hiking, or skiing?",
"How did you meet your best friend?",
"What motivates you?",
"What is something you’ve always wanted to try but have been too afraid to?",
# "What is your hidden talent?",
# "What is something you’ve tried but would never do again?",
# "If you only had 1 week left on Earth, what would you do?",
# "If you could go back in time and tell your younger self one thing, what would it be?"
]

themes=[summer, fall, winter, spring, fun, interesting]

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
    correctAnswer=False
    question = ""
    themeSelected=int(input("Please select a theme: \n1.summer \n2.fall \n3.winter \n4.spring \n5.fun \n6.interesting \nEnter a number corresponding to the theme. [1 to 6]:"))
    while(not correctAnswer):
        x = random.randint(len(summer))
        if themeSelected==1:
            question = summer[x]
            correctAnswer=True
        elif themeSelected==2:
            question = fall[x]
            correctAnswer=True
        elif themeSelected==3:
            question = winter[x]
            correctAnswer=True
        elif themeSelected==4:
            question = spring[x]
            correctAnswer=True
        elif themeSelected==5:
            question = fun[x]
            correctAnswer=True
        elif themeSelected==2:
            question = interesting[x]
            correctAnswer=True
        else:
            themeSelected=int(input("Select a number between 1 to 6:"))

    print(question)
    play(str(question))

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
