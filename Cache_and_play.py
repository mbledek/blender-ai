import os
from csv import reader
import pygame
import pathlib
sciezka = pathlib.Path(__file__).parent.absolute()

# Checks for all necessary folders and files to cache generated voices
def setup_cache():
    global cached
    global cached_iter
    if os.path.isfile('Cached.csv') == False:
        with open("Iter.txt", "w") as f:
            f.write("0")
        cached_iter = 0
        cached = []
    else:
        with open('Cached.csv', 'r') as f:
            csv_reader = reader(f)
            cached = list(csv_reader)
        with open('Iter.txt', 'r') as f:
            cached_iter = f.read()
    if not os.path.isdir(str(sciezka) + "\Cached"):
        os.mkdir(str(sciezka) + "\Cached")
    return cached, cached_iter

# Plays a cached file
def play_cached(location):
    global cached
    global cached_iter

    audio_name = cached[location][0]

    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(str(sciezka) + r"\Cached\\" + str(audio_name))
    my_sound.play()
    pygame.time.wait(int(my_sound.get_length() * 1000))

# Searches for a cached file - if there is, then it plays the file, if there isn't, it returns False
def search_cached(voice, text):
    global cached
    global cached_iter
    x = 0
    location = ""
    for sublist in cached:
        if text in sublist:
            location = x
            break
        else:
            x = x + 1
    if location == "":
        return False
    else:
        if voice in cached[x]:
            print("File cached! Playing now...")
            play_cached(x)
        else:
            return False