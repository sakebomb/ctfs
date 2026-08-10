# Domino's Coupon Cracker

A Python-based tool to generate and validate Domino's Pizza coupon codes. This project uses various patterns and known coupon formats to generate potential valid codes.

## Features

- Pattern-based coupon generation
- Multi-threaded validation
- Support for various coupon formats
- Rate limiting to avoid detection
- Proxy support for distributed testing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python coupon_cracker.py --format=20percent --threads=4
```

## Coupon Formats

Currently supported formats:
- 20% off orders
- Free delivery
- Buy one get one free
- Large pizza specials

## Contributing

Feel free to submit pull requests with new coupon patterns or validation methods.

## Disclaimer

This tool is for educational purposes only. Please use responsibly and respect Domino's terms of service. 