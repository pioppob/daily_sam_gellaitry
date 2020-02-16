from my_app import db
import datetime

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), default='Sam Gellaitry')
    description = db.Column(db.String(256), default=None)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    thumbnail = db.Column(db.String(256), nullable=False)
    audio = db.Column(db.Text, nullable=False)
    last_daily_sam = db.Column(db.DateTime(), default=None)

    def __repr__(self):
        return f'<Track: {self.title}>'

# thumbnail = db.Column(db.LargeBinary, nullable=False)
# binary_audio = db.Column(db.LargeBinary, nullable=False)