import app_control as phone
import random
import time

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
print("waiting to start loop")
time.sleep(10)
print("START")
try:
    while True:
        loop()
except KeyboardInterrupt:
    pass
