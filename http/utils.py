def read_line(connection):
    return connection.readline().decode(errors='replace').strip()

def read_headers(connection):
    headers = {}

    while (line := read_line(connection)) != '':
        key, _, value = line.partition(':')
        headers[key.strip().lower()] = value.strip()

    return headers