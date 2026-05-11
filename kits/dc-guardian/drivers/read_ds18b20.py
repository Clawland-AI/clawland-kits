#!/usr/bin/env python3
"""Minimal DS18B20 smoke-test stub for DC Guardian documentation."""
import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pin", required=True)
    args = parser.parse_args()
    print(json.dumps({"ok": True, "pin": args.pin, "temperature_c": 23.6}))


if __name__ == "__main__":
    main()
