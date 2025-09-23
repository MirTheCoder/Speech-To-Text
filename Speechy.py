#Used to record audio from you computers microphone
import sounddevice as sd
#This will help with handling the audio by recording it as an array of numbers
import numpy as np
#This is what we will use to turn the speech into text
import speech_recognition as sr
import keyboard


#Here are the arguments for our callback function
#1. indata refers to the array of audio data that we receive from the mic
#2. frames_count is used to count the number of frames in this chunk of array audio data
#3. time gives crucial time information regarding the audio recorded
#4. and status just is used to show warnings if any issues arise in your audio transcription process after you have recorded it
keyboard.wait("spacebar")
def callback(indata, frames_count, time, status):
 #If there is an issue with the audio recording then we will
 #just make a copy of the audio and append it to our frames array
 if status:
     print("Status: ",status)
     frames.append(indata.copy())

#STEP 1: to set up the recording system and give the scope for it

#This will handle the audio that we receive and convert it into text
recognizer = sr.Recognizer()
# Record 5 seconds of audio (mono, 16 kHz)
#This is needed to let the system know that we want to capture 16,000 samples per second
samplerate = 16000
#This is the array where we will store the chunks of data we get from the users audio
frames = []
print("Recording...")
#We use channel=1 to tell python to record all our audio in mono meaning that we will get the audio in one stream of audio samples
#dytype tells you the bit count for how you want to store the integer, and standard is 16-bit
#sd.rec() is what is needed to start recording the audio and to store it in a numpy array called audio

#Our input stream will not go live until the spacebar key is pressed

audio = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16',callback=callback)
#This will pause the program until the duration of recording has been finsihed
print("Done recording.")


#STEP 2: This will convert the audio into audio data
#This will be used to convert the audio we received into raw bytes
#We need to add the samplerate in there to let the system know how fast samples were recorded,
#and we have the number at the end to represent the number of bytes per sample
keyboard.wait("spacebar")
audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)


# This will be used to transcribe the audio data
try:
    text = recognizer.recognize_google(audio_data)
    print("You said:", text)
    #This will create a text file called speech and make it open to editing, and store it in the variable f
    with open("speech.txt", "w") as f:
        f.write(text)
        #The text will automatically close and save once the write command has finished and the with loop is down

except Exception as e:
    print("Error:", e)

