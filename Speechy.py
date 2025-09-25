#Used to record audio from you computers microphone
import sounddevice as sd
#This will help with handling the audio by recording it as an array of numbers
import numpy as np
#This is what we will use to turn the speech into text
import speech_recognition as sr
from pynput import keyboard
import os



#This function is our callback function in which the stream will call when active
#in order to store chunks of audio within an array
def callback(indata, frames_count, time, status):
    #this checks to see if a status (or error) has been found in the stream
    if status:
        print("Status: ",status)

    frames.append(indata.copy())

#STEP 1: to set up the recording system and give the scope for it

#Creates an instance of the Recognizer class in which will allow tou manage your
#speech to text transferring process
recognizer = sr.Recognizer()
# Record 5 seconds of audio (mono, 16 kHz)
#This is needed to let the system know that we want to capture 16,000 samples per second
samplerate = 16000
#This is the array where we will store the chunks of data we get from the users audio
frames = []
#We use channel=1 to tell python to record all our audio in mono meaning that we will get the audio in one stream of audio samples
#dytype tells you the bit count for how you want to store the integer, and standard is 16-bit
#sd.rec() is what is needed to start recording the audio and to store it in a numpy array called audio

#Our input stream will not go live until the "a" key is pressed, and will end once the
#"b" key is pressed

stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16',callback=callback)
def startStream(key):
    try:
        #Start stream if "a" key is pressed
        if key.char == 'a':  # letter "a"
            print("Recording in progress...")
            stream.start()  # macOS example
        elif key.char == 'b':
            #End stream if "b" key is pressed
            stream.stop()
            print("Recording Stopped....")
            #Used to group all the chunks of audio frames together
            audio = np.concatenate(frames, axis=0)
            #Will transform the combined frames of audio data into readable audio data
            #by turning it into bytes
            audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)
            try:
                #This sends your audio data to the Google web speech API to translate
                #your text
                text = recognizer.recognize_google(audio_data)
                print("You said:", text)
                # This will create a text file called speech and make it open to editing, and store it in the variable f
                with open("speech.txt", "w") as f:
                    f.write(text)
                    # The text will automatically close and save once the write command has finished and the with loop is down

            except Exception as e:
                print("Error:", e)
    except Exception as e:
        print("Error: ", e)
        #If a key that is pressed while the system is running is anything but
        #the char characters, we wil automatically end our program
        if key == keyboard.Key.esc:
            print("Exiting...")
            return False


#This will create a listener that will listen for keyboard inputs
with keyboard.Listener(on_press=startStream) as listener:
    listener.join()


