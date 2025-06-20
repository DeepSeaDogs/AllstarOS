import subprocess
import pygame, pygame_gui
from camera_client import CameraClient
import math
import time
import sys
import signal
import socket
import json

#Connect to the pi's processes
try:
    pi_boot = subprocess.Popen(["ssh", "pi@192.168.1.50", "python3 ~/rov_project/startup.py"])
except Exception as e:
    print("Error booting: ", e)

#Get camera feed
try:
    camera1 = CameraClient(camera_number=0) #for /dev/video0
except ConnectionRefusedError as e:
    print("Camera 0 not avaiable: ", e)
#try:
#    camera2 = CameraClient(camera_number= 4) #for /dev/video4, uses port 8489
#except ConnectionRefusedError as e:
#    print("camera 4 not available: ", e)


#Connect to thrusters
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for _ in range(10):  # Try up to 10 times
    try:
        client_socket.connect(('192.168.1.50', 8487))
        print("Connected to thruster control!")
        break
    except Exception as e:
        print("Retrying thruster socket...", e)
        time.sleep(1)
else:
    print("Failed to connect to thruster control after 10 tries.")  

#termine() will close ssh, cameras, and pygame
def terminate():
    pygame.quit()
    #Close camera feeds
    print("Closing camera feeds...")
    camera1.close()
    #camera2.close()
    client_socket.close()
    
    #close 
    print("Running shutdown script on Pi...")
    subprocess.run([
        "ssh", "pi@192.168.1.50", "python3 ~/rov_project/shutdown.py"], timeout=5)
    print("Killing background SSH subprocesses...")
    pi_boot.kill()
    time.sleep(1.5)
    print("Exiting")
    sys.exit(0)

#signal_handle() will run ctrl + C is pressed
def signal_handle(sig, frame):
    terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handle) #Define signal for exit

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

