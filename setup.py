import setuptools
import subprocess

from setuptools import setup


def get_version():
    s = subprocess.check_output(["git", "describe", "--always"]).decode("utf-8").strip()
    return s


setup(
    name="nsapi",
    version=get_version(),
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
