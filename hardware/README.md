# Hardware

This folder contains Arduino trainer code and device notes.

Current hardware source files:

- `arduino/heart_pulse_flprog_generated.ino` - generated Arduino C++ sketch from FLProg.
- `bridge/serial_to_backend.py` - desktop bridge from Arduino USB Serial to the backend API.
- `flprog/heart_pulse.flp` - original FLProg project file for the heart/pulse circulation controller.
- `protocol.md` - current sensor/control interpretation and planned API bridge format.

Current device logic:

- counts flow/circulation pulses on digital pin `D2`;
- shows volume, target volume, menu, and cycle count on a 16x2 I2C LCD at address `0x27`;
- uses EEPROM to store target milliliters/liters and continuous mode;
- controls outputs on `D13` and `D9`;
- sends telemetry over USB Serial as JSON once per second.

Backend integration target:

```text
POST /api/hardware/events
```

The first integration sends `pulse_count`, `volume`, `target_volume`, and `circulation` values. Pressure and leak sensors can be added later without changing the endpoint shape.
