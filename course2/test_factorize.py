import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        """
        Check if a float or str argument passed to the function raises an TypeError exception.
        """
        for f, t in (factorize, 1.5), (factorize, 'string'):
            with self.subTest(x=f):
                self.assertRaises(TypeError, f, t)

    def test_negative(self):
        """
        Check if a negative argument passed to the function raises an ValueError exception.
        """
        for f, t in (factorize, -1), (factorize, -10), (factorize, -100):
            with self.subTest(x=f):
                self.assertRaises(ValueError, f, t)

    def test_zero_and_one_cases(self):
        """
        Check if "0" and "1" arguments passed to the function returns tuples with this numbers.
        0 -> (0,) and 1 -> (1,).
        """
        for f, t in (factorize(0), (0,)), (factorize(1), (1,)):
            with self.subTest(x=f):
                self.assertEqual(f, t)

    def test_simple_numbers(self):
        """
        Check if simple argument passed to the function returns tuple with this value.
        3 -> (3,), 13 -> (13,) and 29 -> (29,).
        """
        for f, t in (factorize(3), (3,)), (factorize(13), (13,)), (factorize(29), (29,)):
            with self.subTest(x=f):
                self.assertEqual(f, t)

    def test_two_simple_multipliers(self):
        """
        Check the cases when numbers that passed to the function returns a tuple with the number of elements equal to 2.
        6 -> (2, 3), 26 -> (2, 13) and 121 -> (11, 11).
        """
        for f, t in (factorize(6), (2, 3)), (factorize(26), (2, 13)), (factorize(121), (11, 11)):
            with self.subTest(x=f):
                self.assertEqual(t, f)

    def test_many_multipliers(self):
        """
        Check the cases when numbers that passed to the function returns a tuple with the number of elements more than 2
        1001 -> (7, 11, 13) and 9699690 -> (2, 3, 5, 7, 11, 13, 17, 19).
        """
        for f, t in (factorize(1001), (7, 11, 13)), (factorize(9699690), (2, 3, 5, 7, 11, 13, 17, 19)):
            with self.subTest(x=f):
                self.assertEqual(t, f)


def factorize(x):
    pass
