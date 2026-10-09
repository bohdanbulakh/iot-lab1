#!/usr/bin/env python3
# Передача файлу через serial з CRC32 (порт /tmp/serial_conn)
# Використання: python file_sender.py <файл> [порт]
import os
import sys
import zlib
import serial

DEFAULT_ADDR = '/tmp/serial_conn'

if len(sys.argv) < 2:
    sys.exit('Використання: python file_sender.py <файл> [порт]')
path = sys.argv[1]
addr = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ADDR

with open(path, 'rb') as f:
    data = f.read()
crc = zlib.crc32(data)
name = os.path.basename(path).replace(' ', '_')

s = serial.serial_for_url(addr, timeout=10)
s.write(f'FILE {name} {len(data)} {crc:08x}\n'.encode())
s.write(data)
s.flush()

reply = s.readline().decode().strip()
print(f'Sent {len(data)} bytes, CRC32={crc:08x}, reply: {reply or "timeout"}')
