import unittest
import os
from .support import TempdirManager
from wmc.project import ProjectData, Project


class TestProjectData(TempdirManager, unittest.TestCase):

    def test_basic(self):
        dir = self.mkdtemp()
        path = os.path.join(dir, 'test_data.json')
        data = ProjectData(path)
        data.create()
        for key in ['record', 'size', 'prefix']:
            self.assertIn(key, data)


class TestProject(TempdirManager, unittest.TestCase):

    def test_basic(self):
        dir = self.mkdtemp()
        path = os.path.join(dir, 'foo.json')
        data = Project(path)
        data.create()
        for key in ['name', 'video', 'records']:
            self.assertIn(key, data)


if __name__ == '__main__':
    unittest.main()
