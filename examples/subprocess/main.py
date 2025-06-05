# main.py
import subprocess
import signal
import sys
import time

process = subprocess.Popen(
    ['python3', '-u','./heartbeat_sub.py'],  # Command to run. '-u' runs python 'unbuffered'
    stdout=subprocess.PIPE,           # Captures the standard output (so you can read process.stdout in your script)
    stderr=subprocess.STDOUT,         # Combine stderr into stdout
    # stderr=subprocess.PIPE,         # Captures the standard error in a similar way to stdout.
                                        # Useful if you want to read or log error messages from the subprocess.
    text=True                         # Tells Python to treat input/output as text (str) instead of bytes
)

# Respond to CTRL-C
def handle_interrupt(sig, frame):
    print("\nCtrl+C detected. Terminating subs...")
    process.terminate()
    time.sleep(3)
    # try:
    #     process.wait(timeout=5)
    # except subprocess.TimeoutExpired:
    #     print("Heartbeat did not exit in time. Killing it.")
    #     process.kill()
    sys.exit(0)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, handle_interrupt)

# Read subprocess output line-by-line
try:
    for line in process.stdout:
        print(f"[Subprocess] {line.strip()}")
except Exception as e:
    print(f"Error: {e}")
    handle_interrupt(None, None)

