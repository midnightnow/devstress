#!/usr/bin/env python3
"""
DevStress - Zero-Config Load Testing for Developers
Setup and installation configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from version.py
version_file = Path(__file__).parent / "devstress" / "version.py"
version_dict = {}
with open(version_file) as f:
    exec(f.read(), version_dict)
version = version_dict["__version__"]

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
with open(readme_file, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="devstress",
    version=version,
    author="HardCard Team",
    author_email="hello@devstress.com",
    description="Zero-config load testing for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devstress/devstress",
    project_urls={
        "Documentation": "https://devstress.com/docs",
        "Source": "https://github.com/devstress/devstress",
        "Tracker": "https://github.com/devstress/devstress/issues",
        "Homepage": "https://devstress.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
        "Topic :: Utilities",
    ],
    keywords="load testing, performance testing, api testing, stress testing, developer tools",
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "aiosqlite>=0.19.0",
        "psutil>=5.9.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "jinja2>=3.0.0",
        "PyYAML>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "charts": [
            "matplotlib>=3.6.0",
            "plotly>=5.0.0",
        ],
        "exports": [
            "reportlab>=4.0.0",  # PDF generation
            "openpyxl>=3.0.0",   # Excel export
        ],
    },
    entry_points={
        "console_scripts": [
            "devstress=devstress.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "devstress": [
            "templates/*.html",
            "templates/*.css",
            "templates/*.js",
            "static/*",
            "config/*.yaml",
        ],
    },
    zip_safe=False,
)