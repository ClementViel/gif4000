import cv2
import os
import rest_piwigo
import qrcode
import imageio
from PIL import Image
from tkinter import *

def get_qr_code(url):
    print(url)
    code = qrcode.make(url)
    code.save("code.png")

def send_gif_to_server(gif_path):
   link = rest_piwigo.send_to_share(gif_path)
   return link
    # this function sends picture to

def show_gif(gif_path, win_name):
    print(f"showing gif {gif_path} in image {win_name}")
    img = imageio.mimread(gif_path)
    if img is None:
        print("image is None")
        return
    num = len(img)
    print(f"there are {num} images")
    cv2.namedWindow(win_name)
    i = 0
    print("Coucou avant while")
    while True:
        cv2.imshow(win_name, img[i])
        if cv2.waitKey(100)&0xFF == 97:
            break
        i = (i+1)%num
    print("destroying win")
    cv2.destroyWindow(win_name)
