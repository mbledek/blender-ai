import requests
import string
from googlesearch import search
from bs4 import BeautifulSoup
import re
import cleverbotfree
from googletrans import Translator


#URL Header
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

# The google_query function i basically copied from Google's documentation. The only thing I changed is the language
# and the 'fallback' response to Polish
def google_query(query, index=0):
    # print(query)
    # If you want to change it to English it should be
    """I don't know how to respond."""
    fallback = 'Przepraszam, nie wiem co odpowiedzieć.'
    result = ''

    try:
        search_result_list = list(search(query, tld="com", lang = "pl",  num=10, stop=3, pause=1))

        page = requests.get(search_result_list[index])

        soup = BeautifulSoup(page.content, features="lxml")

        article_text = ''
        article = soup.findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        article_text = article_text.replace('\n', '')
        first_sentence = article_text.split('.')
        first_sentence = first_sentence[0].split('?')[0]

        chars_without_whitespace = first_sentence.translate(
            { ord(c): None for c in string.whitespace }
        )

        if len(chars_without_whitespace) > 0:
            result = first_sentence
        else:
            result = fallback

        return result
    except:
        if len(result) == 0: result = fallback
        return result


# The get_data function uses requests and soup to output data from a given URL and a <div class= > name
def get_data(givenURL, givendataa):
    page = requests.get(givenURL, headers=HEADERS, timeout=240)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup.find_all("div",{"class": givendataa})

# The get_joke function uses the get_data function to output a joke from a Polish website
def get_joke():
    joke = get_data("http://www.kinyen.pl/dowcipy/losowy/", "joke")

    joke = re.sub(str("""<div class="joke">"""), "", str(joke[0]))
    joke = re.sub("""<br/>""", "", joke)
    joke = re.sub("""</div>""", "", joke)

    return joke

# Cleverbot is a WIP module, since there is a lot of trouble to handle HTML utf-8 formatting. I suppose that if you use
# it in English, you'll do just fine
def cleverbot(input):
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        bot = c_b.single_exchange(input)
        print("Bot: ", bot)

        return bot

# The translate function, as the name suggests, translates a given input into Polish. You can change the output language
# by changing the 'dest= ' to a language of your choice
def translate(input):
    translator = Translator()
    translations = translator.translate(str(input), dest='pl')

    return translations.text

# The get_fact function uses get_data and translate functions to output a fact from Google, translated into Polish.
# If you want to output non-translated (English) facts, just add # before the last two lines with translate function
def get_fact():
    page = requests.get("https://www.google.com/search?q=random+facts", headers=HEADERS, timeout=240)
    soup = BeautifulSoup(page.content, 'html.parser')
    fact_quest = soup.find_all("div",{"class": "sW6dbe"})
    fact_text = soup.find_all("div",{"class": "EikfZ"})

    fact_quest = re.sub(r"""<div class="sW6dbe" jsname="H17AHc">""", "", str(fact_quest[0]))
    fact_quest = re.sub(r"""</div>""", "", fact_quest)

    fact_text = re.sub(r"""<div class="EikfZ" jsname="oQYOj">""", "", str(fact_text[0]))
    fact_text = re.sub(r"""</div>""", "", fact_text)

    fact_quest = translate(fact_quest)
    fact_text = translate(fact_text)


    return  str(fact_quest + " " + fact_text)


