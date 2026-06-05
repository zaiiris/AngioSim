import argparse
import json
import time
import urllib.error
import urllib.request

import serial


def post_events(api_url, payload):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        api_url.rstrip("/") + "/api/hardware/events",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.status


def main():
    parser = argparse.ArgumentParser(
        description="Forward AngioSim Arduino Serial JSON to the backend."
    )
    parser.add_argument("--port", required=True, help="Arduino serial port, for example COM3.")
    parser.add_argument("--session-id", required=True, type=int, help="Active AngioSim session id.")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000", help="Backend URL.")
    parser.add_argument("--baud", default=115200, type=int, help="Serial baud rate.")
    args = parser.parse_args()

    print(f"Listening on {args.port} at {args.baud} baud")
    print(f"Forwarding to session {args.session_id} at {args.api_url}")

    with serial.Serial(args.port, args.baud, timeout=1) as arduino:
        time.sleep(2)
        while True:
            raw_line = arduino.readline().decode("utf-8", errors="replace").strip()
            if not raw_line:
                continue

            try:
                payload = json.loads(raw_line)
            except json.JSONDecodeError:
                print(f"skip non-json: {raw_line}")
                continue

            payload["session_id"] = args.session_id
            try:
                status = post_events(args.api_url, payload)
                print(f"posted {len(payload.get('events', []))} events: HTTP {status}")
            except urllib.error.URLError as exc:
                print(f"backend error: {exc}")


if __name__ == "__main__":
    main()
