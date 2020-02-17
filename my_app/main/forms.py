from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class AddTrackForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    artist = StringField("Artist")
    quote = TextAreaField("Quote", validators=[DataRequired()])
    quote_author = StringField("Author", validators=[DataRequired()])
    thumbnail = FileField("Upload Thumbnail", validators=[DataRequired()])
    binary_audio = FileField("Upload Audio", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TrackRequestForm(FlaskForm):
    title = StringField("Song Title", validators=[DataRequired()])
    desc = StringField("Comments (optional)")
    submit = SubmitField("Submit")
