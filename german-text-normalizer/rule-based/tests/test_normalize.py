import unittest
from src.normalize import Normalizer
import os

class TestNormalizer(unittest.TestCase):
    def setUp(self):
        rules_file = os.path.join("..", "data", "normalization_rules.txt")
        self.normalizer = Normalizer(rules_file)

    def test_basic_normalization(self):
        self.assertEqual(
            self.normalizer.normalize("ich bin muede"),
            "Ich bin müde"
        )

    def test_no_rule(self):
        self.assertEqual(
            self.normalizer.normalize("hallo"),
            "hallo"
        )

if __name__ == "__main__":
    unittest.main()
