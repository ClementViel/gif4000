import app_control as phone
import random
import time
import display as video
import sound as audio
import threading
# connect to phone to control it:
#   - start app
#   - loop over take photo
#   - pull gif and rename it.
num_pic = 20
num_gif = 0


def shuffle_list(liste):
    liste = list(range(1, 21))
    random.shuffle(liste)


def loop():
    global num_gif
    print("this is gif num ", num_gif)
    for idx in range(0, num_pic):
        print("take photo ", idx)
        phone.take_photo(serial)
        time.sleep(delay_list[idx]/1000)
    time.sleep(10)
    phone.pull_gif(serial, num_gif)
    phone.erase_dir(serial)
    num_gif += 1

def thread_audio(function, moment):
    print("Thread audio starting")
    if function == "play":
        if moment == "intro":
            path = "/home/clem/Téléchargements/labyrinth-for-the-brain-190096.mp3"
        print("playing audio ",path)
        audio.playSound(path)

    elif function == "stop":
        video.setLoop(False)
 
def thread_video(function, moment):
    print("Thread starting")
    if function == "play":
        if moment == "intro":
            path = "/home/clem/Téléchargements/alb_glitch1029_1080p_24fps.mp4"
        print("playing video ",path)
        video.playVideo(path)

    elif function == "stop":
        video.setLoop(False)
    
serial = phone.connect_to_phone()

if serial is None:
    print("serial is None, connect phone and relaunch")
    sys.exit(0)

delay_list = []
phone.start_app(serial)
# Generate random delays
for num in range(0, num_pic):
    delay_list.append(random.randrange(300, 3000, 100))

print(delay_list)

# generate random scenarii list
list_scenar = list(range(0, num_pic))
random.shuffle(list_scenar)

print(list_scenar)

intro_video = threading.Thread(target=thread_video, args=("play", "intro"))
intro_audio = threading.Thread(target=thread_audio, args=("play", "intro"))
print("GIF4000 starting")
time.sleep(10)




print("START intro")
intro_audio.start()
intro_video.start()
print("waiting for audio to finish")
intro_audio.join()
video.setLoop(False)
phone.turn_on_screen(serial)
time.sleep(2)
phone.unlock_phone(serial)

try:
    while True:
        loop()
except KeyboardInterrupt:
    pass
