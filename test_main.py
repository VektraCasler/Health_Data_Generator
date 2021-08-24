# IMPORTS
import main # We will be testing the "main.py" functions
import unittest # To ensure no breaking of functionality during commits

# Classes
class TestSSN(unittest.TestCase):
    # This class tests the functionality of generate_SSN()

    def test_generate_SSN_returns_string(self):
        # Ensure that a string is returned from generate_SSN()
        test = main.generate_SSN()
        assert isinstance(test, str)
        
    
class TestSurname(unittest.TestCase):
    # This class tests the functionality of generate_surname()

    # Tests generate_SSN
    def test_generate_surname_returns_string(self):
        # Ensure that a string is returned from generate_SSN()
        test = main.generate_surname("Asian", "Not Hispanic", "Female")
        assert isinstance(test, str)


if __name__ == "__main__":
    # First, ensure no tests fail and we are working with a reliable build.
    unittest.main()
