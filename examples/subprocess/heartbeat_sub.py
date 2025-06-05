# Heartbeat
import time
from datetime import datetime
import signal
import sys

def handle_sigterm(signum, frame):
    print("Heartbeat received SIGTERM, shutting down...", flush=True)
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
    print("Heartbeat terminated", flush=True)
