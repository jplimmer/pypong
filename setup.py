from setuptools import setup, find_packages

setup(
    name="pypong",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "PyYaml"
    ],
    entry_points={
        "console_scripts": [
            "pypong=pypong.__main__:main",
        ],
    },
)