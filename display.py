
import numpy as np
import cv2
import screeninfo
import time

img1 = cv2.imread('background.png', 0)
img2 = cv2.imread('background.png', 0)
img3 = cv2.imread('background.png', 0)
img4 = cv2.imread('background.png', 0)
img5 = cv2.imread('background.png', 0)
img5 = cv2.imread('background.png', 0)
scale_percent = 1000  # percent of original size
screen = screeninfo.get_monitors()[0]
dim = (screen.width, screen.height)

resized1 = cv2.resize(img1, dim)
resized2 = cv2.resize(img2, dim)
resized3 = cv2.resize(img3, dim)
resized4 = cv2.resize(img4, dim)
resized5 = cv2.resize(img5, dim)
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (450, 600)

# fontScale
fontScale = 4

color = (255, 0, 0)

# Line thickness of 2 px
thickness = 4

while cv2.waitKey(2000) != ord(' '):
    text = "Bienvenue"
    cv2.putText(resized1, text, org, font, fontScale,
                color, thickness, cv2.LINE_AA, False)

    cv2.imshow("image", resized1)
    text = "dans GIF4000"
    cv2.waitKey(1000)
    cv2.putText(resized2, text, org, font, fontScale,
                color, thickness, cv2.LINE_AA, False)

    cv2.imshow("image", resized2)

    text = "Appuyez sur"
    cv2.waitKey(1000)
    cv2.putText(resized3, text, org, font, fontScale,
                color, thickness, cv2.LINE_AA, False)

    cv2.imshow("image", resized3)

    text = "Pomme et C"
    cv2.waitKey(1000)
    cv2.putText(resized4, text, org, font, fontScale,
                color, thickness, cv2.LINE_AA, False)

    cv2.imshow("image", resized4)

    text = "Pour commencer"
    cv2.waitKey(1000)
    cv2.putText(resized5, text, org, font, fontScale,
                color, thickness, cv2.LINE_AA, False)

    cv2.imshow("image", resized5)


cv2.destroyAllWindows()
