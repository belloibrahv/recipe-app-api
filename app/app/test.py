from django.test import SimpleTestCase
from app.calc import add_two_numbers


class CalcTestView(SimpleTestCase):
    """Test calc module"""

    def test_calc_two_numbers(self):
        """Add two numbers together"""
        res = add_two_numbers(10, 11)

        self.assertEqual(res, 21)

    def test_calc_subtract(self):
        """Subtract two number"""
        res = self
