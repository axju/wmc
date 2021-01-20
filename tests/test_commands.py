import os
import unittest
from .support import TempdirManager
from wmc.commands import Setup, Info, Record, Link


class BasicCommandTest(TempdirManager, unittest.TestCase):

    def get_cmd(self, cls, setup=True):
        path = os.path.join(self.mkdtemp(), 'foo')
        if setup:
            Setup(path=path).run([])

        return cls(path=path)


class TestSetup(BasicCommandTest):

    def test_main(self):
        cmd = self.get_cmd(Setup, False)
        self.assertFalse(os.path.exists(cmd.filename))
        cmd.run([])
        self.assertTrue(os.path.exists(cmd.filename))
        self.assertRaises(Exception, cmd.check)


class TestInfo(BasicCommandTest):
    def test_main(self):
        cmd = self.get_cmd(Info)
        cmd.run([])


class TestRecord(BasicCommandTest):
    def test_main(self):
        cmd = self.get_cmd(Record)
        cmd.run(['-t', '1'])


class TestLink(BasicCommandTest):
    def test_main(self):
        cmd = self.get_cmd(Link)
        cmd.run([])


if __name__ == '__main__':
    unittest.main()
