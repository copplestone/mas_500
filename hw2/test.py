from hw2 import fetch_data
import unittest

class MediaCloudTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_API(self):
    	self.results = fetch_data()
    	self.assertTrue(len(self.results)==3)

# if this file is run directly, run the tests
if __name__ == "__main__":
    unittest.main()
