import cv2
import numpy as np

'''
upper_green = np.array([75, 255, 255])
lower_green = np.array([45, 100, 50])

lower_red1 = np.array([0, 65, 75])
upper_red1 = np.array([12, 255, 255])
lower_red2 = np.array([240, 65, 75])
upper_red2 = np.array([256, 255, 255])

lower_yellow = np.array([16, 76, 72])
upper_yellow = np.array([30, 255, 210])
'''
cap = cv2.VideoCapture(0)
LimiarBinarizacao = 125
kernel = np.ones((2,2), np.uint8)

while (True):
    __,frame = cap.read()
    if 1 == True:
        x = 0
        y = 0
        w = 0
        h = 0
        lower_laranja = np.array([0, 65, 75])
        upperupper_laranja = np.array([12, 255, 255])
        '''
        lower_laranja = np.array([45, 100, 50])
        upperupper_laranja = np.array([30, 255, 210])
        '''
        
        height = np.size(frame,0)
        width= np.size(frame,1)
        frame2 = frame[height/1.5:height, 0:width]
        frame_hsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)        
        
        frame_mask = cv2.inRange(frame_hsv, lower_laranja, upperupper_laranja)
        frame_tratado3 = cv2.dilate(frame_mask, None, iterations=5)
        frame_tratado1 = cv2.erode(frame_tratado3, kernel, iterations = 1)
        #frame_tratado2 = cv2.morphologyEx(frame_tratado1, cv2.MORPH_CLOSE, kernel)
        FrameBinarizado1 = cv2.threshold(frame_tratado1,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
        FrameBinarizado2 = cv2.dilate(FrameBinarizado1,None,iterations=1)
        #FrameBinarizado3 = cv2.bitwise_not(FrameBinarizado2)
        __,cnts, __ = cv2.findContours(FrameBinarizado2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(FrameBinarizado2,cnts,-1,(0,255,0),3)
        
        
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 3500:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (16, 76, 72), 2)
        m = cv2.moments(frame_mask, False)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2
        
        cv2.circle(frame2,(int(cx), int(cy)), 10,(0,0,255),-1)

        cv2.imshow('Paulo1',frame2)
        
        if  x+w+y+h==480:
            print('proximo estado')
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
