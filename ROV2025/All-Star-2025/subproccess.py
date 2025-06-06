import subprocess
import time

# Start the Pi server via SSH
pi_command = ["ssh", "pi@192.168.1.50", "python3 ~/rov_project/camera_stream.py"]
pi_proc = subprocess.Popen(pi_command)

# Wait a bit to ensure the server starts
time.sleep(2)

# Start the client viewer
client_command = ["python3", "C:/Users/jacob/Desktop/ROV2025/All-Star-2025/camera_stream_client.py"]
subprocess.run(client_command)

# When client exits, kill server
pi_proc.terminate()
