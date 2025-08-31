# DevStress - Zero-Config Load Testing for Developers

![DevStress Logo](https://devstress.com/logo.png)

[![PyPI version](https://badge.fury.io/py/devstress.svg)](https://badge.fury.io/py/devstress)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/devstress/devstress/workflows/CI/badge.svg)](https://github.com/devstress/devstress/actions)

> **Load test your API in 30 seconds. No Docker, no YAML, no cloud accounts. Just results.**

DevStress is a developer-first load testing tool that eliminates the friction between "I should test this" and actually testing it. Built for the 80% of developers who skip load testing because existing tools are too complex for quick validation.

## 🎯 The Problem We Solve

Most developers fall into one of these camps:

- **"I'll use k6"** - Then spend 15 minutes writing JavaScript test scripts
- **"I'll use Locust"** - Then get distracted setting up Python classes and web UIs  
- **"I'll just ship it"** - And hope nothing breaks under load

**DevStress eliminates the middle step.** One command, instant feedback.

## ⚡ Quick Start

```bash
# Install
pip install devstress

# Test your API (uses sensible defaults: 100 users, 30s duration)
devstress test https://api.myapp.com/health

# More control
devstress test https://api.myapp.com/login \
  --users 500 \
  --duration 60 \
  --scenario spike \
  --header "Authorization: Bearer token123"
```

**That's it.** You'll get:
- Requests per second (RPS)
- Response time percentiles (p50, p95, p99)  
- Error rate and status code breakdown
- Beautiful HTML report automatically opened in your browser

## 🏗️ Architecture

DevStress is built on Python's `asyncio` with carefully optimized connection pooling:

```
CLI Command → DevStressEngine → N async agents → Target API
     ↓              ↓                ↓               ↓
Live Dashboard ← Metrics Collector ← HTTP Responses ← Your Server
```

**Key Features:**
- **Async-first**: Uses `aiohttp` for true concurrent connections
- **Resource-aware**: Automatically scales based on your system capabilities
- **Real-time monitoring**: Live web dashboard at `http://localhost:8890`
- **Smart defaults**: Works out of the box, but configurable when needed
- **CI/CD ready**: Exit codes and JUnit XML for automated testing

## 📊 Load Testing Scenarios

### Steady Load (Default)
```bash
devstress test https://api.example.com --scenario steady
```
Maintains consistent user count throughout the test.

### Spike Testing
```bash
devstress test https://api.example.com --scenario spike --users 1000
```
Immediately hits your API with full load to test burst capacity.

### Ramp Testing
```bash
devstress test https://api.example.com --scenario ramp --duration 120
```
Gradually increases load over 30% of test duration, then sustains.

## 🎨 Reports & Integration

### HTML Reports
Every test generates a beautiful, shareable HTML report:
- Performance charts with Chart.js
- Detailed metrics breakdown
- System resource usage
- Comparative analysis with previous runs

### CI/CD Integration
```yaml
# .github/workflows/performance.yml
- name: Performance Test
  run: |
    devstress test ${{ env.STAGING_URL }} \
      --users 200 \
      --duration 45 \
      --export junit
```

DevStress returns appropriate exit codes:
- `0`: Test passed (error rate <5%, avg response <2s)
- `1`: Test failed performance thresholds  
- `130`: Test interrupted by user

### Export Formats
- **HTML**: Rich dashboard with interactive charts
- **JSON**: Machine-readable metrics for further processing
- **Markdown**: Perfect for GitHub PR comments
- **JUnit XML**: For CI/CD integration

## 🔧 Configuration

### Environment Variables
```bash
export DEVSTRESS_DEFAULT_USERS=100
export DEVSTRESS_DEFAULT_DURATION=30
export DEVSTRESS_RESULTS_DIR=~/.devstress/results
```

### Config File
Create `~/.devstress/config.yaml`:
```yaml
defaults:
  users: 150
  duration: 45
  timeout: 10

thresholds:
  max_error_rate: 5.0      # Percent
  max_avg_response: 2000   # Milliseconds
  max_p95_response: 5000   # Milliseconds

reports:
  auto_open: true
  export_formats: ["html", "json"]
```

## 🚀 Advanced Usage

### Custom Headers & Authentication
```bash
# API Key authentication
devstress test https://api.example.com/protected \
  --header "X-API-Key: your-key-here"

# Bearer token
devstress test https://api.example.com/graphql \
  --header "Authorization: Bearer eyJ0eXAi..."

# Multiple headers
devstress test https://api.example.com/api \
  --header "Accept: application/json" \
  --header "User-Agent: DevStress/1.0"
```

### Performance Thresholds
```bash
# Fail if error rate >1% or avg response >500ms
devstress test https://api.example.com \
  --max-error-rate 1.0 \
  --max-response-time 500
```

### Historical Comparison
```bash
# Compare against previous test
devstress test https://api.example.com --compare-previous

# Compare against specific baseline
devstress test https://api.example.com --compare-baseline baseline-v1.2.3
```

## 📈 Performance Characteristics

**Tested on Mac Studio (M2 Ultra, 128GB RAM):**
- Maximum concurrent users: **2000+** 
- Sustained throughput: **~180 RPS** (target-dependent)
- Memory usage: **~1MB per 100 concurrent users**
- CPU usage: **~20% at 500 concurrent users**

**Single-machine limitations:**
- Bound by system file descriptor limits (`ulimit -n`)
- Network interface bandwidth
- Target server capacity

**When to use distributed tools instead:**
- Need >5000 concurrent users
- Multi-region load simulation
- Complex multi-step user journeys
- Long-running soak tests (>1 hour)

## 🆚 Comparison with Alternatives

| Feature | DevStress | k6 | Locust | Artillery |
|---------|-----------|----|---------| ----------|
| Setup time | **30 seconds** | 10-15 minutes | 15-30 minutes | 5-10 minutes |
| Configuration | **Zero** | JavaScript | Python classes | YAML |
| Built-in dashboard | **✅ Auto-opens** | Cloud only | ✅ Web UI | ❌ |
| CI/CD integration | **✅ Templates** | Manual setup | Manual setup | ✅ |
| Learning curve | **Zero** | Medium | Medium | Low |
| Cost | **Free** | Free (Cloud paid) | Free | Free |
| Best for | **Quick validation** | Complex scenarios | Python shops | Node.js teams |

## 🛣️ Roadmap

### v1.1 - Enhanced Reporting
- [ ] PDF export for formal reports
- [ ] Slack/Discord webhook integration
- [ ] Performance regression detection
- [ ] Baseline management system

### v1.2 - Advanced Scenarios  
- [ ] Multi-endpoint testing
- [ ] WebSocket support
- [ ] Custom request bodies (POST/PUT/PATCH)
- [ ] Cookie/session handling

### v1.3 - Team Features
- [ ] Shared baselines across team members
- [ ] Performance budgets and alerts
- [ ] Integration with monitoring systems
- [ ] Multi-machine coordination (beta)

### v2.0 - DevStress Pro
- [ ] Historical performance database
- [ ] Advanced CI/CD integrations
- [ ] SSO and team management
- [ ] Enterprise support options

## 🤝 Contributing

We welcome contributions! DevStress is built to be simple but extensible.

**Getting started:**
1. Fork the repository
2. Install development dependencies: `pip install -e .[dev]`
3. Run tests: `pytest`
4. Submit a pull request

**Areas where we need help:**
- Additional export formats (CSV, InfluxDB, Prometheus)
- CI/CD integration templates (GitLab CI, Jenkins, etc.)
- Performance optimizations for high-concurrency scenarios
- Documentation and tutorials

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙋‍♀️ Support

- **Documentation**: [devstress.com/docs](https://devstress.com/docs)
- **Issues**: [GitHub Issues](https://github.com/devstress/devstress/issues)
- **Discussions**: [GitHub Discussions](https://github.com/devstress/devstress/discussions)
- **Email**: [hello@devstress.com](mailto:hello@devstress.com)

---

**Built with ❤️ for developers who ship with confidence.**