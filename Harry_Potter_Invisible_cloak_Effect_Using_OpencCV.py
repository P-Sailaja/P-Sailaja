import cv2 as c
import numpy as np

#initial function for the callin of the trackbar
def hello(x):
    #only for reference
    print("")

#initialisation of the camera
cap = c.VideoCapture(0)
bars = c.namedWindow("bars")

c.createTrackbar("upper_hue", "bars", 110,180,hello)
c.createTrackbar("upper_saturation", "bars", 255,255, hello)
c.createTrackbar("upper_value", "bars", 255,255, hello)
c.createTrackbar("lower_hue", "bars", 68,180,hello)
c.createTrackbar("lower_saturation", "bars",55,255,hello)
c.createTrackbar("lower_value","bars", 54,255,hello)

#capturing the initial frame for creation of backgground
while(True):
    c.waitKey(1000)
    ret, init_frame = cap.read()
    #check if the frame is returned then brake
    if(ret):
        break

#start capturing the frame for actual magic!
while(True):
    ret, frame = cap.read()
    inspect = c.cvtColor(frame, c.COLOR_BGR2HSV)

    #getting the HSV values for masking the cloak
    upper_hue = c.getTrackbarPos("upper_hue", "bars")
    upper_saturation = c.getTrackbarPos("upper_saturation", "bars")
    upper_value = c.getTrackbarPos("upper_value", "bars")
    lower_value = c.getTrackbarPos("lower_value","bars")
    lower_hue = c.getTrackbarPos("lower_hue","bars")
    lower_saturation = c.getTrackbarPos("lower_saturation","bars")

    #kernel to be used for dilation
    kernel = np.ones((3,3),np.uint8)

    upper_hsv = np.array([upper_hue, upper_saturation,upper_value])
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])

    mask =c.inRange(inspect, lower_hsv, upper_hsv)
    mask = c.medianBlur(mask,3)
    mask_inv = 255-mask
    mask = c.dilate(mask,kernel,5)

    #The mixing of frames in a combination to achieve the required frame
    b= frame[:,:,0]
    g= frame[:,:,1]
    r= frame[:,:,2]
    b= c.bitwise_and(mask_inv, b)
    g= c.bitwise_and(mask_inv, g)
    r= c.bitwise_and(mask_inv, r)
    frame_inv = c.merge((b,g,r))

    b= init_frame[:,:,0]
    g= init_frame[:,:,1]
    r= init_frame[:,:,2]
    b= c.bitwise_and(b,mask)
    g= c.bitwise_and(g,mask)
    r= c.bitwise_and(r,mask)
    blanket_area = c.merge((b,g,r))

    final = c.bitwise_or(frame_inv, blanket_area)

    c.imshow("Harry's cloak", final)
    c.imshow("original", frame)

    if(c.waitKey(3) ==ord('q')):
        break;

c.destroyAllwindows()
cap.release()
    

    
    
