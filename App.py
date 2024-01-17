from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # SQLite database file
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages=messages)

@socketio.on("message")
def handle_message(data):
    message_content = data["message"]

    # Save the message to the database
    with app.app_context():
        new_message = Message(content=message_content)
        db.session.add(new_message)
        db.session.commit()

    # Broadcast the message to all connected clients
    socketio.emit("message", {"message": message_content})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables before running the app
    socketio.run(app, host='BoxStudios.pythonanywhere.com', port=443, debug=True, use_reloader=False)

