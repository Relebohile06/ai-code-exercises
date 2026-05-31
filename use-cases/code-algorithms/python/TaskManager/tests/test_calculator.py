import unittest
from calculator import calculate_compound_interest


class TestCompoundInterest(unittest.TestCase):

    def test_basic_growth(self):
        result = calculate_compound_interest(
            principal_amount=1000,
            annual_interest_rate=10,
            time_years=1
        )
        self.assertTrue(result["final_amount"] > 1000)

    def test_no_interest_no_growth(self):
        result = calculate_compound_interest(
            principal_amount=1000,
            annual_interest_rate=0,
            time_years=1
        )
        self.assertEqual(result["final_amount"], 1000)

    def test_additional_contributions(self):
        result = calculate_compound_interest(
            principal_amount=1000,
            annual_interest_rate=10,
            time_years=2,
            additional_amount=100
        )
        self.assertGreater(result["final_amount"], 1100)

    def test_interest_is_calculated(self):
        result = calculate_compound_interest(
            principal_amount=1000,
            annual_interest_rate=5,
            time_years=1
        )
        self.assertIn("interest_earned", result)
        self.assertGreater(result["interest_earned"], 0)


if __name__ == "__main__":
    unittest.main()
