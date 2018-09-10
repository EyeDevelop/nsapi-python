import setuptools
from setuptools import setup

setup(
    name="nsapi",
    version="9f9c7c0de",
    description="A Python wrapper to the NS API.",
    url="https://github.com/EyeDevelop/nsapi-python",
    author="EyeDevelop (Hans Goor)",
    license="GPLv3",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=[
        "requests",
        "bs4",
        "lxml"
    ]
)
