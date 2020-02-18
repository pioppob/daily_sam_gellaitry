from flask.cli import FlaskGroup
from my_app import create_app, db
from my_app.config import Config
from my_app.main.models import Track
import json
from my_app.main.services import set_default_thumbnail

app = create_app()
cli = FlaskGroup(create_app=create_app)



@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('add_json_tracks')
def add_json_tracks():
    """
    Populates the database with the data supplied by the given .json file.

    Unfortunately soundcloud has stopped processing API application requests
    so everything from here on is reverse engineered using a web-scraper
    and tracing network IO in chrome devtools.
    """

    with open(Config.JSON_TRACK_DATA) as json_file:
        json_content = json.load(json_file)

    for row in json_content['rows']:

        thumbnail = row["image"]
        if not thumbnail:
            thumbnail = set_default_thumbnail()

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
    return f"Added {len(json_content['rows'])} tracks to the database."


if __name__ == '__main__':
    cli()
