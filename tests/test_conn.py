#!/usr/bin/env python3

import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 6666)
    for x in range(10):
        message = f'{x}\n'
        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()
        # await asyncio.sleep(1)
        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

# asyncio.run(tcp_echo_client('Test'))
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client('Test'))
loop.close()