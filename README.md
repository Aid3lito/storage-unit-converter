# Storage Unit Converter

[![Tests](https://github.com/Aid3lito/storage-unit-converter/actions/workflows/tests.yml/badge.svg)](https://github.com/Aid3lito/storage-unit-converter/actions/workflows/tests.yml)

A lightweight storage unit converter for desktop and command-line use.

Built with Python and Tkinter, Storage Unit Converter provides both a graphical interface and a command-line interface for converting, adding, and subtracting decimal and binary storage values.

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

## Supported Platforms

Storage Unit Converter supports:

- macOS Intel (`x86_64`)
- macOS Apple Silicon (`arm64`)
- Windows 64-bit (`x86_64`)
- Linux 64-bit (`x86_64`)

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

## Requirements for Source Installation

- Python 3.9 or later
- Tkinter

Tkinter is included with most standard Python installations.
On some Linux distributions, it may need to be installed separately.

## Installation

### Pre-built releases

Pre-built desktop applications for supported platforms are available through GitHub Releases.

### From source

Clone the repository:

```bash
git clone https://github.com/Aid3lito/storage-unit-converter.git
cd storage-unit-converter
```

Install the project:

```bash
python3 -m pip install -e .
```

## Usage

### Desktop application

For command-line usage, see the [Command-Line Interface](#command-line-interface) section below.

```bash
python3 -m storage_converter.app
```

### Conversion

1. Select **Conversion**.
2. Enter a value.
3. Select the source unit.
4. Select the desired result unit.
5. Click **Calculate**.

### Addition and Subtraction

1. Select **Addition** or **Subtraction**.
2. Enter at least two values.
3. Select a unit for each value.
4. Add additional input fields if necessary.
5. Select the desired result unit.
6. Click **Calculate**.

## Project Structure

```text
storage-unit-converter/
├── .github/
│   └── workflows/
│       ├── build.yml
│       └── tests.yml
├── assets/
│   ├── icons/
│   │   ├── app-icon.png
│   │   ├── app-icon.icns
│   │   └── app-icon.ico
│   └── screenshots/
│       └── storage-unit-converter.png
├── packaging/
│   └── launcher.py
├── src/
│   └── storage_converter/
│       ├── __init__.py
│       ├── app.py
│       ├── cli.py
│       ├── converter.py
│       ├── units_binary.json
│       └── units_decimal.json
├── tests/
│   ├── test_cli.py
│   └── test_converter.py
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── pyproject.toml
├── storage-unit-converter-linux.spec
├── storage-unit-converter-macos.spec
└── storage-unit-converter-windows.spec
```

## Command-Line Interface

Storage Unit Converter also provides a command-line interface.

The full command is:

```bash
storage-unit-converter
```
A shorter command is also available:

```bash
suc
```
### Convert

```bash
suc convert 100 GB GiB
```
Example output:

```bash
93.13225746 GiB
```
### Addition and Subtraction

```bash
suc add 1 GB 500 MB --to GB
suc subtract 2 GB 500 MB --to GB
```

Example output:

```bash
1.5 GB
1.5 GB
```

### Help

```bash
suc --help
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

Run the CLI:

```bash
suc --help
```

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```


## Releases

Pre-built desktop releases are available through GitHub Releases for:

- macOS Intel (`x86_64`)
- macOS Apple Silicon (`arm64`)
- Windows 64-bit (`x86_64`)
- Linux 64-bit (`x86_64`)

## Contributing

Contributions are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting an issue or pull request.

## Security

Please refer to [SECURITY.md](SECURITY.md) for information about reporting security issues.

## License

See the [LICENSE](LICENSE) file for licensing information.