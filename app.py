from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz
import gevent
import gevent.monkey
gevent.monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lovnish_super_secret_key'

socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins='*')

IST = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Send a welcome or empty chat log on user connect (MongoDB removed)."""
    emit('load_messages', [])  # Send empty list instead of past messages

@socketio.on('message')
def handle_message(data):
    """Broadcast messages with nickname and timestamp (MongoDB removed)."""
    nickname = data.get('nickname', 'Anonymous')
    message_text = data.get('message', '')
    
    utc_now = datetime.utcnow()
    utc_now = pytz.utc.localize(utc_now)
    ist_now = utc_now.astimezone(IST)

    message_doc = {
        'nickname': nickname,
        'message': message_text,
        'timestamp': ist_now.strftime("%d-%m-%Y %I:%M %p")
    }

    emit('message', message_doc, broadcast=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
