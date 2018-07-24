import unittest
from calculator import *

class TestTDD(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2,3),5)

    def test_raise_error(self):
        test_cases = [
            {
                "name":"test incorrect first value",
                "a":'one',
                "b":2,
                "expected":ValueError
            },
            {
                "name":"test incorect second value",
                "a":1,
                "b":'two',
                "expected":ValueError
            },
            {
                "name":"test incorrect both values",
                "a":'one',
                "b":'two',
                "expected":ValueError
            }
        ]
        for tt in test_cases:
            self.assertRaises(tt["expected"],self.calc.add,tt["a"],tt["b"])

if __name__ == '__main__':
    unittest.main()