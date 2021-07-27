import wikipedia
wikipedia.set_lang("pl")

# A simple usage of wikipedia module - returns a summary of a given text and with a given number of sentences
def get_summary(wiki_tekst, length):
    return wikipedia.summary(wiki_tekst, sentences=int(length))

# Checks if a wikipedia search is valid and if there actually is a wikipedia website connected to this search
def check_input(wiki_tekst):
    try:
        wikipedia.summary(wiki_tekst)
        return True
    except wikipedia.exceptions.DisambiguationError as e:
        return e.options
    except wikipedia.exceptions.PageError:
        return "Nie ma takiej strony."
