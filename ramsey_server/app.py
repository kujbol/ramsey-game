#! /usr/bin/env python
import asyncio
import os

import aiohttp_cors
import aiohttp_jinja2
import jinja2
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

from ramsey_server.routes import routes
from ramsey_server.settings import *


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, handler):
    server.close()
    await server.wait_closed()
    await app.shutdown()
    await handler.shutdown(10.0)
    await app.cleanup()


def init():
    app = web.Application(middlewares=[
        session_middleware(EncryptedCookieStorage(SECRET_KEY)),
    ])
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    setup_statics(app)
    setup_cors(app)

    app.on_shutdown.append(on_shutdown)

    app['rooms'] = {}
    app['games'] = {}

    return app


def setup_statics(app):
    root_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(root_dir, 'ramsey_front/dist')
    static_path = os.path.join(template_path, 'static')

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_path))
    app.router.add_static(
        '/static/', path=static_path, name='static'
    )


def setup_cors(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
            allow_methods="*",
        ),
    })
    for route in app.router.routes():
        cors.add(route)


initialized_app = init()
log.debug('app_initialized')


# loop = asyncio.get_event_loop()
# serv_generator, handler, app = loop.run_until_complete(init(loop))
# serv = loop.run_until_complete(serv_generator)
# log.debug('start server %s' % str(serv.sockets[0].getsockname()))
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     log.debug('Stop server begin')
# finally:
#     loop.run_until_complete(shutdown(serv, app, handler))
#     loop.close()
# log.debug('Stop server end')
