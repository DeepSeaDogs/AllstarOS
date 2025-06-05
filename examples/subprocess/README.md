# Subprocess Example
This example uses ```Popen``` subprocess option. It runs each process in a Thread for control and proper shutdown

## Notes
```subprocess.run()``` is blocking
  - It runs the command and waits for it to finish before continuing.
  - It captures the output only after the subprocess exits (unless you use capture_output=True, which still doesn't stream in real-time).
  - It’s a convenience wrapper around Popen(...).wait().

```subprocess.Popen()``` is non-blocking
  - It starts the subprocess and returns immediately, allowing your main program to:
      - Stream output line-by-line
      - Monitor or send input
      - Terminate the subprocess when needed
  - Ideal when your subprocess runs for a long time or indefinitely (like a heartbeat script).