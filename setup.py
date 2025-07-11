from setuptools import setup, find_packages
import os

# Leer el archivo README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Leer requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sistema-inventario",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    description="Sistema de gestión de inventario con interfaz gráfica",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/sistema-inventario",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "sistema-inventario=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*.png", "*.db"],
    },
    keywords="inventario, gestión, tkinter, sqlite, pandas",
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/sistema-inventario/issues",
        "Source": "https://github.com/tu-usuario/sistema-inventario",
    },
) 