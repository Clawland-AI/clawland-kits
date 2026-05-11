#!/usr/bin/env python3
"""Minimal DHT22 smoke-test stub for DC Guardian documentation.
Replace the read_sensor function with the board-specific GPIO library in production.
"""
import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pin", required=True)
    args = parser.parse_args()
    print(json.dumps({"ok": True, "pin": args.pin, "temperature_c": 24.8, "humidity_percent": 45.2}))


if __name__ == "__main__":
    main()
