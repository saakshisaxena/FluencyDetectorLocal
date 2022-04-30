from speech import speech
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

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1


# add delay so that the user gets time to grasp the question and make mental notes for a short time
for i in range(5,0, -1):
    print(str(i)+"...")

# Record voice via OS record system
fs = 44100  # Sample rate
seconds = 30  # Duration of recording # in seconds

print("Voice recording started!! \nPlease Start Speaking") # To print on console

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # Try changing channel numbers if channels are busy or unavailable for audio recording.
# for i in range(1, 120):
#     print(str(i)+"...")
sd.wait()  # Wait until recording is finished
print("End of recording...")
write('test6.wav', fs, myrecording)  # Save as WAV file


# IBM WATSON Project key and url to be able to access the Speech to Text converting API
apikey = 'UgYS0_WKlpN_2UASRG4x6FqoB90ZEmxELm1aRdzJ9r-N'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/4bce5a9f-a50b-40ff-b781-f3b36a3a103a'

# Setup Service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Perform conversion
with open('test6.wav', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/wav', model='en-GB_Telephony', inactivity_timeout=60, speech_detector_sensitivity=1.0, background_audio_suppression=0.5, timestamps=True, smart_formatting=True).get_result()

transcript = ". ".join([res['results'][i]['alternatives'][0]['transcript'].strip() \
                        for i in range(0,len(res['results']))])

# write the speech converted text in a text file
with open('test6.txt', 'w') as out:
     out.writelines(transcript)
