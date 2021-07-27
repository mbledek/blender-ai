import re
import pickle
import os
import time

import subprocess
import pathlib
directory = pathlib.Path(__file__).parent.absolute()
import sys

import Cache_and_play
import Gen_play_save
import Wiki
import converters
import networking
import mail
import dictionaries
import network_search


# Number of characters that your GPU can handle in one Tacotron2 generation
# GTX 1060 at max_decoder_steps = 2000 can handle ~380 characters, so 300 is a safe limit
max_char = 300

# Voices that you want to use
STT_voice = "V_male"
IP_voice = "Silverhand"
mail_voice = "Silverhand"
wikipedia_voice = "V_female"
google_voice = "V_female"
joke_voice = "V_female"
fact_voice = "V_female"







# Variables
voice = []
output = []
text_mail = []
STT = ""

# Determines how often it will check email to prevent Google blocking us
mail_iter = 0
mail_freq = 100

input_wiki = False
input_google = False
input_joke = False
input_fact = False
output_TTS = True



# Setup all modules that require setup

subprocess.Popen([sys.executable, directory.__str__()+r"\final_STT.py"])
networking.get_L1()
Cache_and_play.setup_cache()


while True:
    Jarvis = input("Start Jarvis?")
    Jarvis = converters.convert_to_boolean(Jarvis)

    if Jarvis == False:
        break

    while Jarvis == True:
        #
        # Inputs
        #

        # Checking STT
        """Now, STT works a bit differently than other modules. In order to listen to the user ALL the time, rather than
            in a specific moment, while also freezing the engine, STT is handled in a different python process started
            by subprocess.Popen in the beginning. This process saves what it heard in STT.pkl and immediately starts to 
            listen again, which prevents the program from not hearing what you said. This way, Jarvis will hear 
            everything that you say, while also working properly. The only downside is that the engine checks STT in 
            a given moment of the code, which means that if it's stuck (or simply doing something else entirely) you may
            notice a delay between STT hearing you, Jarvis handling it and then Jarvis' reaction"""
        if os.path.isfile('STT.pkl') == False:
            with open("STT.pkl", "wb") as f:
                pickle.dump(STT, f)
        with open('STT.pkl', 'rb') as f:
            STT = pickle.load(f)
            # print("STT: ", STT, "Type: ", type(STT))
        with open("STT.pkl", "wb") as f:
            pickle.dump("", f)
        if not STT == "":
            # Returns text to say and STT_var which tells Jarvis which input (or outpus) it should use
            STT, STT_var = dictionaries.STT_dict(STT)

            # Recognizing STT_var as defined input or output
            if STT_var == "input_wiki": input_wiki = True
            if STT_var == "output_TTS": output_TTS = True
            if STT_var == "input_google": input_google = True
            if STT_var == "input_joke": input_joke = True
            if STT_var == "input_fact": input_fact = True


            if STT == None:
                STT = ""
            elif not STT == "":
                output.append(STT)
                voice.append(STT_voice)
                # print("Dict STT: ", STT)
                STT = ""


        # IP Checking
        #
        # Returns two lists with all the IPs that are new or have disappeared
        new_IP, gone_IP = networking.check_for_new()
        # New IPs
        if len(new_IP) != 0:
            # If you want to change it to English it should be
            """Found a new device with this address: """
            IP_text = "Znaleziono nowe urządzenie z adresem: "
            for item in new_IP:
                IP = re.sub('192.168.', '', new_IP[new_IP.index(item)])
                output.append(str(IP_text + IP))
                voice.append(IP_voice)
            output_TTS = True
        # Gone IPs
        if len(gone_IP) != 0:
            # If you want to change it to English it should be
            """Found a device that's gone with this address: """
            IP_text = "Odłączono urządzenie z adresem: "
            for item in gone_IP:
                IP = re.sub('192.168.', '', gone_IP[gone_IP.index(item)])
                output.append(str(IP_text + IP))
                voice.append(IP_voice)
            output_TTS = True

        # Receiving generated voices and Human Input
        if mail_iter == mail_freq:
            # Returns a list with text from mails with 'Human Input' subject, so that you can write a mail to Jarvis
            # and he will say what you wrote
            text_mail = mail.jarvis_mail()
            mail_iter = 0
        if not text_mail == []:
            for item in text_mail:
                output.append(text_mail[text_mail.index(item)])
                voice.append(mail_voice)
            output_TTS = True


        # Wikipedia

        # Here Jarvis pull the output that STT dictionary returned so that the Wikipedia module knows what to search
        # and then searches it on Wikipedia. If you want to change the language, check the Wiki.py file
        if input_wiki == True and networking.have_internet() == True:
            if Wiki.check_input(output[0]) == True:
                x = 1
                wiki_output = ""
                while (len(wiki_output) < 100):
                    wiki_output = Wiki.get_summary(output[0], x)
                    x = x + 1
                output.append(wiki_output)
                voice.append(wikipedia_voice)
                output.pop(0)
                voice.pop(0)
                output_TTS = True
            else:
                output.append(Wiki.check_input(output[0]))
                voice.append(wikipedia_voice)
                output.pop(0)
                output_TTS = True
        elif input_wiki == True and networking.have_internet() == False:
            # If you want to change it to English it should be
            """I don't have Internet connection to search it now. Try again later"""
            output.append("Nie mogę wyszukać z powodu braku Internetu. Spróbuj ponownie później.")
            voice.append(wikipedia_voice)
            output.pop(0)
            output_TTS = True

        # Google search

        # Google search works the same as Wikipedia, so I don't think I have to explain it. If you want to
        # change the language check the network_search.py file
        if input_google == True and networking.have_internet() == True:
            output.append(network_search.google_query(output[0]))
            voice.append(google_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True
        elif input_google == True and networking.have_internet() == False:
            # If you want to change it to English it should be
            """I don't have Internet connection to search it now. Try again later"""
            output.append("Nie mogę wyszukać z powodu braku Internetu. Spróbuj ponownie później.")
            voice.append(google_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True

        # Random joke

        # Random joke uses requests and BeautifulSoup to get a joke from some random Polish website that I found.
        # If you want to change it to English it's will require some tinkering. You will have to change the website and
        # the '<div class= >' for the one that you are looking for
        if input_joke == True and networking.have_internet() == True:
            output.append(network_search.get_joke())
            voice.append(joke_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True
        elif input_joke == True and networking.have_internet() == False:
            # If you want to change it to English it should be
            """I don't have Internet connection to search it now. Try again later"""
            output.append("Nie mogę wyszukać z powodu braku Internetu. Spróbuj ponownie później.")
            voice.append(joke_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True

        # Random fact

        # Translated from Google into Google Translate since I couldn't find any Polish websites with random facts
        # If you want to change it to English check the network_search.py file and add # before translating
        if input_fact == True and networking.have_internet() == True:
            output.append(network_search.get_fact())
            voice.append(fact_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True
        elif input_fact == True and networking.have_internet() == False:
            # If you want to change it to English it should be
            """I don't have Internet connection to search it now. Try again later"""
            output.append("Nie mogę wyszukać z powodu braku Internetu. Spróbuj ponownie później.")
            voice.append(fact_voice)
            output.pop(0)
            voice.pop(0)
            output_TTS = True





        #
        # Outputs
        #


        # Text-to-speech
        # I've decided to implement this in order to prevent the Text to speech system from failing due to no
        # characters to generate from. You could try to prevent those situations from happening in the inputs, but for
        # me this was more universal
        if len(output) != 0:
            for item in output:
                if output[0] == "" or output[0] == None:
                    output.pop(0)
                    voice.pop(0)
        if not output == [] and output_TTS == True:
            print("Output: ", output)
            # Converting the text with numbers in it to text with numbers as you would say them
            output[0] = converters.numbtext_to_texttext(output[0])
            # Changing the voice name to the actual file name (Geralt -> Witcher3_Geralt_48000)
            voice[0] = dictionaries.name_dict(voice[0])
            # Checking if this text + voice were already generated. If they were, the search_cached() function already
            # plays the generated file
            if Cache_and_play.search_cached(voice[0], output[0]) == False:
                Gen_play_save.long_gen(voice[0], output[0], max_char)
            output.pop(0)
            voice.pop(0)
            if output == []:
                output_TTS = False

        # Handling boolean inputs and mail iteration counter
        input_wiki = False
        input_google = False
        input_joke = False
        input_fact = False

        mail_iter += 1

        time.sleep(1)


