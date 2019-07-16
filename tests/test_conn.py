#!/usr/bin/env python3

import asyncio
import json
import sys


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('192.168.1.4', 6666)
    message = f'{message}\n'
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()
    # await asyncio.sleep(1)
    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

if len(sys.argv) < 2:
    sys.exit(1)
# msg = {'cmd': 'write', 'sid': '158d00027d0065', 'model': 'plug', 'data': {'toogle': ''}}
# asyncio.run(tcp_echo_client(json.dumps(msg)))
#
# if len(sys.argv) < 3:
#     sys.exit(2)
# msg = {'cmd': 'write', 'sid': '0x0000000007e7bae0', 'data': {'set_power': sys.argv[2]}}
# asyncio.run(tcp_echo_client(json.dumps(msg)))
msg = {'cmd': 'write', 'sid': 'rgbstrip', 'data': {'red': 0, 'green': 0, 'blue': 255, 'dimm': '100'}}
asyncio.run(tcp_echo_client(json.dumps(msg)))
