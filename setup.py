from setuptools import setup

requirements = ["requests", "bs4", "lxml"]

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="arubabank",
    version="0.0.1",
    description="Aruba Bank API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orson1282/arubabank_api",
    author="Orson Oehlers",
    author_email="orson@oehlers.net",
    packages=["arubabank"],
    install_requires=requirements,
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        
    ],
)