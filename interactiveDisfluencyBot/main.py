import matplotlib.pyplot as plt
import math
from pathlib import Path
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
from scipy.io.wavfile import write
import sounddevice as sd
import subprocess
import time

from Client import Client
from feedback import feedback
from TableTopicsMaster import TableTopicsMaster
from speech import speech

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1


# Initialize speech object to be able to use speak and listen facilities from speech class
speech = speech()

# To give user options of themes and speak out the final question the user needs to speak on:
tableTopicsMaster = TableTopicsMaster()
tableTopicsMaster.randomQuestionGenerator()

# add delay so that the user gets time to grasp the question and make mental notes for a short time
speech.speak("You need to speak for a minimum of 1 and a half minutes on the given question. Get ready to speak in")
for i in range(5,0, -1):
    print(str(i)+"...")
    speech.speak(i)
    time.sleep(1)

# Record voice via OS record system
fs = 44100  # Sample rate
seconds = 40  # Duration of recording # in seconds

print("Voice recording started!! \nPlease Start Speaking") # To print on console
speech.speak("Voice recording started.")

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # Try changing channel numbers if channels are busy or unavailable for audio recording.
# for i in range(1, 120):
#     print(str(i)+"...")
sd.wait()  # Wait until recording is finished
print("End of recording...")
speech.speak("Voice recording stopped. Well done!")
write('output.wav', fs, myrecording)  # Save as WAV file

# IBM WATSON Project key and url to be able to access the Speech to Text converting API
apikey = 'UgYS0_WKlpN_2UASRG4x6FqoB90ZEmxELm1aRdzJ9r-N'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/4bce5a9f-a50b-40ff-b781-f3b36a3a103a'

# Setup Service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Perform conversion
with open('output.wav', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/wav', model='en-GB_Telephony', inactivity_timeout=60, speech_detector_sensitivity=1.0, background_audio_suppression=0.5, timestamps=True, smart_formatting=True).get_result()

totalTimeTaken = float(res['results'][len(res['results'])-1]['alternatives'][0]['timestamps'][len(res['results'][len(res['results'])-1]['alternatives'][0]['timestamps'])-1][2]) - float(res['results'][0]['alternatives'][0]['timestamps'][0][1])
# totalTimeTaken = totalTimeTaken/60 # convert it to minutes
totalTime = float(int((totalTimeTaken/60)*100)/100.0) # convert it to only 2 decimal places
if totalTime<1.0:
    seconds = totalTimeTaken
    print("Total Time Taken for Speech "+str(int(seconds))+" seconds")
    speech.speak("Total Time Taken for Speech "+str(int(seconds))+" seconds")
    # Save timeTaken in feedback text file
    with open('feedback.txt', 'w') as out:
        out.writelines("Short Summary: \n Total Time Taken for Speech "+str(int(seconds))+" seconds \n")
else:
    minutes, seconds = divmod(int(totalTime * 60), 60)
    print("Total Time Taken for Speech "+str(int(minutes))+" minutes and "+str(int(seconds))+" seconds")
    speech.speak("Total Time Taken for Speech "+str(int(minutes))+" minutes and "+str(int(seconds))+" seconds")
    # Save timeTaken in feedback text file
    with open('feedback.txt', 'w') as out:
        out.writelines("Short Summary: \n Total time taken for speech "+str(int(minutes))+" minutes and "+str(int(seconds))+" seconds \n")


transcript = ". ".join([res['results'][i]['alternatives'][0]['transcript'].strip() \
                        for i in range(0,len(res['results']))])

# write the speech converted text in a text file
with open('output.txt', 'w') as out:
     out.writelines(transcript)
#
# ################################################
# #ASKING THE USER IF THEY WANT TO MAKE ANY CHANGES TO THE SPEECH TO TEXT OUTPUT FILE BEFORE RUNNING THE CLIENT
# #########################################################
# print("Would you like to see and make changes to the speech to text output?")
# changeText = speech.listen("Would you like to see and make changes to the speech to text output? Say 'yes' or 'no'").lower()
# correctAnswer = False
# while(not correctAnswer):
#     if changeText=="no":
#         print("Analysing your speech~")
#         speech.speak("Analysing your speech~")
#         correctAnswer=True
#     elif changeText=="yes":
#         ###### Open the file in notepad and wait for the user to finish editing the file.
#         print("Please save and close the notepad file after you are done cheking / making changes, to get the feedback.")
#         speech.speak("Opening the file in notepad. Please save and close the notepad file after you are done cheking / making changes to progress.")
#
#         p = subprocess.Popen(('notepad',"output.txt"))
#         p.wait()
#         print("Analysing your speech~")
#         speech.speak("Analysing your speech~")
#         correctAnswer=True
#     else:
#         changeText = speech.listen("Say 'yes' or 'no'").lower()
#         print("Say 'yes' or 'no'[Y/n]")
#
# ################################################
###### Run the client side code now for socket to talk to py2 server
client = Client()
client.connect()
client.sendData()
client.getData()
client.closeAndPrint()

#############################################
#############################################
###Read the Feedback
feedback = feedback()
feedback.getAndSaveFeedbackWithScore()

print("Do you want to read all feedback at once or go through it in steps? Say yes or no")
readAll = speech.listen("Do you want to read all feedback at once or go through it in steps? Say yes, to read feedback altogether, or no, to go through it in steps.").lower()
correctAnswer=False
while(not correctAnswer):
    if readAll=="yes":
        feedback.readAll() # Read the feedback text file that was stored
        correctAnswer=True
        speech.speak("You can see the full feedback report saved as a text file.")

    elif readAll=="no":
        print("Okay here is a short summary with types of repairs found:")
        speech.speak("Okay, here is a short summary with types of repairs found:")
        feedback.shortSummary(totalTime, totalTimeTaken)
        correctAnswer=True
        feedback.detailedReport()

    else:
        print("yes or no")
        readAll = speech.listen("Say yes or no").lower()

############################################
############################################
### Plot a graph of disfluency score
print("Would you like to see your progress/ score tracker")
showScoreTracker = speech.listen("Would you like to see your progress/ score tracker. Say 'yes' or 'no'").lower()
correctAnswer=False
while(not correctAnswer):
    if showScoreTracker=="yes":
        speech.speak("Please see your progress in the graph pop up")
        x = [] # attemp number
        y = []
        for line in open("disfluencyScoreTracker.txt", 'r'):
            y.append(int(line)) # score
        x = range(1, len(y)+1)

        plt.title("Disfluency Score Tracking")
        plt.xlabel('Attempt number')
        plt.ylabel('Score')
        plt.yticks(y)
        plt.plot(x, y, marker = 'o', c = 'g')

        plt.show()
        correctAnswer=True

    elif showScoreTracker=="no":
        correctAnswer=True

    else:
        print("yes/no")
        showScoreTracker = speech.listen("Say yes or no").lower()

################################################
#################################################
#######Ask if they want to listen to their speech
print("Would you like to listen to your speech again [yes/no] \n The audio will only be available for this current session: ")
listenToSpeech = speech.listen("Would you like to listen to your speech that was recorded \n The audio will only be available for this current session. Say yes or no. ").lower()
correctAnswer=False
while(not correctAnswer):
    if listenToSpeech=="yes":
        speech.speak("playing sound audio")

        # for playing note.wav file
        playsound('output.wav')

        print("bye~")
        speech.speak("Finished playing the recording.")
        correctAnswer=True

    elif listenToSpeech=="no":
        correctAnswer=True

    else:
        print("yes or no")
        listenToSpeech = speech.listen("Say yes or no").lower()

##############   END   ####################
speech.speak("Goodbye")
