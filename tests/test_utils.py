import unittest
from wmc.utils import resize_window


class TestResizeWindow(unittest.TestCase):

    def test_call(self):
        callable = hasattr(resize_window, '__call__')
        self.assertTrue(callable)


if __name__ == '__main__':
    unittest.main()
