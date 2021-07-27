import matplotlib.pylab as plt
import IPython.display as ipd
import sys
sys.path.append('waveglow2/')
import numpy as np
import torch
from hparams import create_hparams
from train import load_model
from text import text_to_sequence
from denoiser import Denoiser

from pydub import AudioSegment
import pygame
import Cache_and_play
from shutil import copyfile
import pathlib
import csv
sciezka = pathlib.Path(__file__).parent.absolute()

import converters

# Function from Tacotron2
def plot_data(data, figsize=(16, 4)):
    fig, axes = plt.subplots(1, len(data), figsize=figsize)
    for i in range(len(data)):
        axes[i].imshow(data[i], aspect='auto', origin='bottom',
                       interpolation='none')

# Plays, saves and caches a generated voice
def play_and_save(voice, tekst):
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(str(sciezka) + r"\audio.wav")
    my_sound.play()
    pygame.time.wait(int(my_sound.get_length() * 1000))


    cached, cached_iter = Cache_and_play.setup_cache()

    copyfile(str(sciezka) + r"\audio.wav", str(sciezka) + r"\Cached\\" + "{}.wav".format(int(cached_iter)+1))
    with open("Iter.txt", "w") as f:
        f.write(str(int(cached_iter)+1))

    with open('Cached.csv', 'a') as f:
        text = ["{}.wav".format(int(cached_iter)+1)]
        text.append(voice)
        text.append(tekst)


        writer = csv.writer(f)
        writer.writerow(text)

# Using Tacotron2 generates a voice. (Contains a check for a dot at the end of a string, to properly generate a voice)
def generate(name_generuj, tekst_generuj):

    text = tekst_generuj

    # Check for dot at the end of text
    if not text[-1] == '.':
        text = text + '.'

    # generowany_glos = name_dict(name_generuj)


    # Generating the voice
    hparams = create_hparams()
    hparams.sampling_rate = 22050

    # tacotron2_statedict2.pt
    checkpoint_path = "outdir/ready/" + str(name_generuj)
    model = load_model(hparams)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    _ = model.cuda().eval().half()

    waveglow_path = 'waveglow_256channels_universal_v5.pt'
    waveglow = torch.load(waveglow_path)['model']
    waveglow.cuda().eval().half()
    for k in waveglow.convinv:
        k.float()
    denoiser = Denoiser(waveglow)


    sequence = np.array(text_to_sequence(text, ['basic_cleaners']))[None, :]
    sequence = torch.autograd.Variable(
        torch.from_numpy(sequence)).cuda().long()

    try:
        mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
        plot_data((mel_outputs.float().data.cpu().numpy()[0],
                   mel_outputs_postnet.float().data.cpu().numpy()[0],
                   alignments.float().data.cpu().numpy()[0].T))
    except ValueError:
        pass
    with torch.no_grad():
        audio = waveglow.infer(mel_outputs_postnet, sigma=1.000)

    # audio_denoised = denoiser("audio.wav", strength=0.06)[:, 0]

    audio = ipd.Audio(audio[0].cpu().numpy(), rate=hparams.sampling_rate)
    audio = AudioSegment(audio.data, frame_rate=22050, sample_width=2, channels=1)
    audio.export("audio.wav", format="wav", bitrate="64k")

    play_and_save(name_generuj, tekst_generuj)

# Using previous functions and the split_str() function, chops a long text into a few generated voices
def long_gen(glos, input, max_char=300):

    input = converters.split_str(input, max_char)
    # print("Returned input: ", input)
    for item in input:
        # print("Iter: ", input.index(item), "Text: ", item)
        generate(glos, item)
