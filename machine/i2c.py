# SPDX-FileCopyrightText: Copyright (c) 2025 Bjoern Bilger
#
# SPDX-License-Identifier: MIT

"""
MicroPython 'machine.I2C' shim for CircuitPython.

* Author(s): Bjoern Bilger
"""

import time

import busio

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Sequence

    from circuitpython_typing import ReadableBuffer, WriteableBuffer

__all__ = [
    "I2C",
]


class I2C:
    """
    MicroPython 'machine.I2C' shim for CircuitPython, using CircuitPython's 'busio.I2C'.

    Example usage:
        import board
        import busio
        from machine import I2C as MP_I2C

        cp_i2c = busio.I2C(board.SCL, board.SDA)
        mp_i2c = MP_I2C(cp_i2c=cp_i2c)

        devices = mp_i2c.scan()
        print("Found devices:", [hex(d) for d in devices])
    """

    def __init__(self, *, cp_i2c: busio.I2C) -> None:
        self.cp_i2c = cp_i2c

    def __enter__(self) -> "I2C":
        return self

    def __exit__(self, *args) -> None:
        self.deinit()

    def scan(self) -> list[int]:
        """Returns a list of 7-bit device addresses found on the I2C bus."""
        self._lock()
        try:
            return self.cp_i2c.scan()
        finally:
            self.cp_i2c.unlock()

    def writeto(self, addr: int, buf: ReadableBuffer, stop: bool = True) -> int:
        """Write the bytes in 'buf' to the device with address 'addr'."""
        # Note: CircuitPython does not support stop=False (Repeated Start)
        # for manual writeto calls. We accept the argument for compatibility
        # but must ignore it. The transaction will always end with a STOP.
        self._lock()
        try:
            self.cp_i2c.writeto(addr, buf)
            return len(buf)
        finally:
            self.cp_i2c.unlock()

    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
        """Read 'nbytes' from the device with address 'addr'."""
        # Note: CircuitPython does not support stop=False (Repeated Start)
        # for manual readfrom calls. We accept the argument for compatibility
        # but must ignore it. The transaction will always end with a STOP.
        result = bytearray(nbytes)
        self._lock()
        try:
            self.cp_i2c.readfrom_into(addr, result)
            return bytes(result)
        finally:
            self.cp_i2c.unlock()

    def readfrom_into(self, addr: int, buf: WriteableBuffer, stop: bool = True) -> None:
        """Read into 'buf' from the device with address 'addr'."""
        self._lock()
        try:
            self.cp_i2c.readfrom_into(addr, buf)
        finally:
            self.cp_i2c.unlock()

    def writevto(self, addr: int, vector: Sequence[ReadableBuffer], stop: bool = True) -> int:
        """Write the bytes contained in 'vector' to the device with address 'addr'."""
        # CircuitPython's busio.I2C does not support scatter-gather writes directly
        # or repeated starts between writes easily. We concatenate the vector.
        total_len = sum(len(b) for b in vector)
        full_buf = bytearray(total_len)
        offset = 0
        for b in vector:
            l = len(b)
            full_buf[offset : offset + l] = b
            offset += l

        return self.writeto(addr, full_buf, stop=stop)

    def readfrom_mem(
        self,
        addr: int,
        memaddr: int,
        nbytes: int,
        *,
        addrsize: int = 8,
    ) -> bytes:
        """Read 'nbytes' from 'memaddr' on device 'addr'."""
        memaddr_buf = I2C._get_memaddr_bytes(memaddr, addrsize)
        result = bytearray(nbytes)

        self._lock()
        try:
            # writeto_then_readfrom handles the Repeated Start correctly
            self.cp_i2c.writeto_then_readfrom(addr, memaddr_buf, result)
            return bytes(result)
        finally:
            self.cp_i2c.unlock()

    def readfrom_mem_into(
        self,
        addr: int,
        memaddr: int,
        buf: WriteableBuffer,
        *,
        addrsize: int = 8,
    ) -> None:
        """Read into 'buf' from 'memaddr' on device 'addr'."""
        memaddr_buf = I2C._get_memaddr_bytes(memaddr, addrsize)
        self._lock()
        try:
            self.cp_i2c.writeto_then_readfrom(addr, memaddr_buf, buf)
        finally:
            self.cp_i2c.unlock()

    def writeto_mem(
        self,
        addr: int,
        memaddr: int,
        buf: ReadableBuffer,
        *,
        addrsize: int = 8,
    ) -> None:
        """Write 'buf' to 'memaddr' on device 'addr'."""
        memaddr_buf = I2C._get_memaddr_bytes(memaddr, addrsize)

        # Ensure buf is bytes-like for concatenation
        if isinstance(buf, (bytes, bytearray)):
            full_buffer = memaddr_buf + buf
        else:
            full_buffer = memaddr_buf + bytes(buf)

        self._lock()
        try:
            self.cp_i2c.writeto(addr, full_buffer)
        finally:
            self.cp_i2c.unlock()

    def deinit(self) -> None:
        """Release the I2C bus."""
        self.cp_i2c.deinit()

    def _lock(self) -> None:
        """Wait for and acquire the I2C lock."""
        while not self.cp_i2c.try_lock():
            time.sleep(0.005)

    @staticmethod
    def _get_memaddr_bytes(memaddr: int, addrsize: int) -> bytes:
        if addrsize == 8:
            return bytes([memaddr & 0xFF])
        if addrsize == 16:
            return bytes([(memaddr >> 8) & 0xFF, memaddr & 0xFF])
        if addrsize == 32:
            return bytes(
                [
                    (memaddr >> 24) & 0xFF,
                    (memaddr >> 16) & 0xFF,
                    (memaddr >> 8) & 0xFF,
                    memaddr & 0xFF,
                ]
            )
        raise ValueError("addrsize must be 8, 16, or 32")
