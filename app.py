#!/usr/bin/env python

async_mode = None
if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass
    
    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass
    
    if async_mode is None:
        async_mode = 'threading'
    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
threadpool = []
roomsDict = {}
games = []
inputlock = 0

def background_thread(args):
    print("background thread")
    while True:
        time.sleep(1)
        if(games[args] is not None):
            print(games[args])
            
@app.route('/')
def index():
    global threadpool
    if threadpool is None:
        thread = Thread(target=background_thread, args=(len(threadpool)-1))
        thread.daemon = True
        thread.start()
        threadpool.append(thread)
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socketio.on('start_game', namespace='/test')
def start_game(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    if not roomsDict[message['room']]['start']:# and len(roomsDict[message['room']]['users']) >= 3:
        roomsDict[message['room']]['start'] = True
        emit('my response',
             {'data': '<span class="username">Deceit</span>: ' + session['username'] + ' started the game!', 'count': session['receive_count']},
             room=message['room'])
        emit('my response',
             {'data': '<span class="username">' + message['room'].capitalize() + 'Bot</span>: Starting the game!', 'count': session['receive_count']},
             room=message['room'])
        global games
        games.append(game.Game(roomsDict[message['room']]['users'], message['room']))
        return True
    elif roomsDict[message['room']]['start']:
        emit('my response',
             {'data': '<span class="username">Deceit</span>: Game currently in progress!', 'count': session['receive_count']})        
        return False
    else:
        emit('my response',
             {'data': '<span class="username">Deceit</span>: Not enough players to start the game.', 'count': session['receive_count']})        
        return False

@socketio.on('join', namespace='/test')
def join(message):
    global roomsDict
    session['username'] = message['username']
    if message['room'] not in roomsDict:
        roomsDict[message['room']] = {
            'users': [],
            'start': False
        }
    else:
        if len(roomsDict[message['room']]['users']) > 3:
            emit('my response',
             {'data': '<span class="username">Deceit</span>: Could not join ' + message['room'] + '(room is full)',
             'count': session['receive_count']})
            return False
    roomsDict[message['room']]['users'].append(session['username'])
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': '<span class="username">Deceit</span>: Joined ' + message['room'],
          'count': session['receive_count']})
    emit('my response',
         {'data': '<span class="username">' + message['room'].capitalize() + 'Bot</span>: ' + session['username'] + ' has entered the room',
          'count': session['receive_count']}, room=message['room'])
    return True

@socketio.on('leave', namespace='/test')
def leave(message):
    global roomsDict
    leave_room(message['room'])
    roomsDict[message['room']]['users'].remove(session['username'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': '<span class="username">Deceit</span>: Left ' + message['room'],
          'count': session['receive_count']})
    emit('my response',
         {'data': '<span class="username">' + message['room'].capitalize() + 'Bot</span>: ' + session['username'] + ' has left the room',
          'count': session['receive_count']}, room=message['room'])

@socketio.on('close room', namespace='/test')
def close(message):
    global roomsDict
    session['receive_count'] = session.get('receive_count', 0) + 1
    if message['room'] in roomsDict:
        del roomsDict[message['room']]
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])

def parseCommand(message, command):
    print("PARSING COMMAND")
    if(command.split()[0] == '/a'):
        choosecardevent(int(command.split()[1]))

#@socketio.on('choose card event', namespace='/test')
def choosecardevent(message):
    print("cardevet" + str(message))
    inptt = message
    return

@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    print(message['data'])
    if(message['data'][0] == '/'):
        parseCommand(message, message['data'])
    else:
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my response',
         {'data': '<span class="username">' + session.get('username', '') + '</span>: ' + message['data'], 'count': session['receive_count']},
         room=message['room'])  

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': '<span class="username">Deceit</span>: Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': '<span class="username">Deceit</span>: Establishing connection...', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
