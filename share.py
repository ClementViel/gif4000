import cv2
import os
import rest_piwigo
import qrcode
import imageio

def show_qr_code(url):
    print(url)
    code = qrcode.make(url)
    code.save("code.png")
    img = cv2.imread("code.png")
    cv2.namedWindow("code", cv2.WINDOW_NORMAL)
    cv2.imshow("code",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def send_gif_to_server(gif_path):
   link = rest_piwigo.send_to_share(gif_path)
   return link
    # this function sends picture to

def show_gif(gif_path):
    img = imageio.mimread('2154.gif')
    if img is None:
        print("image is None")
        return
    num = len(img)
    print(f"{num} pictures in gif")
    cv2.namedWindow('gif', cv2.WINDOW_AUTOSIZE)
    i = 0
    while True:
        cv2.imshow("gif", img[i])
        if cv2.waitKey(100)&0xFF == 27:
            break
        i = (i+1)%num
    cv2.destroyAllWindows()

show_gif("new.gif")
