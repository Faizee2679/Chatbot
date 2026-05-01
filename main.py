from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, async_mode="threading")

# store messages per room
rooms_data = {
    "general": [],
    "gaming": [],
    "tech": [],
    "random": [],
    "support": []
}

@app.route("/chatbot")
def chatbot():
    return render_template("chat2.0.html")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)

    for msg in rooms_data[room]:
        socketio.emit('message', msg, room=request.sid)

@socketio.on('leave')
def handle_leave(data):
    leave_room(data['room'])

@socketio.on('message')
def handle_message(data):
    room = data['room']

    # save message
    rooms_data[room].append(data)

    # send to everyone in that room
    socketio.emit('message', data, room=room)

if __name__ == '__main__':
    socketio.run(app)