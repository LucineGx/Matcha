import logging

from flask_socketio import emit

from flaskr import socketio


@socketio.on('connect', namespace='/devices')
def connection_to_socket():
    logging.info('New socket connection')
    emit('HelloWorld', {'data': 'Hello there.'})
