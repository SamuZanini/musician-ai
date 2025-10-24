"""
Setup script para o módulo de IA
Implementação simples para instalação e configuração
"""

from setuptools import setup, find_packages
import os

# Lê o README para a descrição longa
def read_readme():
    """Lê o arquivo README.md"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Módulo de IA para detecção de áudio musical"

# Lê os requisitos
def read_requirements():
    """Lê o arquivo requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="musician-ai",
    version="1.0.0",
    author="Musician AI Team",
    author_email="team@musician-ai.com",
    description="Módulo de IA para detecção de áudio musical",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/musician-ai/ia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "requests>=2.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "musician-ai-ml=ml_service:main",
            "musician-ai-tuner=tuner_service:main",
            "musician-ai-detection=detection_service:main",
            "musician-ai-run=run_services:main",
            "musician-ai-test=test_services:main",
            "musician-ai-example=example_usage:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords=[
        "music", "audio", "machine learning", "pitch detection", 
        "tuning", "musical instruments", "real-time", "websocket"
    ],
    project_urls={
        "Bug Reports": "https://github.com/musician-ai/ia/issues",
        "Source": "https://github.com/musician-ai/ia",
        "Documentation": "https://github.com/musician-ai/ia#readme",
    },
)
