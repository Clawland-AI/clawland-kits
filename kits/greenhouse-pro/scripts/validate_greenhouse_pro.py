from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "BOM.md",
    "WIRING.md",
    "skill.yaml",
    "alerts.yaml",
    "test-report.md",
    "enclosure/greenhouse-pro-enclosure.scad",
    "drivers/soil_moisture.py",
    "drivers/bme280_reader.py",
    "drivers/bh1750_reader.py",
    "drivers/scd41_reader.py",
    "drivers/ds18b20_leaf.py",
]

REQUIRED_SKILL_TERMS = [
    "greenhouse-pro",
    "air_temperature_c",
    "soil_moisture_pct",
    "light_lux",
    "co2_ppm",
    "fan.on",
    "irrigation_pump",
    "daily",
]

REQUIRED_DOC_TERMS = [
    "Bill of Materials",
    "ASCII Wiring Diagram",
    "3D-printable",
    "Sample Readings",
]


def fail(message):
    print(f"greenhouse-pro validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


for relative in REQUIRED_FILES:
    path = ROOT / relative
    if not path.exists():
        fail(f"missing {relative}")
    if path.stat().st_size == 0:
        fail(f"{relative} is empty")

skill = (ROOT / "skill.yaml").read_text(encoding="utf-8")
for term in REQUIRED_SKILL_TERMS:
    if term not in skill:
        fail(f"skill.yaml missing {term}")

combined_docs = "\n".join(
    (ROOT / name).read_text(encoding="utf-8")
    for name in ["README.md", "BOM.md", "WIRING.md", "test-report.md"]
)
for term in REQUIRED_DOC_TERMS:
    if term not in combined_docs:
        fail(f"documentation missing {term}")

print("greenhouse-pro validation ok")

