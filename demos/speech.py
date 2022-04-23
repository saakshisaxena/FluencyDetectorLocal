from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

class speech:

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

        self.speaker = tts.init()
        self.speaker.setProperty('rate', 150)

    def speak(self, message):
        self.speaker.say(message)
        self.speaker.runAndWait()

    def listen(self, message):
        global recognizer

        self.speaker.say(message)
        self.speaker.runAndWait()

        done = False

        while not done:
            try:

                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    item = self.recognizer.recognize_google(audio)
                    item = item.lower()

                    done=True

                    self.speaker.say(f"Option {item} was selected!")
                    self.speaker.runAndWait()

            except speech_recognition.UnknownValueError:
                self.recognizer = speech_recognition.Recognizer()
                self.speaker.say("I did not understand you! Please try again!")
                self.speaker.runAndWait()

        return item
