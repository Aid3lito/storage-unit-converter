# Storage Unit Converter

[![Tests](https://github.com/Aid3lito/storage-unit-converter/actions/workflows/tests.yml/badge.svg)](https://github.com/Aid3lito/storage-unit-converter/actions/workflows/tests.yml)

A lightweight desktop application for converting and calculating decimal and binary storage units.

Built with Python and Tkinter, Storage Unit Converter provides a simple graphical interface for converting, adding, and subtracting storage values across common decimal and binary units.

## Features

- Convert between decimal and binary storage units
- Add multiple storage values using different units
- Subtract multiple storage values using different units
- Dynamically add or remove input fields
- Choose the desired output unit
- Automatic formatting of large and small numbers
- Scientific notation for very small values
- Calculation history
- Copy results to the clipboard
- Reset the interface instantly
- Keyboard support with the Enter key
- No external runtime dependencies

## Supported Units

### Decimal units

- Byte (B)
- Kilobyte (KB)
- Megabyte (MB)
- Gigabyte (GB)
- Terabyte (TB)
- Petabyte (PB)
- Exabyte (EB)

### Binary units

- Byte (B)
- Kibibyte (KiB)
- Mebibyte (MiB)
- Gibibyte (GiB)
- Tebibyte (TiB)
- Pebibyte (PiB)
- Exbibyte (EiB)

## Screenshot

![Storage Unit Converter](assets/screenshots/storage-unit-converter.png)

## Requirements

- Python 3.9 or later
- Tkinter

Tkinter is included with most standard Python installations.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd storage-unit-converter
```

Install the project in editable mode:

```bash
python3 -m pip install -e .
```

## Usage

Run the application with:

```bash
python3 -m storage_converter.app
```

### Conversion

1. Select **Conversion**.
2. Enter a value.
3. Select the source unit.
4. Select the desired result unit.
5. Click **Calculate**.

### Addition and subtraction

1. Select **Addition** or **Subtraction**.
2. Enter at least two values.
3. Select a unit for each value.
4. Add additional input fields if necessary.
5. Select the desired result unit.
6. Click **Calculate**.

## Project Structure

```text
storage-unit-converter/
├── assets/
├── src/
│   └── storage_converter/
│       ├── __init__.py
│       ├── app.py
│       ├── converter.py
│       ├── units_binary.json
│       └── units_decimal.json
├── tests/
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

## Development

Install the project in editable mode:

```bash
python3 -m pip install -e .
```

Then launch the application:

```bash
python3 -m storage_converter.app
```

## Releases

Pre-built desktop releases for supported operating systems will be distributed through GitHub Releases.

## Contributing

Contributions are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting an issue or pull request.

## Security

Please refer to [SECURITY.md](SECURITY.md) for information about reporting security issues.

## License

See the [LICENSE](LICENSE) file for licensing information.