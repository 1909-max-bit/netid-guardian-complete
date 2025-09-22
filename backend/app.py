# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
db_path = os.environ.get('DB_PATH', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    data = db.Column(db.Text)
    timestamp = db.Column(db.Integer)

    def as_dict(self):
        return {'id': self.id, 'type': self.type, 'data': self.data, 'timestamp': self.timestamp}

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/events', methods=['POST'])
def receive_event():
    payload = request.get_json(force=True)
    ev = Event(type=payload.get('type'), data=json.dumps(payload), timestamp=payload.get('timestamp', int(time.time())))
    db.session.add(ev)
    db.session.commit()
    return jsonify({'status':'ok','id':ev.id}), 201

@app.route('/api/events', methods=['GET'])
def list_events():
    evs = Event.query.order_by(Event.id.desc()).limit(200).all()
    return jsonify([e.as_dict() for e in evs])

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status':'ok','time': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
