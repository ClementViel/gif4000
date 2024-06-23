import app_control as phone
import random
import time
import display as video
import sound as audio
import threading
import bluetooth
import shutil
import datetime
import os
from pytimedinput import timedKey
# connect to phone to control it:
#   - start app
#   - loop over take photo
#   - pull gif and rename it.
num_pic = 30
num_gif = 0


def shuffle_list(liste):
    liste = list(range(1, 21))
    random.shuffle(liste)

def copy_to_gallery(num_gifs):
    for idx in range(0, num_gifs):
       filename = "gif" + str(idx) + ".gif"
       new_name = "gif" + str(datetime.datetime.utcnow()) + ".gif"
       shutil.copy2("/home/clem/Projets/gif4000/" + filename,
                 "/home/clem/Projets/gif4000/showroom/public/images/photos/" + new_name)


def loop(thread_audio):
    global num_gif
    gif = 0
    max_gif = 3
    waiting = True
    thread_audio.start()
    for gif in range(0, max_gif):
        for idx in range(0, num_pic):
            print("take photo ", idx)
            phone.take_photo(serial)
            time.sleep(delay_list[idx]/1000)
    for gif in range(0, max_gif):
        phone.pull_gif(serial, gif)
    phone.erase_dir(serial)
    audio_select("play", "partage", 0)
    audio_select("play", "partage", 1)
    audio_select("play", "partage", 2)
      #  copy_to_attachement()
    while waiting == True:
        key, timeout = timedKey(timeout=5, allowCharacters="bszd")
        print(key)
        if key == "s" :
            print("copied to gallery")
            copy_to_gallery(max_gif)
        elif key == "z":
            waiting=False
    thread_audio.join()

def remove_attachment(path):
    try:
        os.remove(path)
    except:
        print("nothing to RM")


def audio_accident(seq_array):
        for audio_seq in seq_array:
            if  audio_seq != 0:
                path = "/home/clem/Projets/gif4000/audio/" + audio_seq
                audio.playSound(path)
            else:
                time.sleep(5)

def audio_select(function, moment, track):
    if function == "play":
        if moment == "intro":
            filename="intro" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "explications":
            filename="exp" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "exec":
            filename="exec" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "partage":
            filename="partage" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "conclu":
            filename="conclu" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "attente":
            filename="attente" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename

        else:
            print("not the good sound")
        print("playing audio ",path)
        audio.playSound(path)


def init_randoms():
    # clean attachements
    # Generate random delays
    for num in range(0, num_pic):
        delay_list.append(random.randrange(100, 300, 50))
    
    print(delay_list)
    #track = random.randint(0, 4)
    track = 0
    
    remove_attachment("/home/clem/Projets/gif4000/public_html/images/gif0.gif")
    # generation tableau séquence
    sequence = ["ok1.mp3", 0, 0,  "ok2.mp3", 0, 0, 0, "ok3.mp3"]
    # generation du nombre d'accident
    accident_num = random.randint(1,3)
    # placement des accidents.
    for index in range(accident_num):
            #tirage au sort du numéro de l'accident
            accident_idx = random.randint(0, 8)
            accident_place = random.choice([1, 2, 4, 5, 6])
            print(accident_place)
            sequence[accident_place] = "accident" + str(accident_idx) + ".mp3"
    
    print(sequence)
    return sequence

def waitKey(exp_key):
    waiting = True
    while waiting == True:
       # audio_select("play", "attente", 0)
        print("waiting for key")
        key, timeout = timedKey(timeout=5, allowCharacters=exp_key)
        print(exp_key)
        if key == exp_key:
            waiting = False



serial = phone.connect_to_phone()

if serial is None:
    print("serial is None, connect phone and relaunch")
    sys.exit(0)

delay_list = []
phone.turn_on_screen(serial)
phone.unlock_phone(serial)
phone.unlock_phone(serial)
phone.unlock_phone(serial)
phone.start_app(serial)
phone.stop_app(serial)
phone.start_app(serial)


cond = False


while cond == False:
    waiting = True
    sequence = init_randoms()
    while waiting == True:
        audio_select("play", "attente", 0)
        print("waiting for key")
        key, timeout = timedKey(timeout=5, allowCharacters="q")
        if key == "q":
            waiting = False

    print(datetime.datetime.utcnow())


    print("START intro")
    audio_select("play", "intro", 0)
    audio_select("play", "intro", 1)
    audio_select("play", "intro", 2)
    audio_select("play", "intro", 3)
    audio_select("play", "intro", 4)
    waitKey("q") 
    execution_audio = threading.Thread(target=audio_accident, args=(sequence,))
    loop(execution_audio)
    # TODO : make sure start/join is always working
#    audio_select("play", "conclu", 0)
