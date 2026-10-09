#!/usr/bin/env python3
import sys
import serial
from utils import read_line, read_headers

DEFAULT_ADDR = '/tmp/serial_conn'
path = sys.argv[1] if len(sys.argv) > 1 else '/idn'
addr = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ADDR

s = serial.serial_for_url(addr, timeout=5)
request = f'GET {path} HTTP/1.1\r\nHost: serial-device\r\n\r\n'
s.write(request.encode())

status = read_line(s)
if not status:
    sys.exit('Таймаут: відповіді немає (чи запущено http_server.py?)')

headers = read_headers(s)
body = s.read(int(headers.get('content-length', 0))).decode()

print('Status :', status)
print('Headers:', headers)
print('Body   :', body)
