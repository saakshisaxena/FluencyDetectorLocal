from gtts import gTTS
from numpy import random
import os
from playsound import playsound
from speech import speech

class TableTopicsMaster:
    def __init__(self):
        self.summer = [
        "What is your favorite summer memory?",
        "What is your most memorable summer vacation?",
        "What is your favorite way to cool off in the summertime?",
        "What is your favorite family activity for summertime?",
        "If you were invited to a cookout, what would you bring and why?",
        "Which do you prefer, summer or winter?"
        ]

        self.fall = [
        "What is your favorite Fall festival?",
        "Have you ever made apple cider or any other special drink from scratch?",
        "If you could, would you like go experience Oktoberfest in Munich?",
        "What is the scariest movie you’ve ever seen?",
        "What is your favorite way to spend a lazy day?",
        "If you could have it be warm year round, would you?",
        ]

        self.winter = [
        "What is your favorite winter sport?",
        "If you had the chance to go to the north pole would you take it?",
        "What’s worst smell you have ever experienced?",
        "Did you ever have the chance to make a snowman? If so, what was your best one? If not, what would you start with?",
        "What do you think about Santa Claus?",
        "What is your favorite food to eat on a snowy date?"
        ]

        self.spring = [
        "What food would be at your ideal picnic?",
        "Jogging, cycling, or swimming?",
        "Have you ever been horseback riding?",
        "You’re on your way to an important meeting and you get caught in the rain without an umbrella, what do you do?",
        "If you could build a garden with only 3 plants, which ones would you grow?",
        "Do you believe in spring cleaning?"
        ]

        self.fun = [
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
        # "What is the most surprising thing you have seen in someone else’s home?"
        ]

        self.interesting = [
        "What is your hidden talent?",
        "If you could switch lives with anyone currently living for an entire day who would it be?",
        "Whitewater rafting, hiking, or skiing?",
        "How did you meet your best friend?",
        "What is something you’ve tried but would never do again?",
        "What is something you’ve always wanted to try but have been too afraid to?",
        # "If you only had 1 week left on Earth, what would you do?",
        # "If you could go back in time and tell your younger self one thing, what would it be?"
        ]

        self.themes=[self.fun, self.interesting, self.summer, self.fall, self.winter, self.spring]
        self.speech = speech()

    def randomQuestionGenerator(self):
        correctAnswer=False
        question = ""
        print("Please select a theme: \n1.fun \n2.interesting \n3.summer \n4.fall \n5.winter \n6.spring \nEnter a number corresponding to the theme. [1 to 6]:")
        self.speech.speak("Please select a theme: 1 fun. 2 interesting. 3 summer. 4 fall. 5 winter. 6 spring.")
        while(not correctAnswer):
            try:
                themeSelected = int(self.speech.listen("Say a number corresponding to the theme. [1 to 6]:"))
                while(not correctAnswer):
                    x = random.randint(len(self.summer))
                    if themeSelected==1:
                        question = self.fun[x]
                        correctAnswer=True
                    elif themeSelected==2:
                        question = self.interesting[x]
                        correctAnswer=True
                    elif themeSelected==3:
                        question = self.summer[x]
                        correctAnswer=True
                    elif themeSelected==4:
                        question = self.fall[x]
                        correctAnswer=True
                    elif themeSelected==5:
                        question = self.winter[x]
                        correctAnswer=True
                    elif themeSelected==6:
                        question = self.spring[x]
                        correctAnswer=True
                    else:
                        themeSelected = int(self.speech.listen("Say a number corresponding to the theme. [1 to 6]:"))

                print(question)
                self.speech.speak("Your question is: "+question)
            except ValueError:
                # Handle the exception
                self.speech.speak('Please say a number')
