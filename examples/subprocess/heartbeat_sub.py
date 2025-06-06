# Heartbeat
# Sends an ever incrementing value out
# Value will reset to 0 after reaching 2^32
import time
from datetime import datetime
import signal
import sys

proc_name = "Heartbeat_Sub"

tick = 0

def handle_sigterm(signum, frame):
    print(F"{proc_name} received SIGTERM (sig: {signum}), shutting down...", flush=True)
    sys.exit(0)

# Register SIGTERM handler
signal.signal(signal.SIGTERM, handle_sigterm)

try:
    while True:
        # flush=True to ensure that output is immediately written to stdout (important for real-time subprocess communication)
        print(tick, flush=True)
        time.sleep(1)
        tick = (tick + 1) % (2**32) # Reset to 0 when number reaches 2^32 (4_294_967_296)
except KeyboardInterrupt:
    #Handles Ctrl+C gracefully with a KeyboardInterrupt
    print(F"{proc_name} terminated", flush=True)
