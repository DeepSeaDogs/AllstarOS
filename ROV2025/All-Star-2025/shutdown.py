import subprocess
import time
try:
    thruster_pid = subprocess.check_output(["cat", "/home/pi/rov_project/thruster_pid.txt"]).decode().strip()
    print("killing PID: ", thruster_pid + "\n")
    #subprocess.run(["kill", str(int(thruster_pid ))]) 
    subprocess.run(["fuser", "-k", "8487/tcp"])
except Exception as e:
    print("failed to kill process: ", e)
#subprocess.run("rm", "/home/pi/rov_project/thruster_pid.txt")

try:
    subprocess.run(["pkill", "-f",  "camera_stream.py"])
    subprocess.run(["pkill", "-f", " camera_stream2.py"])
    subprocess.run(["fuser", "-k", "8485/tcp"])
    subprocess.run(["fuser", "-k", "8489/tcp"])
    subprocess.run(["fuser", "-k", "8487/tcp"])
except Exception as e:
    print("Couldn't close camera stream: ", e)

result = subprocess.run(["lsof", "-i", ":8487"], capture_output=True)
print("Port 8487 status:\n", result.stdout.decode())    
result1 = subprocess.run(["lsof", "-i", ":8485"], capture_output=True)
print("Port 8485 status:\n", result1.stdout.decode())
result2 = subprocess.run(["lsof", "-i", ":8489"], capture_output=True)
print("Port 8489 status:\n", result2.stdout.decode())

