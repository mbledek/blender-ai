#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import pickle

STT = ""
with open('STT.pkl', 'wb') as f:
    pickle.dump(STT, f)

# obtain audio from the microphone
r = sr.Recognizer()


# Simply uses Speech Recognition and Google's Speech Regognition to generate a text from what you are saying
while True:
    with sr.Microphone() as source:
        # print("Say something!")
        audio = r.listen(source)


    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Recognized: ", str(r.recognize_google(audio, language="pl-PL")))
        STT = str(r.recognize_google(audio, language="pl-PL"))
    except sr.UnknownValueError:
        print("Nie zrozumiałem co powiedziałeś")
        STT = "Nie zrozumiałem co powiedziałeś"
    except sr.RequestError as e:
        print("Błąd: {0}".format(e))

    with open('STT.pkl', 'wb') as f:
        pickle.dump(STT, f)
        # print("STT dumped!")

    STT = ""



