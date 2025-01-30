      
import winsound

import cv2 
import numpy as np


# Web camera
cap = cv2.VideoCapture('video.mp4')


min_width_react = 80 #min width reactangel
min_height_react = 80
count_line_position = 550

#Initialize Substructor --> it substract the background of the object and focus on the object 
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x,y,w,h):
    x1= int(w/2)
    y1= int(h/2)
    cx = x+x1
    cy = y+y1
    return cx , cy

detect = []
offset = 6 #Allowable error between pixel 
counter=0
while True:
    ret,frame1 = cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur =  cv2.GaussianBlur(grey,(3,3),5)
    # applying on each frame 
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5))) #(dilate)it's specify the object with
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat , cv2.MORPH_CLOSE,kernel)
    dilatada = cv2.morphologyEx(dilatada , cv2.MORPH_CLOSE,kernel)
    conterSahpe,h= cv2.findContours(dilatada,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # In countersahp height is compelsory 

    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),2)  #This code is used for drawing a line 

    for (i,c) in enumerate(conterSahpe):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h>= min_height_react)
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        

        center=center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,2,(0,0,255),-1)
        cv2.putText(frame1,"Vehicle"+str(counter),(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,244,0),2)    
        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
                cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
                detect.remove((x,y))    
                
                print("Vehicle Counte:"+str(counter))

    cv2.putText(frame1,"VEHICLE COUNTER :"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)        

    alarm = False
    alarm_mode = False
    alarm_counter = 0 
    
    def beep_alarm ():
        global alarm
        for _ in range (5):
            if not alarm_mode:
                break 
            print("ALARM")
            winsound.Beep(2500,1000)
        alarm = False 


  #  cv2.imshow('Detecter',dilatada)
    cv2.imshow('video original',frame1)

    if cv2.waitKey(1)==13: # 13 is use for closing the window when we press enter key
        break

cv2.destroyAllWindows()
cap.release()