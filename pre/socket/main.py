from aiohttp import web
import socketio
import os

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat')
async def message(sid, data):
    print("message ", data)
    if data == "prev":
        print('prev!')
        # cmd = """osascript -e 'tell app "Finder" to sleep'"""
        # os.system("""osascript -e 'tell app "Finder" to sleep'""")
        os.system("""osascript -e 'tell app "System Events" to key code 126'""")
    else:
        print('next!')
        # cmd = """osascript -e 'tell app "System Events" to key code 125'"""
        os.system("""osascript -e 'tell app "System Events" to key code 125'""")
    await sio.emit('reply', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)