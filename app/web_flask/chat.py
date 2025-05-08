from flask import Blueprint, render_template, jsonify
from flask_login import current_user
from app.models.student_model import STUDENT
from app.models.prof_model import PROFESSOR
from app.models.message import MESSAGE
from flask_socketio import emit
from app.socketio_instance import socketio
from app.db_storage import db
from sqlalchemy import or_


time = "%y/%b/%d %H:%M"
bp = Blueprint('chat', __name__, template_folder="templates", static_folder="static")


@bp.route('/chat')
def chat():
    """route that renders the chat template"""
    profs = PROFESSOR.query.all()
    stds = STUDENT.query.all()
    return render_template('chat.html', profs=profs, stds=stds)


@socketio.on('send_message')
def handle_send_message(data):
    """function that handles the send_message event"""
    sender_id = current_user.id
    recipient_id = data['recipient_id']
    content = data['content']

    new_message = MESSAGE(sender_id=sender_id,
                          recipient_id=recipient_id,
                          content=content,
                          )
    db.session.add(new_message)
    db.session.commit()

    emit('message_received', {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'content': content,
        'timestamp': new_message.created_at.strftime(time)
    })


@bp.route('/history/<user_id>', methods=['GET'])
def get_message_history(user_id):
    messages = MESSAGE.query.filter(
        or_(
            (MESSAGE.sender_id == current_user.id) & (MESSAGE.recipient_id == user_id),
            (MESSAGE.sender_id == user_id) & (MESSAGE.recipient_id == current_user.id)
        )
    ).order_by(MESSAGE.created_at).all()
    history = [{
        'content': msg.content,
        'timestamp': msg.created_at.strftime(time)
    } for msg in messages]
    return jsonify(history)
