import unittest
import os
from .support import TempdirManager
from wmc.basic import setup, record, link


class TestSetup(unittest.TestCase):

    def test_basic(self):
        settings = {}
        self.assertNotIn('record', settings)
        self.assertTrue(setup(settings))
        self.assertIn('record', settings)


class TestRecord(TempdirManager, unittest.TestCase):
    pass


class TestLink(TempdirManager, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
