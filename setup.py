#!/usr/bin/env python3
"""Setup script for dhrupad-sah-exception-catcher."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dhrupad-sah-exception-catcher",
    version="1.0.4",
    author="Mira Sentinel Team",
    author_email="noreply@example.com",
    description="Automatically catch and report exceptions to Mira Sentinel with rich context and log integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhrupad-sah/python-exception-catcher",
    project_urls={
        "Bug Tracker": "https://github.com/dhrupad-sah/python-exception-catcher/issues",
        "Repository": "https://github.com/dhrupad-sah/python-exception-catcher",
    },
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.25.0",
        "pydantic>=2.0.0", 
        "psutil>=5.9.0",
    ],
    extras_require={
        "fastapi": ["fastapi>=0.100.0", "starlette>=0.27.0"],
        "flask": ["flask>=2.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "fastapi>=0.100.0",
            "starlette>=0.27.0",
            "flask>=2.0.0",
            "uvicorn>=0.23.0"
        ],
    },
    keywords=[
        "exception", "error-handling", "monitoring", "observability",
        "logging", "automation", "claude", "ai-fixing", "fastapi", "flask"
    ],
)