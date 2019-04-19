from spooti import driver
import unittest
import sys
import io

class testDriver(unittest.TestCase):

    def test_print_status(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        cool = 'Mc Ride'
        depth = 1
        driver.print_status(cool, depth)
        sys.stdout = sys.__stdout__
        self.assertEqual('Current node is Mc Ride and depth is 1\n', capturedOutput.getvalue())

    

        