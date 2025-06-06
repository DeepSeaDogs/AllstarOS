import subprocess
import pygame, pygame_gui
from camera_client import CameraClient
import math
import time
import sys
import signal

#Connect to the pi's camera stream
#subprocess.run(["ssh", "pi@192.168.1.50", "pkill -f camera_stream.py || true"])
#pi_proc = subprocess.run(["ssh", "pi@192.168.1.50", "python3 ~/rov_project/camera_stream.py"])
#pid = pi_proc.stdout
#print(str(pid))

#Get camera feed
camera = CameraClient()

#termine() will close ssh and camera
def terminate():
    print("Terminating subprocesses...")
    #kill_pi_proc = subprocess.run(["ssh", "pi@192.168.1.50", f"kill {pid}"])
    #if kill_pi_proc.returncode == 0:
    #    print(f"successuflly terminaed {pid}")
    #else:
    #print(f"Error terminating {pid}")
    #pi_proc.terminate() for Popen
    print("closing...")
    camera.close() 
    pygame.quit()
    None

#signal_handle() will run if the window closes or ctrl + C is pressed
def signal_handle(sig, frame):
    terminate()
    sys.exit(0)

deadzone = 0.2
signal.signal(signal.SIGINT, signal_handle) #

#Setup window
pygame.init()
Width, Height = 1200, 800 #resolution
screen = pygame.display.set_mode((Width, Height)) 
pygame.display.set_caption("All-Star Window")
clock = pygame.time.Clock()

#Setup labels

label_width = 200
label_height = 100
label_y = Height - label_height  # align bottom
rect_x = pygame.Rect((Width // 6 - label_width // 2, label_y), (label_width, label_height))
rect_y = pygame.Rect((Width // 2 - label_width // 2, label_y), (label_width, label_height))
rect_z = pygame.Rect((5 * Width // 6 - label_width // 2, label_y), (label_width, label_height))
UIManager = pygame_gui.UIManager((Width,Height),  "theme.json")
x_label = pygame_gui.elements.UILabel(rect_x, f"x axis: {0:.2f}", UIManager)
y_label = pygame_gui.elements.UILabel(rect_y, f"y axis: {0:.2f}", UIManager)
z_label = pygame_gui.elements.UILabel(rect_z, f"z axis: {0:.2f}", UIManager)


#init joystick
joystick = None
if pygame.joystick.get_count() == 0:
    print('No Joystick connected')
else:
    pygame.joystick.init() #initalize joystick
    joystick = pygame.joystick.Joystick(0)
    print("Joystick connected! ")
#setup for jyoystick display
x_input = 0
y_input = 0
z_input = 0

#Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000 #60 fps

    #Process events (for buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        UIManager.process_events(event)

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

        time.sleep(.1) #wait .1 seconds
        if x != x_input: #if x changes
            print("x-axis: " + str(x)) # print to terminal
            x_label.set_text(f"x-axis: {x:.2f}") #update gui
            x_input = x #update x_input
        if y != y_input: #if y changes
            print("y-axis: " + str(y)) #print to terminal 
            y_label.set_text(f"y-axis: {y:.2f}") #update gui
            y_input = y #update y_input
        if z != z_input: #if z changes
            print("z-axis: " + str(z)) #print to terminal
            z_label.set_text(f"z-axis: {z:.2f}") #update gui
            z_input = z#update z_input

    #Redraw screen
    screen.fill((0,0,0))#Fill screen (background)
   
   #Get camera frames
    frame_surface = camera.get_surface()
    if frame_surface:
        frame_surface = pygame.transform.scale(frame_surface, (Width - 100, label_y))
        screen.blit(frame_surface,(50,0)) #Draw camera frame
    
    UIManager.update(time_delta)
    UIManager.draw_ui(screen)
    pygame.display.flip()

    #clock.tick(30)    
    pygame.display.update()
    

terminate()