import subprocess
import sys
import socket
import subprocess
import time

print("Checking for open ports...")
try:
    # Find process using port 8487
    result = subprocess.check_output(["lsof", "-i", ":8487", "-t"]).decode().strip()
    if result:
        print("Found PID using port 8487:", result)
        #subprocess.run(["kill", result])
    else:
        print("No process found using port 8487.")
except Exception as e:
    print("Error killing port 8487 process:", e)

try:
    subprocess.run(["fuser", "-k", "8485/tcp"])
    subprocess.run(["fuser", "-k", "8489/tcp"])
    #subprocess.run(["fuser", "-k", "8487/tcp"])
except Exception as e:
    print("Couldn't close ports or no ports to close: ", e)

# Launch camera stream 0
subprocess.Popen(["python3", "/home/pi/rov_project/camera_stream.py"])
print("Camera Stream 1 Initialized")
time.sleep(1)
# Launch camera stream 2
subprocess.Popen(["python3", "/home/pi/rov_project/camera_stream2.py"])
print("Camera Stream 2 Initialized")

#launch thruster control
subprocess.Popen(
    "python3 /home/pi/rov_project/thruster_control.py > /home/pi/rov_project/thruster.log 2>&1 &",
    shell=True
)


#Print initialized
print("Subprocesses Initialized!")
