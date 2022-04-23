from pydub import AudioSegment
import pydub
import sounddevice as sd
from pydub.playback import play
from scipy.io.wavfile import write
from pathlib import Path
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech import speech

speech = speech()

## !pip install ibm_watson

################################################
###### to run the random Question text to speech:
from textToSpeechEx import textToSpeechEx

randomQuesGenerator = textToSpeechEx()
randomQuesGenerator.randomQuesGenerator()
#############################################
#############################################

# add delay so that we can wait for the audio to finish and then start recordign the response of the User
import time
time.sleep(2)
speech.speak("Get ready to speak in")
for i in range(5,0, -1):
    print(str(i)+"...")
    speech.speak(i)
    time.sleep(1)


# Record voice via OS record system
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

print("Voice recording started!! \nPlease Start Speaking")
speech.speak("Voice recording started. \n Please Start Speaking After this message ends.")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # Had errors with channel numbers ...try with channel = 1
sd.wait()  # Wait until recording is finished
print("End of recording...")
speech.speak("Voice recording stopped. Well done!")
write('output.wav', fs, myrecording)  # Save as WAV file

# From the .mp3 file convert it to text file
apikey = 'UgYS0_WKlpN_2UASRG4x6FqoB90ZEmxELm1aRdzJ9r-N'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/4bce5a9f-a50b-40ff-b781-f3b36a3a103a'

# Setup Service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Perform conversion
with open('output.wav', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/wav', model='en-GB_Telephony', inactivity_timeout=60, speech_detector_sensitivity=1.0, background_audio_suppression=0.5, timestamps=True, smart_formatting=True).get_result()

# print(res)
''' Result of stt.recognize(audio=f, content_type='audio/wav', model='en-GB_Telephony', inactivity_timeout=60, speech_detector_sensitivity=1.0, background_audio_suppression=0.5, timestamps=True).get_result()
{'result_index': 0,
'results':
    [{'final': True, 'alternatives': [{'transcript': 'uh ', 'confidence': 0.63, 'timestamps': [['uh', 1.14, 1.48]]}]},
     {'final': True, 'alternatives': [{'transcript': 'okay ', 'confidence': 0.58, 'timestamps': [['okay', 6.12, 6.12]]}]},
     {'final': True, 'alternatives': [{'transcript': 'who says you are not perfect ', 'confidence': 0.73, 'timestamps': [['who', 6.38, 6.58], ['says', 6.7, 7.1], ['you', 7.18, 7.24], ['are', 7.28, 7.4], ['not', 7.52, 7.72], ['perfect', 7.92, 9.12]]}]},
     {'final': True, 'alternatives': [{'transcript': 'who is ', 'confidence': 0.68, 'timestamps': [['who', 9.74, 9.86], ['is', 9.9, 9.94]]}]}
     ]
}
'''
# wordsWithTimeStamp = ""
# for i in range(0,len(res['results'])):
#     for j in range(0, len(res['results'][i]['alternatives'][0]['timestamps'])):
#         print(res['results'][i]['alternatives'][0]['timestamps'][j])
#         print(res['results'][i]['alternatives'][0]['timestamps'][j][1])
    # for j in range(0, len(res(['results'][i]['alternatives'][2]['timestamps']))):
    #     wordsWithTimeStamp += res['results'][i]['alternatives'][2]['timestamps'][j] +"\n"

totalTimeTaken = float(res['results'][len(res['results'])-1]['alternatives'][0]['timestamps'][len(res['results'][len(res['results'])-1]['alternatives'][0]['timestamps'])-1][2]) - float(res['results'][0]['alternatives'][0]['timestamps'][0][1])
totalTimeTaken = totalTimeTaken/60 # convert it to minutes
totalTime = float(int(totalTimeTaken*100)/100.0) # convert it to only 2 decimal places
print("total time taken for speech "+str(totalTime))
speech.speak("Total time taken for your speech is "+str(totalTime)+" minutes")
### Save feedback in a text file ######
with open('feedback.txt', 'w') as out:
    out.writelines("total time taken for speech"+str(totalTimeTaken))
# print(wordsWithTimeStamp)
print(len(res['results']), "segments")
transcript = ". ".join([res['results'][i]['alternatives'][0]['transcript'].strip() \
                        for i in range(0,len(res['results']))])

with open('output.txt', 'w') as out:
     out.writelines(transcript)

################################################
#ASK THE USER IF THEY WANT TO MAKE ANY CHANGES TO THE SPEECH TO TEXT OUTPUT FILE BEFORE RUNNING THE CLIENT
#########################################################
# changeText = input("Would you like to see and make changes to the speech to text output? [Y/n]").lower()
print("Would you like to see and make changes to the speech to text output? [Y/n]")
changeText = speech.listen("Would you like to see and make changes to the speech to text output? Say 'yes' or 'no'[Y/n]").lower()
correctAnswer = False
while(not correctAnswer):
    if changeText=="no":
        print("Analysing your speech~")
        speech.speak("Analysing your speech~")
        correctAnswer=True
    elif changeText=="yes":
        #### do smth#####Open the text file in notepad
        ###### Open the file and wait for the user to finish editing the file.
        print("Please save and close the notepad file after you are done cheking / making changes, to get the feedback.")
        speech.speak("Opening the file in notepad. Please save and close the notepad file after you are done cheking / making changes to progress.")
        import subprocess
        p = subprocess.Popen(('notepad',"output.txt"))
        p.wait()
        print("Analysing your speech~")
        speech.speak("Analysing your speech~")
        correctAnswer=True
    else:
        changeText = speech.listen("Say 'yes' or 'no'[Y/n]").lower()
        print("Say 'yes' or 'no'[Y/n]")
################################################
###### Run the client side code now for socket to talk to py2 server
# import importlib
# importlib.import_module('client')
from Client import Client

client = Client()
client.connect()
client.sendData()
client.getData()
client.closeAndPrint()
#############################################
#############################################

###Plot a graph of disfluency SCORE
print("Would you like to see your progress/ score tracker [y/n]")
showScoreTracker = speech.listen("Would you like to see your progress/ score tracker. Say 'yes' or 'no' [y/n]").lower()
correctAnswer=False
while(not correctAnswer):
    if showScoreTracker=="yes":
        speech.speak("Please see your progress in the graph pop up")
        import matplotlib.pyplot as plt
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
        print("'Y' or 'n' for yes/no")
        showScoreTracker = input("[Y/n]").lower()

#######Ask if they want to listen to their speech
print("Would you like to listen to your speech again [y/n] \n The audio will only be available for this current session: ")
listenToSpeech = speech.listen("Would you like to listen to your speech that was recorded \n The audio will only be available for this current session. Say yes or no. ").lower()
correctAnswer=False
while(not correctAnswer):
    if listenToSpeech=="yes":
        speech.speak("playing sound audio")
        from playsound import playsound

        # for playing note.wav file
        playsound('output.wav')

        print("bye~")
        speech.speak("Goodbye")
        correctAnswer=True

    elif listenToSpeech=="no":
        print("Bye")
        speech.speak("Goodbye")
        correctAnswer=True

    else:
        print("yes or no")
        listenToSpeech = speech.listen("Say yes ir no. ").lower()
