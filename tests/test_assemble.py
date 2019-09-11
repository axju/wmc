import unittest
import os
from .support import TempdirManager
from wmc.assemble import Interface


class TestInterface(TempdirManager, unittest.TestCase):

    def test_create(self):
        dir = self.mkdtemp()
        self.assertRaises(Exception, Interface, dir)

        interface = Interface(dir, check=False)
        self.assertIsInstance(interface, Interface)
        interface = Interface(dir, create=True)
        self.assertIsInstance(interface, Interface)


if __name__ == '__main__':
    unittest.main()
