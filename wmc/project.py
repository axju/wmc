"""Manag the files and data"""
import os
import sys
import json
from datetime import datetime
from wmc.default import COMMON, LINUX, WIN
from wmc.utils import BasicKeys


class ProjectFiles(BasicKeys):
    """docstring for ProjectFiles."""

    KEYS = ['path', 'data', 'videos', 'full', 'intro', 'final', 'cleaned']

    def __init__(self, path):
        super(ProjectFiles, self).__init__()
        self.path = os.path.abspath(path)

    def __getitem__(self, key):
        """ ProjectFiles['info'] """
        if key == 'path':
            return self.path
        if key == 'data':
            return os.path.join(self.path, 'data.json')
        if key == 'videos':
            return list(self.videos())
        if key in ['full', 'final', 'intro', 'cleaned']:
            return os.path.join(self.path, '{key}.mp4'.format(key))
        return None

    def check(self):
        """Check if the project is healthy."""
        return os.path.isfile(self['data'])

    def videos(self):
        """Iterator to grep the video files"""
        for name in os.listdir(self['path']):
            file = os.path.join(self['path'], name)
            if os.path.isfile(file) and name.endswith('.mp4'):
                yield file


class ProjectData(BasicKeys):
    """docstring for ProjectData."""

    KEYS = ['name', 'record', 'size', 'prefix', 'intro', 'intro-record', 'censor']

    def __init__(self, filename, profil=None):
        super(ProjectData, self).__init__()
        self.filename = filename
        self.profil = profil
        self.data = {}

    def __getitem__(self, key):
        """ ProjectData['info'] """
        if key in self.KEYS:
            return self.data.get(key)
        return None

    def load(self):
        """Load the data from the file"""
        with open(self.filename) as file:
            self.data = json.load(file)
        if self.profil and self.profil in self.data['profils']:
            self.data = self.data['profils'][self.profil]

    def save(self):
        """Save the data to the file"""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4, sort_keys=True)

    def create(self):
        """Create the data file"""
        self.data = {
            'name': os.path.basename(os.path.dirname(self.filename)),
            'profils': {}
        }
        for key, value in COMMON.items():
            self.data[key] = value

        if sys.platform in ['linux', 'linux2']:
            defaults = LINUX
        elif sys.platform in ['win32', 'win64']:
            defaults = WIN
        else:
            defaults = {}
        for key, value in defaults.items():
            self.data[key] = value

        self.save()

    def check(self):
        """Check if the data file is healthy."""
        for key in self.KEYS:
            if key not in self.data:
                return False
        return True


class Project(BasicKeys):
    """Manage the data and files for one project folder."""

    KEYS = ['name', 'video', 'records']

    def __init__(self, path, profil=None):
        super(Project, self).__init__()
        self.files = ProjectFiles(path)
        self.data = ProjectData(self.files['data'], profil)

    def __getitem__(self, key):
        """ ProjectFiles['info'] """
        if key == 'name':
            return self.data['name']
        if key == 'video':
            now = datetime.now().strftime('%Y%m%d%H%M.mp4')
            return os.path.join(self.files['path'], self.data['prefix'] + now)
        if key == 'records':
            return sorted(list(filter(lambda x: x.find(self.data['prefix']) > 0, self.files['videos'])))
        return None

    def create(self):
        """Create the info file"""
        if os.path.isfile(self.files['path']):
            raise Exception('Your project look like a file')

        if os.path.isdir(self.files['path']) and os.listdir(self.files['path']):
            raise Exception('The folder is not empty. '
                            'You have to delete it yourself.')

        if not os.path.isdir(self.files['path']):
            os.makedirs(self.files['path'])
        self.data.create()

    def check(self):
        """Check if the project is healthy."""
        return self.files.check() and self.data.check()
