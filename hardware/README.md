# Hardware

This folder contains Arduino trainer code and device notes.

Current hardware source files:

- `arduino/heart_pulse_flprog_generated.ino` - generated Arduino C++ sketch from FLProg.
- `flprog/heart_pulse.flp` - original FLProg project file for the heart/pulse circulation controller.
- `protocol.md` - current sensor/control interpretation and planned API bridge format.

Current device logic:

- counts flow/circulation pulses on digital pin `D2`;
- shows volume, target volume, menu, and cycle count on a 16x2 I2C LCD at address `0x27`;
- uses EEPROM to store target milliliters/liters and continuous mode;
- controls outputs on `D13` and `D9`;
- does not yet send data to the backend over Serial or Wi-Fi.

Backend integration target:

```text
POST /api/hardware/events
```

The first integration should send `flow`, `circulation`, and `volume` values. Pressure and leak sensors can be added later without changing the endpoint shape.
