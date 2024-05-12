from django.test import SimpleTestCase
from app.calc import add_two_numbers


class CalcTest(SimpleTestCase):
    "Test calc module"

    def test_calc_two_numbers(self):
        res = add_two_numbers(10, 11)
        expected = 21

        self.assertEqual(res, expected)
