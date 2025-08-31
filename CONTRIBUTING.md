# Contributing to DevStress

Thank you for your interest in contributing to DevStress! We love your input and appreciate any contributions.

## Ways to Contribute

- **Report bugs** - Help us identify and fix issues
- **Suggest features** - Share ideas for new functionality
- **Submit pull requests** - Implement features or fix bugs
- **Improve documentation** - Help make DevStress easier to use
- **Share feedback** - Tell us about your experience

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/devstress.git
cd devstress
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

5. Run tests:
```bash
pytest
```

## Pull Request Process

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test thoroughly
3. Format your code:
```bash
black devstress.py
```

4. Run tests:
```bash
pytest
```

5. Commit your changes with a descriptive message
6. Push to your fork and submit a pull request

## Code Style

- Follow PEP 8
- Use black for formatting
- Add type hints where possible
- Write clear, descriptive variable names
- Add docstrings to functions and classes

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test edge cases and error conditions

## Questions?

Feel free to open an issue for any questions or discussions!