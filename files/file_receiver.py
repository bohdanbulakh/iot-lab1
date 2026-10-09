#!/usr/bin/env python3
# Прийом файлів через serial з перевіркою CRC32 (порт /tmp/serial_simulator)
import os
import sys
import zlib
import logging
import serial

DEFAULT_ADDR = '/tmp/serial_simulator'
OUT_DIR = 'received'
logging.basicConfig(level=logging.INFO)

addr = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDR

conn = serial.serial_for_url(addr)

os.makedirs(OUT_DIR, exist_ok=True)

logging.info(f'File receiver ready on {addr}')

while True:
    header = conn.readline().decode(errors='replace').strip()
    if not header:
        continue
    try:
        tag, name, size, expectedCrc = header.split()
        assert tag == 'FILE'
        size, expectedCrc = int(size), int(expectedCrc, 16)
    except (ValueError, AssertionError):
        logging.warning('Bad header: %r', header)
        conn.write(b'ERR header\n')
        continue

    data = conn.read(size)
    actualCrc = zlib.crc32(data)

    if len(data) == size and actualCrc == expectedCrc:
        path = os.path.join(OUT_DIR, os.path.basename(name))
        with open(path, 'wb') as f:
            f.write(data)
        logging.info('OK: %s, %d bytes, CRC32=%08x', path, size, actualCrc)
        conn.write(b'OK\n')
    else:
        logging.error('FAIL: %s got %d/%d bytes, CRC32 %08x != %08x',
                      name, len(data), size, actualCrc, expectedCrc)
        conn.write(b'ERR crc\n')
