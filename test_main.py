# IMPORTS
import main # We will be testing the "main.py" functions
import unittest # To ensure no breaking of functionality during commits

# Classes
class UnitTests(unittest.TestCase):
    '''
    This class will eventually test the functions in "main" to ensure that nothing
    major is broken between commits.
    '''

    # An example test
    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "function sum() command does not work.")


if __name__ == "__main__":
    # First, ensure no tests fail and we are working with a reliable build.
    unittest.main()
