import unittest
from wmc.dispatch import get_basic_call, find_entry_points, load_entry_points
from wmc.utils import BasicCommand

class TestDispatch(unittest.TestCase):

    def test_get_basic_call(self):
        calls = get_basic_call()
        for item in calls:
            self.assertIsInstance(item, str)
        self.assertTrue(calls)

    def test_find_entry_points(self):
        entrys = find_entry_points()
        for item in entrys:
            self.assertIsInstance(item, str)
        self.assertTrue(entrys)

    def test_load_entry_points(self):
        entrys = load_entry_points()
        for name, cls in entrys.items():
            self.assertIsInstance(name, str)
            self.assertTrue(issubclass(cls, BasicCommand))
        self.assertTrue(entrys)


if __name__ == '__main__':
    unittest.main()
