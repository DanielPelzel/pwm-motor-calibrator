# PWM Motor Calibrator

PyQt5 GUI tool to find the deadzone and calibrate the usable PWM range of DC motors, connected via serial to an ESP32.

## What it does

- Sweeps PWM values on a connected motor via ESP32
- Detects the deadzone (minimum PWM before the motor actually starts moving)
- Helps determine a usable min/max PWM range for reliable motor control
- Talks to the ESP32 over serial from a desktop GUI

## Structure

```
GUI/    → PyQt5 desktop application
src/    → ESP32 firmware (C/C++)
```

## Requirements

- Python 3.x
- ESP32 flashed with the firmware from `src/`
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Flash `src/` onto your ESP32
2. Wire up the motor driver + motor to the ESP32 (see [pinout/wiring — TODO])
3. Connect the ESP32 via USB
4. Run the GUI:
5. Start calibration 

## Why

Built to quickly characterize unknown/new DC motors before integrating them into a larger project — instead of guessing PWM thresholds by trial and error.

## Hardware assumed

- **Motor driver:** DRV8833 (dual H-bridge)
- **Microcontroller:** ESP32
- Tested with small DC motors (e.g. N20, 6V)
