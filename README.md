[![Build Status](https://github.com/bikectl/CircuitPython_machine/workflows/Build%20CI/badge.svg)](https://github.com/bikectl/CircuitPython_machine/actions)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Discord](https://img.shields.io/discord/327254708534116352.svg)](https://adafru.it/discord)

# Introduction

MicroPython machine module shim for CircuitPython.
It is by no means meant to be a complete implementation of the
MicroPython machine module, but rather to provide basic compatibility
for code written for MicroPython to run on CircuitPython with minimal
changes.

For now it only provides a shim for I2C.

Its primary purpose is to be able to use M5Stack I2C units (e.g. ByteSwitch) with CircuitPython.

The MicroPython drivers for the units can be found here: https://github.com/m5stack/uiflow-micropython/tree/master/m5stack/libs/unit

# Example

```python
import board
import busio
from machine import I2C as MP_I2C

cp_i2c: busio.I2C = board.STEMMA_I2C()
mp_i2c: MP_I2C = MP_I2C(cp_i2c=cp_i2c)

# byteswitch = ByteSwitchUnit(mp_i2c)
# joystick = Joystick2Unit(mp_i2c)
```

# Usage Notes

Please note that MicroPython code might require further changes.
For example `time.sleep_ms(x)` must be replaced by `time.sleep(x / 1000)`.
That is for example the case for `Joystick2Unit`.

# Dependencies

This driver depends on:

- [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
[the Adafruit library and driver bundle](https://circuitpython.org/libraries)
or individual libraries can be installed using
[circup](https://github.com/adafruit/circup).

# Installing to a Connected CircuitPython Device with Circup

Make sure that you have `circup` installed in your Python environment.
Install it with the following command if necessary:

```shell
pip3 install circup
```

With `circup` installed and your CircuitPython device connected use the
following command to install:

```shell
circup install machine
```

Or the following command to update an existing version:

```shell
circup update
```

# Contributing

Contributions are welcome! Please read our
[Code of Conduct](https://github.com/bikectl/CircuitPython_machine/blob/HEAD/CODE_OF_CONDUCT.md)
before contributing to help this project stay welcoming.
