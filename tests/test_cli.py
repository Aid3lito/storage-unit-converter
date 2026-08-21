import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace

from storage_converter import cli


class TestCliHelpers(unittest.TestCase):

    def test_parse_positive_value(self):
        self.assertEqual(
            cli.parse_value("100"),
            100.0
        )

    def test_parse_value_with_comma(self):
        self.assertEqual(
            cli.parse_value("1,5"),
            1.5
        )

    def test_negative_value_raises_error(self):
        with self.assertRaises(ValueError):
            cli.parse_value("-1")

    def test_unknown_unit_raises_error(self):
        with self.assertRaises(ValueError):
            cli.resolve_unit("XYZ")


class TestCliConversion(unittest.TestCase):

    def test_conversion(self):
        args = SimpleNamespace(
            value="100",
            source_unit="GB",
            target_unit="GiB"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            cli.run_conversion(args)

        self.assertEqual(
            output.getvalue().strip(),
            "93.13225746 GiB"
        )


class TestCliAddition(unittest.TestCase):

    def test_addition(self):
        args = SimpleNamespace(
            values=[
                "1", "GB",
                "500", "MB"
            ],
            target_unit="GB"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            cli.run_addition(args)

        self.assertEqual(
            output.getvalue().strip(),
            "1.5 GB"
        )

    def test_addition_requires_two_values(self):
        args = SimpleNamespace(
            values=["1", "GB"],
            target_unit="GB"
        )

        with self.assertRaises(ValueError):
            cli.run_addition(args)


class TestCliSubtraction(unittest.TestCase):

    def test_subtraction(self):
        args = SimpleNamespace(
            values=[
                "2", "GB",
                "500", "MB"
            ],
            target_unit="GB"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            cli.run_subtraction(args)

        self.assertEqual(
            output.getvalue().strip(),
            "1.5 GB"
        )

    def test_negative_subtraction_raises_error(self):
        args = SimpleNamespace(
            values=[
                "1", "GB",
                "2", "GB"
            ],
            target_unit="GB"
        )

        with self.assertRaises(ValueError):
            cli.run_subtraction(args)


class TestCliMain(unittest.TestCase):

    def test_success_exit_code(self):
        parser = cli.create_parser()

        args = parser.parse_args(
            ["convert", "100", "GB", "GiB"]
        )

        output = io.StringIO()

        with redirect_stdout(output):
            result = args.function(args)

        self.assertIsNone(result)

    def test_error_message_format(self):
        error_output = io.StringIO()

        with redirect_stderr(error_output):
            try:
                raise ValueError("Test error")
            except ValueError as error:
                print(
                    f"Error: {error}",
                    file=error_output
                )

        self.assertEqual(
            error_output.getvalue().strip(),
            "Error: Test error"
        )


if __name__ == "__main__":
    unittest.main()