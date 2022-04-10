from pydub import AudioSegment
import pydub
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
## !pip install ibm_watson

################################################
###### to run the random Question text to speech:
import importlib
importlib.import_module('textToSpeechEx')
#############################################
#############################################

# add delay so that we can wait for the audio to finish and then start recordign the response of the User
import time
time.sleep(2)
for i in range(5,0, -1):
    print(str(i)+"...")
    time.sleep(1)

# Record voice via OS record system
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

print("Voice recording started!! \nPlease Start Speaking")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # Had errors with channel numbers ...try with channel = 1
sd.wait()  # Wait until recording is finished
print("End of recording...")
write('output.wav', fs, myrecording)  # Save as WAV file

# convert default .wav to .mp3 file
output = Path("output.wav") # change the path
sound = AudioSegment.from_wav(output)
sound.export('myfile.mp3', format="mp3")

# From the .mp3 file convert it to text file
apikey = 'UgYS0_WKlpN_2UASRG4x6FqoB90ZEmxELm1aRdzJ9r-N'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/4bce5a9f-a50b-40ff-b781-f3b36a3a103a'

# Setup Service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Perform conversion
with open('myfile.mp3', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel').get_result()

print(len(res['results']), "segments")
transcript = ". ".join([res['results'][i]['alternatives'][0]['transcript'].strip() \
                        for i in range(0,len(res['results']))])

with open('output.txt', 'w') as out:
     out.writelines(transcript)

################################################
#ASK THE USER IF THEY WANT TO MAKE ANY CHANGES TO THE SPEECH TO TEXT OUTPUT FILE BEFORE RUNNING THE CLIENT
#########################################################
changeText = input("Would you like to see and make changes to the speech to text output? [Y/n]").lower()
correctAnswer = False
while(not correctAnswer):
    if changeText=="n":
        print("Analysing your speech~")
        correctAnswer=True
    elif changeText=="y":
        #### do smth#####Open the text file in notepad
        # import webbrowser
        # webbrowser.open("output.txt")
        ###### Open the file and wait for the user to finish editing the file.
        print("Please save and close the notepad file after you are done cheking / making changes, to get the feedback.")
        import subprocess
        p = subprocess.Popen(('notepad',"output.txt"))
        p.wait()
        print("Analysing your speech~")
        correctAnswer=True
    else:
        print("'Y' or 'n' for yes/no")
        changeText = input("[Y/n]").lower()
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
showScoreTracker = input("Would you like to see your progress/ score tracker [y/n]").lower()
correctAnswer=False
while(not correctAnswer):
    if showScoreTracker=="y":
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

    elif showScoreTracker=="n":
        print("Bye")
        correctAnswer=True

    else:
        print("'Y' or 'n' for yes/no")
        showScoreTracker = input("[Y/n]").lower()
