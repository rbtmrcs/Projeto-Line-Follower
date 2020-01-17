import cv2
import numpy as np
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError

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
        lower_laranja = np.array([0, 65, 75])
        upperupper_laranja = np.array([12, 255, 255])
        '''
        lower_laranja = np.array([45, 100, 50])
        upperupper_laranja = np.array([30, 255, 210])
        '''
        height = np.size(frame,0)
        width= np.size(frame,1)
        frame2 = frame[height/2:height, 0:width]
        frame_hsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)        
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
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (16, 76, 72), 2)
        m = cv2.moments(frame_mask, False)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2
        cv2.circle(frame2,(int(cx), int(cy)), 10,(0,0,255),-1)
        if  w+h==880:
            print('proximo estado')
        elif x+y+w+h!=0:
            if 256 < cx and 384 > cx:
                print('em frente')
                walk='frente'
                obj.publ1(walk)
            elif 128 < cx and 256 > cx:
                print('vire a esquerda')
                walk='esquerda'
                obj.publ1(walk)
            elif 384 < cx and 512 > cx:
                print('vire a direita')
                walk='direita'
                obj.publ1(walk)
            elif  128 > cx:
                print('vira muito e')
                walk='muito esquerda'
                obj.publ1(walk)
            elif  512 < cx:
                walk='muito direita'
                obj.publ1(walk)
                print('vira muito d')
if __name__=='__main__':  
   rospy.init_node('andando_1', anonymous=True)
   obj= Baterpub()
   rospy.spin()

