
import numpy as np
import cv2
import screeninfo
import time

loop = True

def setLoop(new_val):
    global loop
    print("set loop to ", new_val)
    loop = new_val

def playVideo(path):
    global loop
    print("Play video")
    # Create a VideoCapture object and read from input file 
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cap = cv2.VideoCapture(path)
    # Check if object opened successfully 
    if (cap.isOpened()== False): 
        print("Error opening video file") 
  
    # Read until video is completed 
    while(1): 
      
        # Capture frame-by-frame 
        ret, frame = cap.read() 
        # Display the resulting frame 
        if loop == True:
            if ret == False:
                cap = cv2.VideoCapture(path)
        else:
            print("loop is False")
        if cv2.waitKey(1) & 0xFF == ord('q') or loop == False:
            cap.release()
            cv2.destroyAllWindows()
            break
        if ret == True:
            cv2.imshow('image',frame)          

def stopVideo():
    print("Destroying all windows")
    cv2.destroyAllWindows()

