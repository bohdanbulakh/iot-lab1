#!/usr/bin/env python3
import sys
import serial

DEFAULT_ADDR = '/tmp/serial_conn'
DEFAULT_CMD = '*IDN?'

args = len(sys.argv) - 1

if args == 0:
    addr, cmd = DEFAULT_ADDR, DEFAULT_CMD
elif args == 1:
    addr, cmd = DEFAULT_ADDR, sys.argv[1]
else:
    addr, cmd = sys.argv[1:3]

cmd += '\n'
s = serial.serial_for_url(addr)
s.write(cmd.encode())

print(s.readline())
