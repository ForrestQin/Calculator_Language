import unittest
from io import StringIO
import sys
from bc import bc

class TestCalculator(unittest.TestCase):

    def test_baseline(self):
        with open('test_input.txt') as file:
            input = file.read()
        with open('test_output.txt') as file:
            expected_output = file.read()
        with StringIO(input) as sys.stdin, StringIO() as sys.stdout:
            bc()
            self.assertEqual(sys.stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
