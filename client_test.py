import socketio

sio = socketio.Client()

sio.connect('http://localhost:5000')
print('my sid is', sio.sid)


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on("move")
def move(data):
    print(data)
