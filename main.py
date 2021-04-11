import time

from flask import Flask
import socketio
from flask_cors import CORS
from threading import Timer

sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')
app = Flask(__name__)
cors = CORS(app)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
queue = []
turn_length = 20


@sio.on('connect')
def on_connect(sid, environ):
    print("connect", sid)
    if len(queue) == 0:
        print("First person connected, starting their turn...")
        t = Timer(turn_length, next_person)
        t.start()
    queue.append(sid)
    print(queue)
    sio.emit('queue', {"queue": queue})


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    queue.remove(sid)


def next_person():
    print("Next turn...")
    person = queue.pop(0)
    sio.emit('clear', {})
    time.sleep(1)
    queue.append(person)
    print(queue)


    sio.emit('queue', {"queue": queue})
    t = Timer(turn_length, next_person)
    t.start()


@sio.on('move')
def move(sid, data):
    sio.emit('queue', {"queue": queue})
    print(queue)

    print(data)
    if sid == queue[0]:
        print("Validated")
        sio.emit('move', data)
    else:
        print("Denied.")


@sio.on('ignoreme')
def ignoreme(sid, data):
    queue.remove(sid)


@sio.on('echo')
def echo(sid, data):
    print(sid, "echoes", data)


# ... Socket.IO and Flask handler functions ...

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
