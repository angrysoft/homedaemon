#!/usr/bin/env python3

import asyncio
import json
import sys
from time import sleep

ip = '192.168.1.4'


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(ip, 6666)
    message = f'{message}\n'
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()
    # await asyncio.sleep(1)
    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

#msg = {'cmd': 'write', 'sid': '158d00027d0065', 'model': 'plug', 'data': {'toogle': ''}}
#asyncio.run(tcp_echo_client(json.dumps(msg)))

#msg = {'cmd': 'write', 'sid': '158d00027d0065', 'model': 'plug', 'data': {'status': sys.argv[1]}}
#asyncio.run(tcp_echo_client(json.dumps(msg)))

#msg = {'cmd': 'write', 'sid': '0x0000000007e7bae0', 'data': {'set_power': sys.argv[2]}}
#asyncio.run(tcp_echo_client(json.dumps(msg)))


msg = {'cmd': 'write', 'sid': 'rgb01', 'data': {'red': sys.argv[1], 'green': sys.argv[2], 'blue': sys.argv[3], 'dim': sys.argv[4]}}
asyncio.run(tcp_echo_client(json.dumps(msg)))
#sleep(10)
#msg = {'cmd': 'write', 'sid': 'rgb01', 'data': {'status': sys.argv[3]}}
#asyncio.run(tcp_echo_client(json.dumps(msg)))
