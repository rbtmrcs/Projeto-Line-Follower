import cv2
import numpy as np
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError

'''
upper_green = np.array([107, 255, 255])
lower_green = np.array([49, 50, 50])

lower_red1 = np.array([0, 65, 75])
upper_red1 = np.array([12, 255, 255])
lower_red2 = np.array([240, 65, 75])
upper_red2 = np.array([256, 255, 255])

lower_yellow = np.array([16, 76, 72])
upper_yellow = np.array([30, 255, 210])
'''
class Baterpub:
    def __init__(self):
      self.pub1 = rospy.Publisher('/bater', String)
      self.pub2 = rospy.Publisher('/andar1', String)
      self.bridge = CvBridge()
      self.sub = rospy.Subscriber("/camera_image",Image, self.callback)

    def publ1(self,walk):
        self.pub2.publish(walk)
    
    def publ2(self):
        self.pub1.publish('bate la')
    
    def callback(self,data):
        LimiarBinarizacao = 125
        kernel = np.ones((2,2), np.uint8)
        frame = self.bridge.imgmsg_to_cv2(data,"bgr8")
        x = 0
        y = 0
        w = 0
        h = 0
        lower_verde = np.array([0, 65, 75])
        upperupper_verde = np.array([12, 255, 255])
        lower_laranja = np.array([16, 76, 72])
        upperupper_laranja = np.array([30, 255, 210])
        height = np.size(frame,0)
        width= np.size(frame,1)
        frame2 = frame[height/1.5:height, 0:width]
        frame_hsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        frame_mask = cv2.inRange(frame_hsv, lower_verde, upperupper_verde)
        frame_tratado3 = cv2.dilate(frame_mask, None, iterations=5)
        frame_tratado1 = cv2.erode(frame_tratado3, kernel, iterations = 1)
        FrameBinarizado1 = cv2.threshold(frame_tratado1,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
        FrameBinarizado2 = cv2.dilate(FrameBinarizado1,None,iterations=1)
        __,cnts2, __ = cv2.findContours(FrameBinarizado2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(FrameBinarizado2,cnts2,-1,(0,255,0),3)
        print type(cnts2)
        for c in cnts2:
            area = cv2.contourArea(c)
            if area > 3500:
                x, y, w, h = cv2.boundingRect(c)
        if x+y+w+h!=0:
            bater.publ2()
            print('proximo estado')# essa parte manda pro arquivo objeto.py

        frame1 = frame[height/1.5:height, 160:480]
        frame_hsv=cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        frame_mask = cv2.inRange(frame_hsv, lower_laranja, upperupper_laranja)
        frame_tratado3 = cv2.dilate(frame_mask, None, iterations=5)
        frame_tratado1 = cv2.erode(frame_tratado3, kernel, iterations = 1)
        FrameBinarizado1 = cv2.threshold(frame_tratado1,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
        FrameBinarizado2 = cv2.dilate(FrameBinarizado1,None,iterations=1)
        __,cnts, __ = cv2.findContours(FrameBinarizado2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(FrameBinarizado2,cnts,-1,(0,255,0),3)
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 3500:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (16, 76, 72), 2)
        m = cv2.moments(frame_mask, False)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2
        cv2.circle(frame1,(int(cx), int(cy)), 10,(0,0,255),-1)
        if x+y+w+h!=0:
            if 128 < cx and 192 > cx:
                print('em frente')
                walk='frente'
                bater.publ1(walk)
            elif 64 < cx and 128 > cx:
                print('vire a esquerda')
                walk='esquerda'
                bater.publ1(walk)
            elif 192 < cx and 256 > cx:
                print('vire a direita')
                walk='direita'
                bater.publ1(walk)
            elif  64 > cx:
                print('vira muito e')
                walk='muito esquerda'
                bater.publ1(walk)
            elif  256 < cx:
                walk='muito direita'
                bater.publ1(walk)
                print('vira muito d')
        else:
            walk='nao achei'
            bater.publ1(walk)
            print('Linha nao encontrada')
    



if __name__=='__main__':  
   rospy.init_node('andando_1', anonymous=True)
   bater= Baterpub()
   rospy.spin()

