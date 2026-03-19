# Contributing to Clawland Kits

Thank you for your interest in contributing to Clawland Kits! Every contribution helps build a stronger open hardware ecosystem for edge AI monitoring.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/clawland-kits.git
   cd clawland-kits
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-contribution
   ```
4. **Make your changes** and test them
5. **Commit** with clear messages
6. **Push** to your fork and open a Pull Request

## 📁 Repository Structure

```
clawland-kits/
├── kits/
│   ├── dc-guardian/      # Datacenter monitoring kit
│   ├── aqua-watch/       # Aquaculture monitoring kit
│   └── green-thumb/      # Greenhouse monitoring kit
├── docs/                  # Shared documentation
├── scripts/               # Build and utility scripts
└── CONTRIBUTING.md        # This file
```

Each kit directory contains:
- `README.md` - Overview, use case, ROI calculation
- `BOM.md` - Complete parts list with purchase links
- `WIRING.md` - Connection diagram
- `drivers/` - Sensor driver code
- `skill.yaml` - PicClaw skill configuration
- `alerts.yaml` - Alert thresholds

## 🛠️ Development Guidelines

### Code Style

- **Python drivers**: Follow PEP 8, use type hints where possible
- **YAML configs**: Use consistent indentation (2 spaces)
- **Documentation**: Write clear README files with practical examples

### Testing

Before submitting:
- [ ] Test driver code with actual hardware (if applicable)
- [ ] Verify BOM links are valid and prices are current
- [ ] Check wiring diagrams for accuracy
- [ ] Ensure skill.yaml loads without errors

### Documentation

Good documentation is critical for hardware projects:
- Include clear photos or diagrams
- List all tools needed for assembly
- Provide troubleshooting tips
- Add safety warnings where applicable

## 📝 Pull Request Guidelines

### PR Title Format

```
<type>: <description>

Examples:
- feat: Add Cold Chain monitoring kit
- fix: Correct DHT22 wiring diagram
- docs: Update BOM prices for dc-guardian
- test: Add driver tests for soil sensor
```

### PR Checklist

- [ ] Link to related issue (if applicable)
- [ ] Describe what changes you made
- [ ] Include photos/test results for hardware changes
- [ ] Update README if adding new features
- [ ] Test your changes locally

## 🏷️ Bounty Information

This repository participates in the **RustChain Bounty Program**!

- **CONTRIBUTING.md tasks**: 1 RTC (~$0.10 USD)
- **New kit submissions**: 10-50 RTC depending on complexity
- **Driver improvements**: 5-25 RTC
- **Documentation fixes**: 1-5 RTC

**Payment wallet**: Contributions are paid in RTC tokens to your RustChain wallet upon PR merge.

First time? Comment on your PR with your wallet address:
```
RTC wallet: <your-rtc-address>
```

## 💬 Getting Help

- **GitHub Issues**: For bugs, feature requests, questions
- **Discord**: [RustChain Discord](https://discord.gg/VqVVS2CW9Q)
- **Documentation**: [RustChain Docs](https://github.com/Scottcjn/RustChain)

## 📜 Code of Conduct

- Be respectful and inclusive
- Help newcomers learn
- Give constructive feedback
- Credit original authors and sources

## 🎯 Contribution Ideas

Not sure where to start? Here are some ideas:

1. **Add a new kit**: Design a sensor kit for a new use case
2. **Improve BOM**: Update prices, add alternative suppliers
3. **Better diagrams**: Create clearer wiring diagrams
4. **Driver tests**: Add unit tests for sensor drivers
5. **Translations**: Translate docs to other languages
6. **Tutorials**: Write build guides or video tutorials

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as this repository (see [LICENSE](LICENSE)).

---

**Questions?** Open an issue or join the Discord! Every contribution counts. 🦞
