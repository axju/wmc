import os
import unittest
from wmc.cli import create_parse, main


class TestCli(unittest.TestCase):

    def test_create_parse(self):
        parser = create_parse(['test'])
        args = parser.parse_args([])
        self.assertEqual(args.path, os.getcwd())
        self.assertEqual(args.settings, 'data.json')

    #def test_main(self):
    #    main(['-H'])


if __name__ == '__main__':
    unittest.main(buffer=True)
