import unittest
from my_sample import MySample

class TestMySample(unittest.TestCase):

    def test_name(self):
        s = MySample()
        self.assertEqual(s.name(), "my name")


if __name__ == '__main__':
    unittest.main()
