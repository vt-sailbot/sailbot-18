import unittest
import context

# import any extra stuff here
import calc

class TestClassSample(unittest.TestCase):
    """Sample test class.

    Test classes should be named 'Test*' in files named 'test*'.
    """

    def setUp(self):
        """Runs before each test method."""
        self.p1 = calc.Point((20, 80))
        self.p2 = calc.Point((30, 80))

    def test_sample_test(self):
        """Sample test method.

        Test methods should be named 'test*'.
        """
        self.assertAlmostEqual(calc.distance(self.p1, self.p2), 1111949.2664455848)

    def tearDown(self):
        """Runs after all test methods."""
        pass
