import unittest

from trabaholens.validation import validate_site_data


class ValidationTest(unittest.TestCase):
    def test_committed_site_data_is_consistent(self) -> None:
        validate_site_data()


if __name__ == "__main__":
    unittest.main()
