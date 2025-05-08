from app import create_app
from app.socketio_instance import socketio


flask_app = create_app()
socketio.init_app(flask_app)

if __name__ == '__main__':
    socketio.run(flask_app, port='5001', debug=True, allow_unsafe_werkzeug=True)
