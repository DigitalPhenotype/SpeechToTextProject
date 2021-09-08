import torchaudio
import os
import glob
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import speech_recognition as sr


def convert_dir_mp3_to_wav(audio_folder):
    types = (audio_folder + os.sep + '*.mp3',)  # the tuple of file types
    files_list = []

    for files in types:
        files_list.extend(glob.glob(files))

    for f in files_list:
        
        f_split = f[:-4]
        src = f
        dst = f_split + ".mp3.wav"

        print(src)

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        command = "It's ok"
        print(command)



def resample(directory_resample , sampleRate):

    arr = os.listdir(directory_resample)
    for file in arr:
        
        if file[-3:] == "wav":
            fullPath = directory_resample + "\\" + file;
            waveform, sample_rate = torchaudio.load(fullPath)
            
            print("***************")
            print(fullPath)
            metadata = torchaudio.info(fullPath)
            print(metadata)

            downsample_rate=sampleRate
            downsample_resample = torchaudio.transforms.Resample(
                sample_rate, downsample_rate, resampling_method='sinc_interpolation')

            down_sampled = downsample_resample(waveform)

            torchaudio.save(fullPath, down_sampled, downsample_rate)

            metadata = torchaudio.info(fullPath)
            print(metadata)




    



def VOSK_wav(filename , directory_voice , directory_text):
    SetLogLevel(0)
    file_split = filename[:-4]

    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    wf = wave.open(directory_voice + "\\" + filename , "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    #delete text of file
    open(directory_text + "\\" + file_split + ".txt", 'w').close()

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            string = rec.Result()
            text = string[string.find('"text"')+10:-3] + " "
            f = open(directory_text + "\\" + file_split + ".txt", "ab")
            f.write(text.encode("utf-8"))
            f.close()
        
    string = rec.FinalResult()
    text = string[string.find('"text"')+10:-3].encode("utf-8")
    f = open(directory_text + "\\" + file_split + ".txt", "ab")
    f.write(text)
    f.close()
    print(filename + " is done")



def Google_wav(filename , directory_voice , directory_text):
    #!/usr/bin/env python3

    # obtain path to "english.wav" in the same folder as this script
    from os import path
    AUDIO_FILE = (directory_voice + "\\" + filename)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        file_split = filename[:-4]

        ##delete text of file
        open(directory_text + "\\" + file_split + ".txt", 'w').close()

        f = open(directory_text + "\\" + file_split + ".txt", "ab")
        f.write(r.recognize_google(audio,language ='fa-IR').encode("utf-8"))
        f.close()

        print(filename + " is done")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))





