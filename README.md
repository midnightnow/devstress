# 🚀 DevStress

**Zero-Config Load Testing for Developers**

Load test your API in 30 seconds. No setup, no configuration files, no cloud accounts. Just run and get results.

[![PyPI version](https://badge.fury.io/py/devstress.svg)](https://badge.fury.io/py/devstress)
[![Python](https://img.shields.io/pypi/pyversions/devstress.svg)](https://pypi.org/project/devstress/)
[![License](https://img.shields.io/pypi/l/devstress.svg)](https://github.com/midnightnow/devstress/blob/main/LICENSE)
[![CI](https://github.com/midnightnow/devstress/workflows/CI/badge.svg)](https://github.com/midnightnow/devstress/actions)
[![Downloads](https://pepy.tech/badge/devstress)](https://pepy.tech/project/devstress)

## 🏃‍♂️ Quick Start

```bash
# Install
pip install devstress

# Test any API instantly  
devstress https://api.example.com

# That's it. You're load testing.
```

## Why DevStress?

**The Problem**: You've built an API. You know you should load test it, but setting up JMeter feels like overkill, and cloud services want your credit card. So you ship it untested.

**The Solution**: DevStress. One command, instant results, zero friction.

```bash
# That's it. You're load testing.
devstress https://api.example.com
```

## ✨ Features

- **Zero Configuration** - No config files, no setup, just run
- **Instant Results** - See live progress and get detailed reports
- **Smart Defaults** - Sensible settings that just work
- **Resource Aware** - Automatically adapts to your system capacity
- **Beautiful Reports** - HTML reports with charts and insights
- **CI/CD Ready** - Exit codes for automation, JSON output available

## 🎯 Quick Start

### Install

```bash
pip install devstress
```

### Basic Usage

```bash
# Quick test with defaults (100 users, 30 seconds)
devstress https://api.example.com

# Custom test parameters
devstress https://api.example.com --users 500 --duration 60

# Rate-limited test
devstress https://api.example.com --rps 100

# Ramp-up test
devstress https://api.example.com --scenario ramp
```

### Real-World Examples

**Test your REST API:**
```bash
devstress https://api.myapp.com/users \
  --users 200 \
  --duration 60 \
  --header "Authorization: Bearer token123"
```

**Test with rate limiting:**
```bash
devstress https://api.myapp.com/search \
  --rps 50 \
  --duration 30
```

**CI/CD integration:**
```bash
# Fails if error rate > 5% or avg response > 2000ms
devstress https://staging.api.com/health || exit 1
```

## 📊 What You Get

### Live Progress
```
[████████████████████░░░░░░░░░░░░░░░░░░░] 50.0% | Requests: 5,234 | RPS: 174.5 | Errors: 0.2%
```

### Detailed Results
```
📊 Performance Metrics:
  • Total Requests: 15,234
  • Successful: 15,198
  • Failed: 36
  • Requests/Second: 507.8
  • Error Rate: 0.24%

⏱️  Response Times:
  • Average: 196ms
  • Median: 187ms
  • 95th percentile: 245ms
  • 99th percentile: 312ms

✅ Performance looks good!
```

### Beautiful HTML Reports
- Interactive charts
- Response time distribution
- Status code breakdown
- Performance insights
- Exportable results

## 🛠️ Advanced Usage

### Custom Headers
```bash
devstress https://api.example.com \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json"
```

### Different Load Patterns
```bash
# Steady load (default)
devstress https://api.example.com --scenario steady

# Ramp up gradually
devstress https://api.example.com --scenario ramp

# Spike test
devstress https://api.example.com --scenario spike
```

### System Resource Management
DevStress automatically detects your system capacity and adjusts:
- CPU cores available
- Memory constraints
- Network limitations
- Connection pool optimization

## 🔧 Installation Options

### Via pip (Recommended)
```bash
pip install devstress
```

### Via pipx (Isolated Environment)
```bash
pipx install devstress
```

### From Source
```bash
git clone https://github.com/devstress/devstress.git
cd devstress
pip install -e .
```

## 📈 Performance

DevStress is built with modern Python async/await and can generate significant load:

- **10,000+ requests/second** on modern hardware
- **1,000+ concurrent users** on a laptop
- **Minimal CPU usage** with efficient event loops
- **Smart rate limiting** to prevent self-DoS

## 🤝 Comparison

| Tool | Setup Time | Config Required | Cloud Account | Cost |
|------|-----------|-----------------|---------------|------|
| **DevStress** | 30 seconds | None | No | Free |
| JMeter | 30+ minutes | Yes | No | Free |
| BlazeMeter | 10 minutes | Yes | Yes | $$$ |
| K6 | 15 minutes | Yes | Optional | Free/$$$ |
| Locust | 20 minutes | Yes (Python) | No | Free |

## 🎯 Use Cases

- **Pre-deployment Testing** - Verify performance before shipping
- **API Development** - Test as you build
- **CI/CD Pipelines** - Automated performance gates
- **Capacity Planning** - Find your breaking point
- **Regression Testing** - Ensure performance doesn't degrade

## 🚦 CI/CD Integration

### GitHub Actions
```yaml
- name: Load Test API
  run: |
    pip install devstress
    devstress ${{ secrets.API_URL }} --users 200 --duration 60
```

### Exit Codes
- `0` - Test passed, performance good
- `1` - High error rate (>5%)
- `2` - Slow responses (>2000ms average)
- `130` - User interrupted

## 📚 Documentation

Full documentation available at [devstress.dev](https://devstress.dev)

## 🤔 FAQ

**Q: How is this different from curl in a loop?**
A: DevStress uses async I/O for true concurrency, provides detailed statistics, handles rate limiting, and generates comprehensive reports. It's the difference between a toy and a tool.

**Q: Can it test WebSockets/GraphQL/gRPC?**
A: Currently HTTP/HTTPS only. WebSocket and GraphQL support coming soon.

**Q: Does it handle authentication?**
A: Yes, via custom headers. OAuth/JWT tokens work perfectly.

**Q: Can I save test results?**
A: Yes, all reports are saved to `~/.devstress/` automatically.

## 🧑‍💻 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Setup development environment
git clone https://github.com/devstress/devstress.git
cd devstress
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black devstress.py
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

Built with:
- [aiohttp](https://github.com/aio-libs/aiohttp) - Async HTTP client
- [psutil](https://github.com/giampaolo/psutil) - System monitoring
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output

---

**Made with ❤️ for developers who value their time**

*"It's not about the load test, it's about the friends we made along the way."* - Anonymous DevOps Engineer