#!/usr/bin/env python3
import sys
import logging
import serial
from utils import read_line, read_headers

DEFAULT_ADDR = '/tmp/serial_simulator'
logging.basicConfig(level=logging.INFO)

# "Ресурси" пристрою
RESOURCES = {
    '/': 'IoT device online',
    '/idn': 'Test-conn,24C,305682,1.05A',
    '/temp': '24C',
    '/current': '1.05A',
}


def build_response(status, body):
    body = body.encode()
    head = (f'HTTP/1.1 {status}\r\n'
            'Content-Type: text/plain; charset=utf-8\r\n'
            f'Content-Length: {len(body)}\r\n'
            'Connection: keep-alive\r\n'
            '\r\n').encode()
    return head + body


addr = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDR
conn = serial.serial_for_url(addr)
logging.info(f'HTTP-over-serial server ready on {addr}')



while True:
    request_line = read_line(conn)
    if not request_line:
        continue
    # читаємо заголовки до порожнього рядка
    headers = read_headers(conn)

    logging.info('REQ: %s | headers=%s', request_line, headers)

    parts = request_line.split()
    if len(parts) != 3:
        response = build_response('400 Bad Request', 'Bad Request')
    elif parts[0] != 'GET':
        response = build_response('405 Method Not Allowed', 'Only GET is supported')
    elif parts[1] in RESOURCES:
        response = build_response('200 OK', RESOURCES[parts[1]])
    else:
        response = build_response('404 Not Found', 'Not Found')
    logging.info('RESP: %r', response)
    conn.write(response)