rect_x = pygame.Rect((Width // 6 - label_width // 2, label_y - label_height), (label_width, label_height))
rect_y = pygame.Rect((Width // 2 - label_width // 2, label_y-label_height), (label_width, label_height)) #vertical tilt
rect_z = pygame.Rect((5 * Width //6  - label_width // 2, label_y-label_height), (label_width, label_height)) #pwlv = power level
rect_turn = pygame.Rect((Width // 6 - label_width // 2, label_y), (label_width, label_height))
rect_vt = pygame.Rect((Width // 2 - label_width // 2, label_y), (label_width, label_height))
rect_pwlv = pygame.Rect((5 * Width // 6 - label_width // 2, label_y), (label_width, label_height)) 

UIManager = pygame_gui.UIManager((Width,Height),  "theme.json")
x_label = pygame_gui.elements.UILabel(rect_x, f"x-axis: {0:.0f}%", UIManager)
y_label = pygame_gui.elements.UILabel(rect_y, f"y-axis: {0:.0f}%", UIManager)
turn_label = pygame_gui.elements.UILabel(rect_turn, f"turn: {0:.0f}%", UIManager)
z_label = pygame_gui.elements.UILabel(rect_z, f"z-axis: {0:.0f}%", UIManager)
vt_label = pygame_gui.elements.UILabel(rect_vt, f"z-tilt: {0:.0f}%", UIManager)
pwlv_label = pygame_gui.elements.UILabel(rect_pwlv, f"power level: {3}",UIManager)

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
turn_input = 0
z_input = 0
vertical_tilt_input = 0
deadzone = 0.2
power_level = 3 #Can be adjusted to make controls more/less sensitive (higher power level = stronger pulse)
claw_state = 0 #start with claw closed


#Main loop
try:
    print("Starting program!")
    running = True
    while running:
        time_delta = clock.tick(60) / 1000 #60 fps


        #Process events (for buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN: #Detect button press
                #power level control
                if event.button == 4: #If left bumper pressed
                    power_level -= 1
                    min_power = 1
                    if power_level < min_power:
                        power_level = min_power
                    pwlv_label.set_text(f"Power Level: {power_level}")
                if event.button == 5: #If right bumper pressed
                    power_level += 1
                    max_power = 4
                    if power_level > max_power:
                        power_level = max_power
                    pwlv_label.set_text(f"power Level: {power_level}")
            UIManager.process_events(event)

        #get joystick/trigger inputs
        if joystick is not None:
            x=joystick.get_axis(0)#left joystick -1 is left,  +1 is right 
            y= joystick.get_axis(1) #left joystick -1 is forward, +1 is backward
            turn=joystick.get_axis(2) #right joystick x-axis, used for tilt horizontal
            z=joystick.get_axis(3) #right joystick y-axis, used for vertical
            td=joystick.get_axis(4) #left trigger, tilt down
            tu=joystick.get_axis(5) #right trigger, tilt up
            #Because trigger unpressed = -1 and trigger pressed = 1, we need to map it to  be like the joystick controls
            td = (td + 1) /2 #maps -1 > 0, 0 > 0.5, 1 > 1
            tu = (tu + 1) /2
            vertical_tilt = tu - td #get total tilt for display

            claw_state = 0
            if joystick.get_button(1):  # A button → open
                claw_state = 1
            elif joystick.get_button(0):  # B button → close
                claw_state = -1

            #define a dead zone
            if abs(y)<deadzone: 
                y=0
            if abs(x)<deadzone: 
                x=0
            if abs(turn)<deadzone:
                turn=0
            if abs(z)<deadzone:
                z=0
            if abs(tu)<deadzone:
                tu=0
            if abs(td)<deadzone:
                td=0

            #display joystick changes
            if x != x_input: #if x changes
                x_label.set_text(f"x-axis: {x*100:.0f}%") #update gui
                x_input = x #update x_input
            if y != y_input: #if y changes
                y_label.set_text(f"y-axis: {-y*100:.0f}%") #update gui
                y_input = y #update y_input
            if turn != turn_input: #if turn changes
                turn_label.set_text(f"turn: {turn*100:.0f}%") #update gui
                turn_input = turn#update turn_input
            if z != z_input: #if z changes
                z_label.set_text(f"z-axis: {-z*100:.0f}%") # update gui
                z_input = z #update z_input
            if vertical_tilt != vertical_tilt_input: #if vertical ltilt increases
                vt_label.set_text(f"z-tilt: {vertical_tilt*100:.0f}%") #update gui
                vertical_tilt_input = vertical_tilt #update vertical_tilt_input

            #Send data to pi
            data = {
                "x": round(x, 3),
                "y": round(-y, 3),
                "turn": round(turn, 3),
                "z": round(-z, 3),
                "powerlv": power_level,
                "td": round(td, 3),
                "tu": round(tu, 3),
                "claw_state": claw_state,
                }
            try:
                client_socket.sendall(json.dumps(data).encode('utf-8'))
            except Exception as e:
                print("Couldn't send joystick data:", e)

        #Redraw screen
        screen.fill((0,0,0))#Fill screen (background)
    
    #Get camera frames
        padding = 55
        available_width = Width - (2 * padding)
        feed_width = available_width 
        feed_height = label_y - label_height *2

        # Left camera
        frame_surface1 = camera1.get_surface() if camera1 else print("Warming: camera 0 missing")
        if frame_surface1:
            frame_surface1 = pygame.transform.scale(frame_surface1, (feed_width, feed_height))
            screen.blit(frame_surface1, (padding, padding))

        # Right camera
        #frame_surface2 = camera2.get_surface() if camera2 else print("Warning: camera 1 missing")
        #if frame_surface2:
        #    frame_surface2 = pygame.transform.scale(frame_surface2, (feed_width, feed_height))
        #    screen.blit(frame_surface2, (padding * 2 + feed_width, padding))

        UIManager.update(time_delta)
        UIManager.draw_ui(screen)

        pygame.display.flip()

        #clock.tick(30)    
        pygame.display.update()
except Exception as e:
    print("Error: ", e)
finally:
    terminate()

