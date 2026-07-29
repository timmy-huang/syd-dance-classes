import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from helper import determine_style


class DetermineStyleTest(unittest.TestCase):
    def test_specific_styles_win_over_choreography(self):
        cases = {
            "Hip Hop Choreography": ["Hip Hop"],
            "K-Pop Choreo": ["K-Pop"],
            "Heels Choreography": ["Heels"],
            "Girls Choreo": ["Girl Style"],
            "Jazz Funk Choreography": ["Jazz"],
        }

        for class_name, expected in cases.items():
            with self.subTest(class_name=class_name):
                self.assertEqual(determine_style(class_name), expected)

    def test_choreography_is_generic_fallback(self):
        self.assertEqual(determine_style("Open Choreography"), ["Choreography"])

    def test_unknown_is_other(self):
        self.assertEqual(determine_style("Mystery Workshop"), ["Other"])


if __name__ == "__main__":
    unittest.main()
