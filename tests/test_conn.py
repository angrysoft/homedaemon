#!/usr/bin/env python3

import asyncio
import json
import sys


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 6666)
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
msg = {'cmd': 'write', 'sid': '158d00029b1929', 'data': {'channel_1': sys.argv[1], 'channel_0': sys.argv[1]}}
asyncio.run(tcp_echo_client(json.dumps(msg)))
