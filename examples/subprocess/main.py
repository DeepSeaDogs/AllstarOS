# main.py
import subprocess
import signal
import sys
import threading
import time

# Global to hold the subprocess so we can terminate it
heartbeat_process = None
time_process = None

last_hb = -1
last_dtstamp = -1

def run_heartbeat():
    global heartbeat_process, last_hb 
    heartbeat_process = subprocess.Popen(
        ['python3', '-u', 'heartbeat_sub.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in heartbeat_process.stdout:
        print(f"[Heartbeat] {line.strip()}")
        last_hb = line.strip()

def run_time():
    global time_process, last_dtstamp 
    time_process = subprocess.Popen(
        ['python3', '-u', 'time_sub.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in time_process.stdout:
        print(f"[Time] {line.strip()}")
        last_dtstamp  = line.strip()

def handle_sigint(sig, frame):
    print("\n[Main]SIGINT received")
    print("[Main]Terminating heartbeat...")
    if heartbeat_process:
        heartbeat_process.terminate()
        heartbeat_process.wait()
    print("[Main]Terminating time...")
    if time_process:
        time_process.terminate()
        time_process.wait()
    sys.exit(0)

# Set up SIGINT (Ctrl+C) handler
signal.signal(signal.SIGINT, handle_sigint)

# Start the heartbeat in a thread
heartbeat_thread = threading.Thread(target=run_heartbeat)
heartbeat_thread.start()

# Start the heartbeat in a thread
time_thread = threading.Thread(target=run_time)
time_thread.start()


# Wait for the thread to finish (will happen after SIGINT)
heartbeat_thread.join()
time_thread.join()

# while True:
#     time.sleep(3)
#     print(f"Time: {last_dtstamp }\nHeartbeat: {last_hb}")

