from setuptools import setup, find_packages

setup(
    name="echo",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "scikit-learn>=1.0.2",
        "pandas>=1.4.0",
        "requests>=2.27.1",
        "click>=8.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        'console_scripts': [
            'echo=echo.cli:cli',
        ],
    },
    python_requires=">=3.8",
)