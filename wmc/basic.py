import os
import ffmpeg
from datetime import datetime


def setup(settings):
    settings['record'] = {
        "input": {
            "filename": ":0.0+0,0",
            "f": "x11grab",
            "framerate": 1,
            "video_size": (1920, 1080),
        },
        "output": {
            "vcodec": "libx264",
            "preset": "ultrafast",
            "r": 30,
        },
        "setpts": "N/TB/30",
    }
    return True


def info(settings, args):
    print(settings)


def record(settings, args):
    now = datetime.now().strftime('%Y%m%d%H%M.mp4')
    filename = os.path.join(settings['path'], 'video_' + now)
    stream = ffmpeg.input(**settings['record']['input']).setpts(settings['record']['setpts'])
    stream = ffmpeg.output(stream, filename, **settings['record']['output'])
    ffmpeg.run(stream, overwrite_output=True)


def link(settings, args):
    """concat all videos to one"""
    records = []
    for record in os.listdir(settings['path']):
        if record.startswith('video_'):
            records.append(os.path.join(settings['path'], record))
    stream = ffmpeg.input(records[0])
    for video in records[1:]:
        stream = stream.concat(ffmpeg.input(video))
    stream = ffmpeg.output(stream, os.path.join(settings['path'], 'full.mp4'))
    ffmpeg.run(stream, overwrite_output=True)
