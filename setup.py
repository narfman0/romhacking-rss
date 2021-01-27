from setuptools import setup, find_packages
from romhacking_rss import __version__ as version


setup(
    name="romhacking-rss",
    version=version,
    description=("Ingest a romhacking search topic and render as RSS"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="romhacking rss atom flask",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    url="https://github.com/narfman0/romhacking-rss",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["beautifulsoup4", "Werkzeug==0.16.0", "flask", "requests"],
    tests_require=["tox", "coverage", "flake8", "wheel"],
    test_suite="tests",
    entry_points={
        "console_scripts": ["romhacking_rss=romhacking_rss.cli:main"],
    },
)
