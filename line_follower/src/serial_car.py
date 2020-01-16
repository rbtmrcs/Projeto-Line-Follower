#!/usr/bin/env python

import serial
import time
import Tkinter as tk
'''
window = tk.Tk()
window.configure(background="gray")
window.geometry("750x300")
window.title("CAR CTRL - PYTHON GUI")
'''
#board = serial.Serial('/dev/ttyUSB1', 9600)
#board = serial.Serial('/dev/ttyACM0', 115200)

class Board:
    def write(self):
        print ('qualquer coisa')
        
class Car_control:

    def __init__(self):
        self.board =  Board()##serial.Serial('/dev/ttyUSB1', 9600)
        print("########### CAR CTRL PROGRAM ###########\n")

    def pra_frente(self):
        print("########### FRENTE ###########\n")
        self.board.write(bytearray('1'))

    def esquerda_light(self):
        print("########### ESQUERDA LIGHT ###########\n")
        self.board.write(bytearray('2'))

    def esquerda_hard(self):
        print("########### ESQUERDA HARD ###########\n")
        self.board.write(bytearray('3'))

    def direita_light(self):
        print("########### DIREITA LIGHT ###########\n")
        self.board.write(bytearray('4'))

    def direita_hard(self):
        print("########### DIREITA HARD ###########\n")
        self.board.write(bytearray('5'))

    def parar(self):
        print("########### PARAR ###########\n")
        self.board.write(bytearray('7'))
    
'''
    b1 = tk.Button(window, text="FRENTE", command=pra_frente, bg='gray80', fg='gray7', font=("Times", 15))
    b2 = tk.Button(window, text="LEFT_LIGHT", command=esquerda_light, bg='gray80', fg='gray7', font=("Times", 15))
    b3 = tk.Button(window, text="LEFT_HARD", command=esquerda_hard, bg='gray80', fg='gray7', font=("Times", 15))
    b4 = tk.Button(window, text="RIGHT_LIGHT", command=direita_light, bg='gray80', fg='gray7', font=("Times", 15))
    b5 = tk.Button(window, text="RIGHT_HARD", command=direita_hard, bg='gray80', fg='gray7', font=("Times", 15))
    b6 = tk.Button(window, text="TRAS", command=parar, bg='gray80', fg='gray7', font=("Times", 15))
    
    b1.grid(row=1, column=2, padx=5, pady=10)
    b2.grid(row=2, column=1, padx=5, pady=10)
    b3.grid(row=3, column=0, padx=5, pady=10)
    b4.grid(row=2, column=3, padx=5, pady=10)
    b5.grid(row=3, column=4, padx=5, pady=10)
    b6.grid(row=4, column=2, padx=5, pady=10)

    window.mainloop()

time.sleep(2)
car_control()
'''