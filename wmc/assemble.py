"""Assemble the data and command together"""
import os
import logging
import ffmpeg
from tempfile import mkdtemp
from lying.utils import Terminal
from wmc.project import Project
from wmc.utils import resize_window


class Interface():
    """docstring for Interface."""

    def __init__(self, path, profil=None, create=False, check=True):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.proj = Project(path, profil)

        if create:
            self.proj.create()

        if os.path.isfile(self.proj.files['data']):
            self.proj.data.load()

        if check and not self.proj.check():
            raise Exception('This is not a wmc project.')

        self.logger.info('Create a Project object')

    def info(self):
        """Print some project infos"""
        print('Name:   ', self.proj['name'])
        print('Records:', len(self.proj['records']))

    def record(self):
        """start the record"""
        filename = self.proj['video']
        setting = self.proj.data['record']
        stream = ffmpeg.input(**setting['input']).setpts(setting['setpts'])
        stream = ffmpeg.output(stream, filename, **setting['output'])
        ffmpeg.run(stream, overwrite_output=True)

    def size(self):
        """change the size of the foreground window"""
        resize_window(self.proj.data['size'])

    def link(self):
        """concat all videos to one"""
        stream = ffmpeg.input(self.proj['records'][0])
        for video in self.proj['records'][1:]:
            stream = stream.concat(ffmpeg.input(video))
        stream = ffmpeg.output(stream, self.proj.files['full'])
        ffmpeg.run(stream, overwrite_output=True)

    def intro(self):
        """create a nice intro"""
        setting = self.proj.data['intro-record']
        stream = ffmpeg.input(**setting['input'])
        stream = ffmpeg.output(stream, self.proj.files['intro'], **setting['output'])
        process = ffmpeg.run_async(
            stream,
            pipe_stdin=True,
            pipe_stdout=True,
            pipe_stderr=True,
            overwrite_output=True,
        )

        cmds = self.proj.data['intro']['cmds']
        prompt = self.proj.data['intro'].get("prompt", ">> ")
        wait = self.proj.data['intro'].get("wait", 1)
        terminal = Terminal(cmds, prompt=prompt, wait=wait)
        terminal.run(auto_exit=True)

        process.communicate(input=b"q")

    def clean(self):
        """cleanup all video frames"""
        #tmpdir = mkdtemp()
        tmpdir = 'C:/Users/ajura/AppData/Local/Temp/tmp29ngwhnl'
        print(tmpdir)
        stream = ffmpeg.input(self.proj.files['full'])
        stream = ffmpeg.output(stream, tmpdir+'/test%06d.png')
        ffmpeg.run(stream, overwrite_output=True)

        PASSWORD
