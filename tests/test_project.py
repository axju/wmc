import unittest
import os
from .support import TempdirManager
from wmc.project import ProjectFiles, ProjectData, Project


class TestProjectFiles(TempdirManager, unittest.TestCase):

    def test_basic(self):
        dir = self.mkdtemp()
        data = ProjectFiles(dir)
        for key in ['path', 'data', 'videos', 'full', 'intro', 'final', 'cleaned']:
            self.assertIn(key, data)


class TestProjectData(TempdirManager, unittest.TestCase):

    def test_basic(self):
        dir = self.mkdtemp()
        path = os.path.join(dir, 'foo.json')
        data = ProjectData(path)
        data.create()
        for key in ['name', 'record', 'size', 'prefix', 'intro', 'intro-record', 'censor']:
            self.assertIn(key, data)
        self.assertEqual(os.path.basename(dir), data['name'])


class TestProject(TempdirManager, unittest.TestCase):

    def test_basic(self):
        dir = self.mkdtemp()
        path = os.path.join(dir, 'foo')
        data = Project(path)
        data.create()
        for key in ['name', 'video', 'records']:
            self.assertIn(key, data)
        self.assertEqual('foo', data['name'])


if __name__ == '__main__':
    unittest.main()
