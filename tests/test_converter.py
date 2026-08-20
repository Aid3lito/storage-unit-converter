import unittest

from storage_converter import converter


class TestTextNormalization(unittest.TestCase):

    def test_normalize_text(self):
        self.assertEqual(
            converter.normaliser_texte("  GiB - "),
            "gib"
        )


class TestUnitLookup(unittest.TestCase):

    def test_find_decimal_unit_by_acronym(self):
        self.assertEqual(
            converter.trouver_unite("GB"),
            "GigaByte"
        )

    def test_find_binary_unit_by_acronym(self):
        self.assertEqual(
            converter.trouver_unite("GiB"),
            "GibiByte"
        )

    def test_find_unit_case_insensitive(self):
        self.assertEqual(
            converter.trouver_unite("gigabyte"),
            "GigaByte"
        )

    def test_unknown_unit(self):
        self.assertEqual(
            converter.trouver_unite("unknown"),
            "Impossible !"
        )


class TestConversion(unittest.TestCase):

    def test_same_unit_conversion(self):
        result = converter.convertir(
            100,
            "GigaByte",
            "GigaByte"
        )

        self.assertEqual(result, 100)

    def test_gigabyte_to_gibibyte(self):
        result = converter.convertir(
            100,
            "GigaByte",
            "GibiByte"
        )

        self.assertAlmostEqual(
            result,
            93.13225746154785,
            places=8
        )

    def test_gibibyte_to_gigabyte(self):
        result = converter.convertir(
            1,
            "GibiByte",
            "GigaByte"
        )

        self.assertAlmostEqual(
            result,
            1.073741824,
            places=9
        )


class TestCalculation(unittest.TestCase):

    def test_addition(self):
        result = converter.calculer(
            1,
            "GigaByte",
            500,
            "MegaByte",
            "GigaByte",
            "+"
        )

        self.assertAlmostEqual(
            result,
            1.5,
            places=8
        )

    def test_subtraction(self):
        result = converter.calculer(
            2,
            "GigaByte",
            500,
            "MegaByte",
            "GigaByte",
            "-"
        )

        self.assertAlmostEqual(
            result,
            1.5,
            places=8
        )

    def test_negative_subtraction_returns_none(self):
        result = converter.calculer(
            1,
            "GigaByte",
            2,
            "GigaByte",
            "GigaByte",
            "-"
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()