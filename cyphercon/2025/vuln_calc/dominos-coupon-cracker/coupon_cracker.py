#!/usr/bin/env python3

import argparse
import concurrent.futures
import random
import string
import time
from typing import List, Optional

class CouponGenerator:
    def __init__(self, format: str = "20percent"):
        self.format = format
        self.patterns = {
            "20percent": r"^[A-Z]{2}\d{4}$",
            "freedelivery": r"^FREE\d{3}$",
            "bogo": r"^BOGO[A-Z]{2}\d{2}$",
            "largepizza": r"^LARGE\d{3}[A-Z]{2}$"
        }
    
    def generate_coupon(self) -> str:
        if self.format == "20percent":
            return f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"
        elif self.format == "freedelivery":
            return f"FREE{random.randint(100, 999)}"
        elif self.format == "bogo":
            return f"BOGO{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}"
        else:  # largepizza
            return f"LARGE{random.randint(100, 999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"

def validate_coupon(coupon: str) -> bool:
    # Simulate API call with random success
    time.sleep(0.1)  # Rate limiting
    return random.random() < 0.0001  # 0.01% success rate

def main():
    parser = argparse.ArgumentParser(description="Domino's Coupon Cracker")
    parser.add_argument("--format", default="20percent", help="Coupon format to generate")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads")
    args = parser.parse_args()

    generator = CouponGenerator(args.format)
    print(f"Starting coupon generation for format: {args.format}")
    print("Press Ctrl+C to stop")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        while True:
            coupon = generator.generate_coupon()
            if validate_coupon(coupon):
                print(f"\nValid coupon found: {coupon}")
                break

if __name__ == "__main__":
    main() 