import socket
import pygame, pygame_gui
import math
import time
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.50', 8487))

#init joystick
pygame.init()
joystick = None
if pygame.joystick.get_count() == 0:
    print('No Joystick connected')
else:
    pygame.joystick.init() #initalize joystick
    joystick = pygame.joystick.Joystick(0)
    print("Joystick connected! ")

#setup for joystick display
x_input = 0
y_input = 0
z_input = 0
deadzone = 0.2

#Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #get joystick inputs
    if joystick is not None:
        x=joystick.get_axis(0)#left joystick -1 is left to +1 is right (left thruster)
        y=joystick.get_axis(1) #left joystick -1 is up +1 is down (right thruster)
        z=joystick.get_axis(2) #right joystick x-axis, used for vertical
        

        if abs(y)<deadzone: #define a dead zone
            y=0
        if abs(x)<deadzone: #define a dead zone
            x=0
        if abs(z)<deadzone: #define a dead zone
            z=0

        #Send/print joystick inputs
        time.sleep(.1) #wait .1 seconds
        if x != x_input: #if x changes
            print("x-axis: " + str(x)) # print to terminal
            x_input = x #update x_input
        if y != y_input: #if y changes
            print("y-axis: " + str(y)) #print to terminal
            y_input = y #update y_input
        if z != z_input: #if z changes
            print("z-axis: " + str(z)) #print to terminal
            z_input = z#update z_input
       
        data = {
            "x": round(x, 3),
            "y": round(y, 3),
            "z": round(z, 3)}
        try:
            client_socket.sendall(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print("Couldn't send joystick data", e)
        
