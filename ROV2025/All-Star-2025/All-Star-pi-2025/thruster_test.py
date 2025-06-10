import board, busio, time
from adafruit_pca9685 import PCA9685

def pulse_us_to_duty(pulse_us):
    return int((pulse_us / 20000.0) * 65535)

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

ch = pca.channels[1]  # try channel 1

# Arming
print("Sending 1550 us...")
ch.duty_cycle = pulse_us_to_duty(1550)
time.sleep(3)

print("Sweeping forward throttle...")
for us in range(1550, 1650, 10):
    print(f"{us} µs")
    ch.duty_cycle = pulse_us_to_duty(us)
    time.sleep(2)

print("Sweeping backward throttle...")
for us in range(1650, 1450, -10):
    print(f"{us} µs")
    ch.duty_cycle = pulse_us_to_duty(us)
    time.sleep(2)
ch.duty_cycle = pulse_us_to_duty(1550)

