import asyncio
import time

from aiohttp import web


async def handle(request):
    await asyncio.sleep(0.1)
    return web.Response(text='Hello, Anonymous')

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=8088, host='0.0.0.0')
