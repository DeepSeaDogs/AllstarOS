# Time
# Sends date/time out. This can function like a time server on the Pi, as it
#sends time to the PC. Useful for things like time stamping logs on both systems
import time
from datetime import datetime
import signal
import sys

proc_name = "Time_Sub"

def handle_sigterm(signum, frame):
    print(F"{proc_name} received SIGTERM (sig: {signum}), shutting down...", flush=True)
    sys.exit(0)

# Register SIGTERM handler
signal.signal(signal.SIGTERM, handle_sigterm)

try:
    while True:
        # flush=True to ensure that output is immediately written to stdout (important for real-time subprocess communication)
        print(datetime.now().isoformat(), flush=True)
        time.sleep(1)
except KeyboardInterrupt:
    #Handles Ctrl+C gracefully with a KeyboardInterrupt
    print(F"{proc_name} terminated", flush=True)
