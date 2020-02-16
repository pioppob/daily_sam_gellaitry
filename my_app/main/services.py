import os
import random
from PIL import Image
from my_app.config import Config

def set_default_thumbnail():
    """Sets default thumbnail for the track"""

    defaultDir = os.listdir(Config.BASEDIR + '/static/default_images')
    thumbnail = random.choice(defaultDir)
    thumbnail = Config.BASEDIR + '/static/default_images/' + thumbnail
    
    return thumbnail


def check_thumbnail_dimensions(thumbnail):
    """Checks if the image is the correct size"""

    with Image.open(thumbnail) as img:
        if not img.size == (500, 500):
            raise Exception('Images must be 500x500 pixels.')


def add_one_file(filename):
    """
    This function is invoked by the ThreadPoolExecutor in the add_local_tracks method. 
    This function requires an .mp3 file and optionally .jpg file stored 
    somewhere on the local machine.
    """

    thumbnail = filename[:-4] + '.jpg'

    try:
        check_thumbnail_dimensions(thumbnail)
    except:
        print(f'THUMB NOT FOUND OR WRONG SIZE - USING DEFAULT FOR {filename}')
        thumbnail = set_default_thumbnail()

    with open(filename, 'rb') as f, open(thumbnail, 'rb') as t:

        track = Track(
            
            title=filename[15:-4], 
            artist='Sam Gellaitry',
            description='No desc.', 
            thumbnail=t.read(),
            binary_audio=f.read()
        )
        
    return track

