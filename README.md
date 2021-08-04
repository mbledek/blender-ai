# Blender AI
This is a simple DIY smart assistant that I've decided to create when I stumbled upon Tacotron2. I thought that it would be extremely fun and interesting to create a smart assistant with a voice that I want. That's when Blender AI came to life. 

# What it can do
Right now Blender AI can:
- depict what your're saying
- search Wikipedia with what you've asked
- search Google with what you've asked
- tell you a random joke
- tell you a random fact
- tell you your desired weather 
- chat with cleverbot
- respond to what you've said according to a pre-written dictionary
- check your local network and tell you if there are any new (or gone) devices
- check your email and play all audio attachments and generate voice from a specified mail
- and of course, verbally tell you all the things above with a voice of your choice

Work in progress:
- Spotify control (play, pause, previous, next)

# To do
- release an English version
- make a few long-term tests and improve the code
- release a version of Blender AI for Raspberry PI
- expand the dictionary with pre-written responses

# Future goals and plans
My future goals for this project are to:
- make this code as clear as possible
- make this code easy to expand with your own modules
- use Blender AI as an actual smart assistant with IoT interactions:
- control of lights
- control of other IoT devices
- control of my other projects (possibly IoT robots)
- control old devices with IR controls

# Installation
First of all you have to choose between and installation for a CUDA enabled device that will handle the smart assistant AND will handle voice generation or if you choose to install it on two seperate devices - one that will handle the smart assistant and one that will ONLY handle voice generation

# Installation for one device

# Installation for two seperate devices

## Installation for the device that handles voice generation
1. First of all, clone the Mekatron repository that will handle most of the voice generation
```
git clone https://github.com/ajozefczak/mekatron2.git
```
2. Move into the /mekatron2 directory with
```
cd mekatron2
```
3. In this directory, clone this repository with
```
git clone https://github.com/mbledek/blender-ai.git
```
4. Install all necessary python modules with
```
pip install -r Rec_gen_send_requirements.txt
```
5. In the meantime change the "waveglow"'s directory's name to "waveglow2"
6. Install a **CUDA enabled version** of PyTorch: https://pytorch.org

## Installation for the device that wil handle the smart assistant
1. Clone this repository with
```
git clone https://github.com/mbledek/blender-ai.git
```
2. Install all necessary python modules with
```
pip install -r Jar_local_requirements.txt
```
3. Install pyaudio: https://www.lfd.uci.edu/~gohlke/pythonlibs/
4. Because of smtplib's 'ascii' formatting, you have to change it to 'utf-8':
5. Locate the smtplib.py (it should be in C:\Users\your_user_name\AppData\Local\Programs\Python\Python3x\Lib)
6. Change the line 855 from
```
msg = _fix_eols(msg).encode('ascii')
```
to
```
msg = _fix_eols(msg).encode('utf-8')
```
# Configuration
Check the Jarvis_config.py file in order to properly setup the assistant.

max_chars as explained in the file mean how many characters your GPU can generate in one go. If you will set a number too high, it just won't generate the last characters.

local_gen - True if you handle the smart assistant on one device, False if on two separate devices.

Next is a list of voices used in this assisant. You can freely change them to filenames of your Tacotron voices. You can find mine on [Mekatron's Discord server](https://discord.gg/S9dmsWBTha).

On the bottom are all the necessary credentials for handling mail. If you use only one device, you just have to setup username_sender and app_pass_sender (Google requires you to create a password for an application like this). If you use two devices, make sure to properly setup two mail accounts, and to setup both Jarvis_config.py on BOTH devices.
