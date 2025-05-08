from app import create_app
from flask_socketio import SocketIO


flask_app = create_app()
socketio = SocketIO(flask_app)

if __name__ == '__main__':
    socketio.run(host='0.0.0.0', port='5001', debug=True)
