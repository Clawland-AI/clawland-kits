#!/usr/bin/env python3
"""Minimal discrete sensor smoke-test stub for leak, smoke, and door inputs."""
import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pin", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    print(json.dumps({"ok": True, "pin": args.pin, "name": args.name, "active": False}))


if __name__ == "__main__":
    main()
