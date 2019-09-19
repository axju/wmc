"""The basic commands"""
import os
import sys
from datetime import datetime
from time import sleep

import ffmpeg
from screeninfo import get_monitors
from wmc.utils import BasicCommand


class Record(BasicCommand):
    """Start the record"""

    def _get_input(self, platform, **kwargs):
        """framerate=1, video_size=[1920, 1080], show_region=1, offset_x=-1920"""
        data = {}
        if platform.startswith('win'):
            data['filename'] = 'desktop'
            data['f'] = 'gdigrab'
            data['show_region'] = kwargs.get('show_region', 1)
            data['offset_x'] = kwargs.get('offset_x', -1920)
        elif platform.startswith('linux'):
            data['filename'] = ':0.0+0,0'
            data['f'] = 'x11grab'
        else:
            self.logger.warning('The platform "%s" is not supported', platform)
        data['framerate'] = kwargs.get('framerate', 1)
        data['video_size'] = kwargs.get('video_size', [1920, 1080])
        return data

    def _get_output(self, **kwargs):
        """framerate=30"""
        return {
            'vcodec': 'libx264',
            'preset': 'ultrafast',
            'r': kwargs.get('framerate', 30),
        }

    def _get_settings(self):
        settings = self.settings['record']
        for key in ['input', 'output']:
            args = getattr(self.args, key, None)
            if not args:
                continue
            for arg in args.split(','):
                values = arg.split('=')
                settings[key][values[0]] = values[1] if len(values) > 1 else True
        if self.args.setpts:
            settings['setpts'] = self.args.setpts
        return settings

    def setup_parser(self):
        """Setup some command arguments"""
        super(Record, self).setup_parser()
        self.parser.add_argument('-t', '--time', type=int, help='set a fix time to run')
        self.parser.add_argument('-s', '--show', action='store_false', help='show ffmpeg output')
        self.parser.add_argument('--input', help='overwrite input settings --input "framerate=30,video_size=[500,500]"')
        self.parser.add_argument('--output', help='overwrite output settings --output "r=60"')
        self.parser.add_argument('--setpts', help='overwrite setpts settings --setpts "N/TB/60"')

    def create(self, **kwargs):
        """Create the basic settings"""
        super(Record, self).create()

        user = {
            'framerate': 1, 'width': 1920, 'height': 1080,
            'offset_x': -1920, 'offset_y': 0,
        }
        if not kwargs.get('silent', False):
            user['framerate'] = input('Framerate[1]: ') or 1
            for i, monitor in enumerate(get_monitors(), start=1):
                print('{:>6} : {}'.format(i, monitor.name))
            print('-1 : set custom video size')
            index = int(input('Select monitor [1]: ') or 1)
            if index == -1:
                for key in ['width', 'height', 'offset_x', 'offset_y']:
                    user[key] = input('Set {} [{}]: '.format(key, user[key])) or user[key]
                user['video_size'] = [user['width'], user['height']]
            else:
                monitor = get_monitors()[index-1]
                user['video_size'] = [monitor.width, monitor.height]
                user['offset_x'], user['offset_y'] = monitor.x, monitor.y

        self.settings['record'] = {
            'input': self._get_input(sys.platform, **user),
            'output': self._get_output(),
            'setpts': 'N/TB/30',
        }

    def main(self, **kwargs):
        """Start the record"""
        super(Record, self).create()
        now = datetime.now().strftime('%Y%m%d%H%M.mp4')
        filename = os.path.join(self.settings['path'], 'video_' + now)
        settings = self._get_settings()
        stream = ffmpeg.input(**settings['input']).setpts(settings['setpts'])
        stream = ffmpeg.output(stream, filename, **settings['output'])
        process = ffmpeg.run_async(
            stream,
            pipe_stdin=True,
            pipe_stdout=True,
            pipe_stderr=self.args.show,
            overwrite_output=True,
        )
        try:
            if self.args.time:
                self.logger.info('record the screen for %i sec', self.args.time)
                for _ in range(self.args.time):
                    sleep(1)
            else:
                input('press enter to finish ')
        except KeyboardInterrupt:
            self.logger.info('breack with KeyboardInterrupt')

        finally:
            self.logger.info('save file')
            process.communicate(input=b"q")
