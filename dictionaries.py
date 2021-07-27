import re
import network_search

# Polish dictionary with stuff that Jarvis should respond to according to what STT thinks you said. This contains
# noticing things like 'wikipedia', 'google me this' and so on, which then is returned in a format "text to say", which
# input/output it is
def STT_dict(input):
    # print("Input: ", input)
    input = input.lower()
    # print("Lower input: ", input)
    if "jarvis" in input or "serwis" in input:
        input = re.sub("jarvis", "", input)
        # input = re.sub("dżarwis", "", input)
        if "wikipedia" in input or "wiki" in input or "co to jest" in input:
            # Jarvis_engine.wiki_output = True
            input = re.sub("wikipedia", "", input)
            input = re.sub("wiki", "", input)
            input = re.sub("co to jest", "", input)
            
            STT_var = "input_wiki"

            return input, STT_var
        if "pogoda" in input or "pogodę" in input:
            STT_var = "output_TTS"

            # print("Pogoda nie została jeszcze zaprogramowana")
            return "Pogoda nie została jeszcze zaprogramowana", STT_var
        if "światła" in input or "światło" in input:
            STT_var = "output_TTS"

            # print("Kontrola świateł nie została jeszcze zaprogramowana")
            return "Kontrola świateł nie została jeszcze zaprogramowana", STT_var
        if "mail" in input or "email" in input or "e-mail" in input or "maila" in input:
            STT_var = "output_TTS"

            # print("Imejl nie został jeszcze zaprogramowany")
            return "Imejl nie został jeszcze zaprogramowany", STT_var
        if "google" in input:
            input = re.sub("google", "", input)

            STT_var = "input_google"

            return input, STT_var
        if "żart" in input:
            STT_var = "input_joke"

            return "Chętnie", STT_var
        if "ciekawostka" in input or "fakt" in input or "ciekawostkę" in input:
            STT_var = "input_fact"

            return "Chętnie", STT_var
        else:

            STT_var = "output_TTS"

            if "kim jesteś" in input:
                return "Jestem zwycięzcą", STT_var
            elif "możesz zrobić" in input:
                return "Porozmawiać, sprawdzić maila i sieć", STT_var
            elif "Cię stworzył" in input:
                return "Tego dalej nikt nie wie", STT_var


            elif "gwint" in input or "gwinta" in input:
                return "Kolego, kupiłeś mnie tym jak paczkę żelków", STT_var
            elif "bywaj" in input:
                return "Ja kurwa jestem a nie bywam", STT_var
            elif "problem z potworem" in input:
                return "Problem. Dobre sobie. W czarnej dupie jesteśmy, a nie problem mamy", STT_var
            elif "fraszkę" in input:
                return "Lambert, Lambert, Ty. Zbóju", STT_var
            elif "białe zimno" in input:
                return "Gdy nadzejdzie czas Białego Zimna, nie jedz żółtego śniegu", STT_var
            elif "wiedźmin" in input:
                return "Oddawać moje rzeczy bo zajebie", STT_var
            elif "pobruszę" in input or "pobruszę" in input:
                return "Daj ać ja pobruszę, a Ty skocz do piwnicy po piwo", STT_var
            elif "szermierz" in input:
                return "Każdy szermierz dupa, kiedy wrogów kupa", STT_var

            elif "pytania" in input:
                return "Pytania są tendencyjne, a odpowiedzi z góry znane", STT_var
            elif "płaci" in input:
                return "Pan płaci, Pani płaci, My płacimy. To są nasze pieniądze proszę pana", STT_var
            elif "siara" in input:
                return "Memory. Fajnd. Siara. I wszystko jasne", STT_var
            elif "usmażyć" in input:
                return "Cycki se usmaż", STT_var
            elif "kopernik" in input:
                return "Kopernik był kobietą!", STT_var

            elif "kto ty jesteś" in input:
                return "polak mały", STT_var
            elif "nudzi mi się" in input or "nudzi mi sie" in input:
                return "Już nie mogłem się doczekać, aż to usłyszę", STT_var
            elif "hakuna matata" in input:
                return "Jak cudownie to brzmi", STT_var
            elif "tupta jeż" in input:
                return "Do Raszyna", STT_var
            elif "wola nieba" in input:
                return "Z nią się zawsze zgadzać trzeba", STT_var
            elif "ciemno wszędzie" in input:
                return "Co to będzie, co to będzie", STT_var
            elif "grał w gre" in input or "grał w grę" in input:
                return "Tumb Rajder", STT_var
            elif "daleko jeszcze" in input:
                return "No ale daleko czy nie", STT_var
            elif "bagno" in input:
                return "To moje bagno", STT_var
            elif "kwiat i kolce" in input:
                return "Lepiej by było gdybym nie był daltonistą", STT_var
            elif "z kości chleb" in input:
                return "Gwoli ścisłości, tak to robią olbrzymy. Za to ogry… Aaa, no, tu jest gorzej. Ogry robią " \
                       "sobie rękawiczki z ludzkiej skóry i breloczki z wątroby, wyciskają ofierze białko z oczu. " \
                       "Najlepiej smakuje na tostach.", STT_var
            elif "jak cebula" in input:
                return "Cebula ma warstwy! Ogry mają warstwy! Cebula ma warstwy, dociera?", STT_var
            # elif "" in input:
                # return ""
    if "cleverbot" in input:
        STT_var = "output_TTS"
        input = re.sub("cleverbot", "", input)
        return network_search.cleverbot(input), STT_var


    elif "nie zrozumiałem co powiedziałeś" == input:
        STT_var = "output_TTS"
        return "Nie zrozumiałem co powiedziałeś", STT_var

    else:
        return None, None

# A dictionary used in mail converting
def mail_dict(input):
    output = []
    for i in range(int(len(input)/2)):
        if input[i*2] == "Human Input":
            output.append(str("Human Input: " + str(input[i*2+1])))
        elif input[i*2] == "Received audio":
            output.append("ATTACHMENT")
    return output

# Converting character names to actual file names
def name_dict(name):
    if name == "Bezi" or name == "bezi" or name == "Bezimienny" or name == "bezimienny":
        name = "Gothic_Bezi_201000"
    elif name == "Ciri" or name == "ciri" or name == "Zireael" or name == "zireael":
        name = "ciri_31500"
    elif name == "Silverhand" or name == "silverhand" or name == "Johnny" or name == "johnny":
        name = "Silverhand_20000"
    elif name == "Geralt" or name == "geralt":
        name = "Witcher3_Geralt_48000"
    elif name == "Yen" or name == "yen" or name == "Yennefer" or name == "yennefer":
        name = "Witcher3_Yennefer_1800"
    elif name == "Odim" or name == "odim" or name == "Pan Lusterko" or name == "pan lusterko":
        name = "odim_22000"
    elif name == "Regis" or name == "regis":
        name = "Witcher3_Regis_7000"
    elif name == "V_male" or name == "v_male":
        name = "V_male_16000"
    elif name == "V_female" or name == "v_female":
        name = "V_female_4700"
    return name