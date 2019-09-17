import os
import unittest
from wmc.utils import BasicCommand


class TestBasicCommand(unittest.TestCase):

    def test_init(self):
        cmd = BasicCommand(path='/temp', file='foo.json')
        self.assertEqual('/temp', cmd.path)
        self.assertEqual('foo.json', cmd.file)
        self.assertEqual(os.path.join('/temp', 'foo.json'), cmd.filename)

        self.assertIn('name', cmd.settings)
        self.assertIn('path', cmd.settings)
        self.assertDictEqual(cmd.settings, {'name': 'temp', 'path': '/temp'})

    def test_init_defaults(self):
        cmd = BasicCommand()
        self.assertEqual(os.getcwd(), cmd.path)
        self.assertEqual('data.json', cmd.file)
        self.assertEqual(os.path.join(os.getcwd(), 'data.json'), cmd.filename)

    def test_parser(self):
        cmd = BasicCommand()
        self.assertFalse(cmd.args)
        cmd.parse_args([])
        self.assertTrue(cmd.args)

    def test_help(self):
        cmd = BasicCommand()
        self.assertIsInstance(cmd.help, str)
        self.assertEqual(cmd.help, 'The BasicCommand')

    def test_keys(self):
        cmd = BasicCommand()
        self.assertIn('name', cmd)
        self.assertIn('path', cmd)
        self.assertEqual(os.getcwd(), cmd['path'])

    def test_check(self):
        cmd = BasicCommand()
        self.assertRaises(Exception, cmd.check)

    def test_basic(self):
        cmd = BasicCommand()
        with self.assertLogs('BasicCommand', level='INFO') as cm:
            cmd.setup()
            self.assertIn('INFO:BasicCommand:Setup command', cm.output)
            cmd.create()
            self.assertIn('INFO:BasicCommand:Create settings', cm.output)
            cmd.main()
            self.assertIn('INFO:BasicCommand:Run command', cm.output)







if __name__ == '__main__':
    unittest.main()
