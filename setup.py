import setuptools
import pypandoc
from _version import current_version, get_remote_url


long_description = pypandoc.convert_file("README.md", 'rst')
long_description = long_description.replace(":eye:blink", "blink")

setuptools.setup(
    name = "blink-config",
    version = current_version(),
    author = "Stalin",
    description = "A hot-reload configuration dictionary",
    long_description = long_description,
    # long_description_content_type = "text/markdown",
    url = get_remote_url(),
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(exclude=('tests',)),
    python_requires = ">=3.6",
    extras_require = {
        "ini": ["configparser"],
        "toml": ["toml"],
        "xml": ["xmltodict==0.12.0"],
        "yaml": ["PyYAML"]
    }
)
