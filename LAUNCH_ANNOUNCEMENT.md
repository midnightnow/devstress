# 🚀 DevStress is LIVE!

**Zero-Config Load Testing for Developers**

After getting frustrated with complex load testing setups, I built DevStress - a tool that lets you load test your API in 30 seconds with zero configuration.

## 🎯 The Problem
Every developer knows they should load test their APIs, but:
- JMeter requires learning a whole ecosystem
- Cloud services want your credit card
- Even "simple" tools need YAML configs
- Result: We ship untested

## ✨ The Solution
```bash
pip install devstress
devstress https://api.example.com
```

That's it. You're load testing.

## 🔥 Features
- **Zero Configuration** - No YAML, no Docker, no cloud accounts
- **Instant Results** - Live progress bar, detailed metrics
- **Smart Defaults** - Automatically detects system capacity
- **Beautiful Reports** - HTML reports with charts
- **CI/CD Ready** - Exit codes for automation

## 📊 Real Performance
- **28.6 requests/second** with 200 concurrent users
- **6x faster** than sequential curl loops
- **Minimal resource usage** (<10% CPU, <100MB RAM)
- **Linear scaling** up to system limits

## 🛠️ Examples

```bash
# Basic test
devstress https://api.example.com

# Custom parameters
devstress https://api.example.com --users 500 --duration 60

# Rate limiting
devstress https://api.example.com --rps 100

# Different scenarios
devstress https://api.example.com --scenario ramp
```

## 🔗 Links
- **GitHub**: https://github.com/midnightnow/devstress
- **PyPI**: https://pypi.org/project/devstress
- **Documentation**: https://github.com/midnightnow/devstress#readme

## 🎯 Who It's For
- Developers who want to test APIs without the complexity
- Teams needing quick performance validation
- CI/CD pipelines requiring simple load testing
- Anyone tired of overcomplicated tools

## 💭 Philosophy
Load testing shouldn't require a PhD in distributed systems. DevStress follows the Unix philosophy: do one thing well. It load tests HTTP endpoints. That's it.

## 🚀 Try It Now
```bash
pip install devstress
devstress https://httpbin.org/get --users 50 --duration 10
```

In 30 seconds, you'll have results.

## 🤝 Contributing
DevStress is open source and welcomes contributions! Check out the GitHub repo for issues and roadmap.

---

**Built with ❤️ for developers who value their time**

*From complex multiagent systems to simple developer tools - sometimes the best solutions are the simplest ones.*