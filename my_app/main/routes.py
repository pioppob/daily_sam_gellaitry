from . import bp
from my_app import db
from flask import (
    render_template,
    redirect,
    url_for,
    jsonify,
    make_response,
    send_file
)
from .models import Track
from .forms import AddTrackForm
import random
from datetime import datetime
import time
from my_app.config import Config
from concurrent import futures
from .services import (
    add_one_file,
    set_default_thumbnail
)
import json
import requests


@bp.route("/")
def index():
    """Homepage for the app. Displays every track in the db. TODO: Paginate"""

    tracks = Track.query.all()
    return render_template("index.html", title="Home", tracks=tracks)


@bp.route("/shuffle")
def shuffle():
    """Randomizes order that the tracks are displayed on the homepage"""

    tracks = Track.query.all()
    random.shuffle(tracks)

    return render_template(
        "shuffle.html",
        title="Shuffle Tracks",
        tracks=tracks
    )


@bp.route("/json")
def add_json_tracks():
    """
    Populates the database with the data supplied by the given .json file.

    Unfortunately soundcloud has stopped processing API application requests
    so everything from here on is reverse engineered using a web-scraper
    and tracing network IO in chrome devtools.
    """

    with open(Config.JSON_TRACK_DATA) as json_file:
        json_content = json.load(json_file)

    for row in json_content:

        thumbnail = row["thumbnail"]
        if not thumbnail:
            thumbnail = set_default_thumbnail()
        else:
            thumbnail += f"?client_id={Config.CLIENT_ID}"

        request_url = row["audio_request_url"] + \
            f"?client_id={Config.CLIENT_ID}"

        track = Track(
            title=row["title"],
            description=row["desc"],
            thumbnail=thumbnail,
            audio=request_url,
        )

        # print(track)
        db.session.add(track)

    db.session.commit()
    return f"Added {len(json_content)} tracks to the database."


@bp.route("/play_track/<track_id>/")
def play_track(track_id):
    """
    Purpose:
    This function is invoked for every track displayed on the page.
    It is imbedded in the HTML audio tag's src property and should
    return the audio to make the audio tag playable.

    Info on the track.audio property:
    Soundcloud makes an AJAX call to the url in track.audio which
    returns a response containing the .mpeg audio url. The response
    expires after one call and is programmatically generated on
    every request so no two responses are the same.
    This makes it a pain to work with.

    Goal:
    Simulate the soundcloud AJAX call for every track on the page,
    parse the .mpeg URL from the response and return the audio
    in a format that an HTML <audio> player can understand.
    """

    track = Track.query.filter_by(id=track_id).first()

    res = requests.get(track.audio)
    if not res.status_code == 200:
        return f"Initial request status code: {res.status_code}"

    json_res = json.loads(res.text)
    mpeg_audio_url = json_res["url"]

    

    msg_dict = {"url": mpeg_audio_url}

    # My issue is here: If I hardcode the mpeg_audio_url into the
    # <audio src> HTML property, it works! However, returning the
    # mpeg_audio_url as we do below does not work. My head hurts.

    res = make_response(jsonify({"message": msg_dict}))
    return res


@bp.route("/track_of_the_day")
def track_of_the_day():
    """
    Returns one track based on the day of the year, labeled "Track of the day"
    """

    day_of_year = datetime.now().timetuple().tm_yday
    daily_track_id = day_of_year % 365

    track = Track.query.filter_by(id=daily_track_id).first()

    if track.last_daily_sam != day_of_year:
        track.last_daily_sam = datetime.now().strftime("%b %m, %Y")

    return render_template(
        "daily_sam.html",
        title="Track of the day",
        track=track
    )


@bp.route("/add_local_tracks")
def add_local_tracks():
    """
    Original way of adding tracks to database. Adds tracks asynchronously.
    Requires mp3 and .jpg files already on local machine.

    Do not use: Should use add_json_tracks instead.
    """

    t0 = time.time()

    mp3_list = [x for x in Config.TRACKLIST_DIR if x.endswith(".mp3")]

    with futures.ThreadPoolExecutor(Config.MAX_WORKERS) as executor:
        res = executor.map(add_one_file, mp3_list)

    db.session.bulk_save_objects(list(res))
    db.session.commit()
    elapsed = time.time() - t0

    return f"Uploaded all tracks in {elapsed} seconds."


@bp.route("/add_track")
def add_track():
    """
    Endpoint to add a single track to the db.
    """

    form = AddTrackForm()
    if form.validate_on_submit():

        binary_audio = form.binary_audio.data
        thumbnail = form.thumbnail.data

        track = Track(
            title=form.title.data,
            description=form.description.data,
            thumbnail=thumbnail.read(),
            binary_audio=binary_audio.read(),
        )

        db.session.add(track)
        db.session.commit()
        print("Saved" + binary_audio.filename + "to the database.")
        return redirect(url_for("index"))

    return render_template("add_track.html", title="Add Track", form=form)
