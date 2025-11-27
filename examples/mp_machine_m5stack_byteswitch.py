# SPDX-FileCopyrightText: Copyright (c) 2025 Bjoern Bilger
#
# SPDX-License-Identifier: MIT

import time

import board
import busio

# place bytebutton.py into 'lib/m5stack/unit/'
# https://github.com/m5stack/uiflow-micropython/blob/master/m5stack/libs/unit/bytebutton.py
from m5stack.unit.bytebutton import ByteSwitchUnit  # pyright: ignore[reportMissingImports]

from machine import I2C as MP_I2C

cp_i2c: busio.I2C = board.STEMMA_I2C()  # type: ignore[attr-defined]
mp_i2c: MP_I2C = MP_I2C(cp_i2c=cp_i2c)

byteswitch = ByteSwitchUnit(mp_i2c)

byteswitch.set_led_show_mode(ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE)
for i in range(8):
    byteswitch.set_led_color(i, 0xFF0000)
while True:
    status = byteswitch.get_byte_switch_status()
    print(f"ByteSwitch status: {status}")
    time.sleep(1.0)
