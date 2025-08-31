#!/usr/bin/env python3
"""
DevStress - Zero-Config Load Testing for Developers
Setup configuration for PyPI distribution
"""

from setuptools import setup
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devstress",
    version="1.0.0",
    author="DevStress Contributors",
    author_email="hello@devstress.dev",
    description="Zero-Config Load Testing for Developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devstress/devstress",
    py_modules=["devstress"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Benchmark",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devstress=devstress:main",
        ],
    },
    keywords="load testing, performance testing, api testing, stress testing, http, benchmark, developer tools",
    project_urls={
        "Bug Reports": "https://github.com/devstress/devstress/issues",
        "Source": "https://github.com/devstress/devstress",
        "Documentation": "https://devstress.dev",
    },
    zip_safe=False,
)