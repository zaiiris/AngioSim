# Serial Bridge

The Arduino Uno does not know which web training session is active. The bridge solves this by reading JSON lines from USB Serial, adding the active `session_id`, and posting the payload to the backend.

Install dependency:

```powershell
backend\.venv\Scripts\python.exe -m pip install -r hardware\bridge\requirements.txt
```

Run after creating a session in AngioSim:

```powershell
backend\.venv\Scripts\python.exe hardware\bridge\serial_to_backend.py --port COM3 --session-id 1
```

Use the COM port shown by Arduino IDE. The backend must be running at `http://127.0.0.1:8000`, or pass another URL:

```powershell
backend\.venv\Scripts\python.exe hardware\bridge\serial_to_backend.py --port COM3 --session-id 1 --api-url http://127.0.0.1:8000
```

The bridge expects one JSON object per line:

```json
{"device_id":"heart-pulse-v1","events":[{"sensor_name":"pulse_count","value":840,"unit":"pulses"}]}
```

It sends this to:

```text
POST /api/hardware/events
```
