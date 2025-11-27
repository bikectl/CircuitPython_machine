# SPDX-FileCopyrightText: Copyright (c) 2025 Bjoern Bilger
#
# SPDX-License-Identifier: MIT

import board
import busio

from machine import I2C as MP_I2C

cp_i2c: busio.I2C = board.STEMMA_I2C()  # type: ignore[attr-defined]
mp_i2c: MP_I2C = MP_I2C(cp_i2c=cp_i2c)
print("I2C addresses found:", [hex(address) for address in mp_i2c.scan()])
