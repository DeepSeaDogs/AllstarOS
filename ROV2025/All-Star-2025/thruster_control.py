import board
import busio
from adafruit_pca9685 import PCA9685
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
from time import sleep
import socket
import json
from threading import Thread
import traceback

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8487))  # Listen on all interfaces, port 8487
server_socket.listen(1)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected to: {addr}")
#setup for thruster control
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # For ESC/servo PWM
#setup for claw control
in1 = DigitalOutputDevice(23)
in2 = DigitalOutputDevice(24)
ena = PWMOutputDevice(18)

# Send ~1500µs (neutral position)
def pulse_us_to_duty(pulse_us):
    return int((pulse_us / 20000) * 65535)

#Setup for input mapping
global power_level
power_level = 3 #Can be adjusted to make controls more/less (higher power level = stronger pulse)
base = 1550 #Neutral
max_delta = 400 # Full range(±400µs)

def apply_thrust(x, y, turn, z, td, tu, claw_state):
    #six thruster setup
    global thruster_map
    thruster_map = [base] * 6
    global limiter
    #limiter = abs(11 - (power_level * 2))
    limiter = 5 - power_level
    move_forward_backward(y) #y
    move_left_right(x) #x
    turn_horizontal(turn) #turn
    move_vertical(z) #z
    tilt_up(tu) #tu
    tilt_down(td) #td
    claw_movement(claw_state)
    for i in range(6):
       pulse = thruster_map[i]
       pca.channels[i].duty_cycle = pulse_us_to_duty(pulse)

     #Two thruster setup (For testing)
     #pulse_x = base + int((x/limiter)*max_delta) #convert input to pulse for x
     #pulse_y = base + int((y/limiter)*max_delta) #convert input to pulse for x
     #print(f"Setting PWM t0: {pulse_x}")
     #print(f"Setting PWM t0: {pulse_y}")
     #pca.channels[1].duty_cycle = pulse_us_to_duty(pulse_x)
     #pca.channels[0].duty_cycle = pulse_us_to_duty(pulse_y)

def move_forward_backward(y):
     pulse_y = int((y/limiter)*max_delta) #convert input to pulse
     thruster_map[0] += pulse_y #thruster 1 
     thruster_map[1] += -pulse_y  #thruster 2
     thruster_map[4] += pulse_y #thruster 5
     thruster_map[5] += -pulse_y #thruster 6

def move_left_right(x):
     pulse_x = int((x/limiter)*max_delta)
     thruster_map[0] += pulse_x
     thruster_map[1] += pulse_x
     thruster_map[4] += -pulse_x
     thruster_map[5] += -pulse_x

def turn_horizontal(turn):
     pulse_turn = int((turn/limiter)*max_delta)
     thruster_map[0] += pulse_turn
     thruster_map[1] += pulse_turn
     thruster_map[4] += pulse_turn
     thruster_map[5] += pulse_turn

def move_vertical(z):
     pulse_vertical = int((z/limiter)*max_delta)
     thruster_map[2] +=  -pulse_vertical #thruster 3
     thruster_map[3] +=  pulse_vertical #thruster 4

def tilt_down(td):
     pulse_td = int((td/limiter)*max_delta)
     thruster_map[0] += pulse_td
     thruster_map[1] += -pulse_td
     thruster_map[4] += -pulse_td
     thruster_map[5] += pulse_td 

def tilt_up(tu):
     pulse_tu = int((tu/limiter)*max_delta)
     thruster_map[0] += -pulse_tu
     thruster_map[1] += pulse_tu
     thruster_map[4] += pulse_tu
     thruster_map[5] += -pulse_tu 


def claw_movement(claw_state):

    if claw_state == 1:  # open
        in1.on()
        in2.off()
        ena.value = 0.7
    elif claw_state == -1:  # close
        in1.off()
        in2.on()
        ena.value = 0.7
    else:  # neutral / no press
        ena.value = 0


def open_claw():
    in1.on()
    in2.off()
    ena.value = 0.7
def close_claw():
    in1.off()
    in2.on()
    ena.value = 0.7

print("Initializing Thruster...")
pca.channels[0].duty_cycle = pulse_us_to_duty(1550)

print("Starting control")
while True:
        try:
            data = conn.recv(1024)
            if not data:
                continue
            #decoded = json.loads(data.decode('utf-8'))
            decoded = json.loads(data.decode('utf-8').split('}')[0] + '}')
            x_input = decoded.get("x", 0)
            y_input = decoded.get("y", 0)
            turn_input = decoded.get("turn", 0)
            z_input = decoded.get("z", 0)
            tu_input = decoded.get("tu", 0)
            td_input = decoded.get("td", 0)
            power_level = decoded.get("powerlv", 0)
            claw_state = decoded.get("claw_state", 0)
            apply_thrust(x_input, y_input, turn_input, z_input, td_input, tu_input, claw_state)
        except Exception as e:
            print("Error receiving or applying thrust:", e)
            traceback.print_exc()
            break
conn.close()
    