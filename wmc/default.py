"""Some constant default values"""

COMMON = {
    'prefix': 'video_',
    "intro": {
        "prompt": ">>> ",
        "wait": 1,
        "font": "univers",
        "cmds": [
            {
                "input": "cat intro.txt",
                "output": [
                    {"text": "\n\n\n\n"},
                    {"title": "Watch me coding"},
                    {"text": "\n\n\n"},
                ],
            },
            {
                "input": "python load_info.py",
                "output": [
                    {"progressbar": None},
                    {"text": "I code some crazy stuff...\n"},
                ],
            },
            {
                "input": "vcl video.mp4",
                "output": [
                    {"text": "[*] Load video"},
                    {"progressbar": None},
                ],
            },
        ],
    }
}

LINUX = {
    'size':  [0, 0, 1920, 1080],
    'record': {
        "input": {
            "filename": ":0.0+0,0",
            "f": "x11grab",
            "video_size": (1920, 1080),
        },
        "output": {
            "vcodec": "libx264",
            "preset": "ultrafast",
            "r": 30,
        },
        "setpts": "N/TB/30",
    },
    'intro-record': {
        "input": {
            "filename": ":0.0+0,0",
            "f": "x11grab",
            "video_size": (1920, 1080),
        },
        "output": {
            "vcodec": "libx264",
            "preset": "ultrafast",
            "r": 30,
        },
        "setpts": "N/TB/30",
    },
}

WIN = {
    'size': [-1928, -4, 1935, 1093],
    'record': {
        "input": {
            "filename": "desktop",
            "f": "gdigrab",
            "framerate": 1,
            "video_size": (1920, 1080),
            "offset_x": -1920,
            "show_region": 1,
        },
        "output": {
            "vcodec": "libx264",
            "preset": "ultrafast",
            "r": 30,
        },
        "setpts": "N/TB/30",
    },
    'intro-record': {
        "input": {
            "filename": "desktop",
            "f": "gdigrab",
            "framerate": 1,
            "video_size": (1920, 1080),
            "offset_x": -1920,
            "show_region": 1,
        },
        "output": {
            "vcodec": "libx264",
            "preset": "ultrafast",
            "r": 30,
        },
        "setpts": "N/TB/30",
    },
}
