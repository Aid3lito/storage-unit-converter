import argparse
import sys

from . import converter


# ==============================
# CONSTANTS
# ==============================

EXIT_SUCCESS = 0
EXIT_ERROR = 1


# ==============================
# HELPERS
# ==============================

def resolve_unit(unit):
    resolved_unit = converter.trouver_unite(unit)

    if resolved_unit == "Impossible !":
        raise ValueError(f"Unknown unit: {unit}")

    return resolved_unit


def parse_value(value):
    try:
        number = float(value.replace(",", "."))
    except ValueError as exc:
        raise ValueError(
            f"Invalid value: {value}"
        ) from exc

    if number < 0:
        raise ValueError(
            "Negative values are not allowed."
        )

    return number


def format_number(number):
    if number == 0:
        return "0"

    absolute_value = abs(number)

    if absolute_value < 0.0001:
        return f"{number:.6e}"

    if number.is_integer():
        return f"{int(number):,}"

    text = f"{number:,.8f}"
    return text.rstrip("0").rstrip(".")


def get_acronym(unit):
    return converter.toutes_les_units[unit]["acronyme"]


# ==============================
# OPERATIONS
# ==============================

def run_conversion(args):
    value = parse_value(args.value)

    source_unit = resolve_unit(args.source_unit)
    target_unit = resolve_unit(args.target_unit)

    result = converter.convertir(
        value,
        source_unit,
        target_unit
    )

    print(
        f"{format_number(result)} "
        f"{get_acronym(target_unit)}"
    )


def parse_calculation_values(values):
    if len(values) < 4:
        raise ValueError(
            "At least two values and their units are required."
        )

    if len(values) % 2 != 0:
        raise ValueError(
            "Each value must be followed by a unit."
        )

    parsed_values = []

    for index in range(0, len(values), 2):
        value = parse_value(values[index])
        unit = resolve_unit(values[index + 1])

        parsed_values.append(
            (value, unit)
        )

    return parsed_values


def run_addition(args):
    target_unit = resolve_unit(args.target_unit)
    values = parse_calculation_values(args.values)

    result = 0

    for value, unit in values:
        result += converter.convertir(
            value,
            unit,
            target_unit
        )

    print(
        f"{format_number(result)} "
        f"{get_acronym(target_unit)}"
    )


def run_subtraction(args):
    target_unit = resolve_unit(args.target_unit)
    values = parse_calculation_values(args.values)

    first_value, first_unit = values[0]

    result = converter.convertir(
        first_value,
        first_unit,
        target_unit
    )

    for value, unit in values[1:]:
        result -= converter.convertir(
            value,
            unit,
            target_unit
        )

    if result < 0:
        raise ValueError(
            "Operation impossible: the result cannot be negative."
        )

    print(
        f"{format_number(result)} "
        f"{get_acronym(target_unit)}"
    )


# ==============================
# ARGUMENT PARSER
# ==============================

def create_parser():
    parser = argparse.ArgumentParser(
        prog="storage-unit-converter",
        description=(
            "Convert, add, and subtract "
            "decimal and binary storage units."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )


    # Conversion

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert a storage value."
    )

    convert_parser.add_argument(
        "value",
        help="Value to convert."
    )

    convert_parser.add_argument(
        "source_unit",
        help="Source storage unit."
    )

    convert_parser.add_argument(
        "target_unit",
        help="Target storage unit."
    )

    convert_parser.set_defaults(
        function=run_conversion
    )


    # Addition

    add_parser = subparsers.add_parser(
        "add",
        help="Add storage values."
    )

    add_parser.add_argument(
        "values",
        nargs="+",
        help="Pairs of values and units."
    )

    add_parser.add_argument(
        "--to",
        dest="target_unit",
        required=True,
        help="Result unit."
    )

    add_parser.set_defaults(
        function=run_addition
    )


    # Subtraction

    subtract_parser = subparsers.add_parser(
        "subtract",
        help="Subtract storage values."
    )

    subtract_parser.add_argument(
        "values",
        nargs="+",
        help="Pairs of values and units."
    )

    subtract_parser.add_argument(
        "--to",
        dest="target_unit",
        required=True,
        help="Result unit."
    )

    subtract_parser.set_defaults(
        function=run_subtraction
    )

    return parser


# ==============================
# MAIN
# ==============================

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        args.function(args)

    except ValueError as error:
        print(
            f"Error: {error}",
            file=sys.stderr
        )

        return EXIT_ERROR

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())