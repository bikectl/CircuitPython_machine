# SPDX-FileCopyrightText: Copyright (c) 2025 Bjoern Bilger
#
# SPDX-License-Identifier: MIT
"""
`machine`
================================================================================

MicroPython 'machine' module shim for CircuitPython.

* Author(s): Bjoern Bilger
"""

from .i2c import I2C

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/bikectl/CircuitPython_machine.git"

__all__ = [
    "I2C",
]
