====================
romhacking-rss
====================

.. image:: https://img.shields.io/pypi/v/romhacking-rss.svg
        :target: https://pypi.python.org/pypi/romhacking-rss

.. image:: https://img.shields.io/travis/narfman0/romhacking-rss.svg
        :target: https://travis-ci.org/narfman0/romhacking-rss

Ingest a romhacking search topic and render as RSS.

Usage
=====

Install requirements::

    pip install -r requirements.txt

Change directory into romhacking_rss and run flask server::

    cd romhacking_rss
    FLASK_APP=romhacking.py flask run

Hit the endpoint with something like this url in your favorite browser::

    http://127.0.0.1:5000/?page=hacks&game=750&category=1&dir=1&order=Date

License
=======

Copyright (c) 2020 Jon Robison

See included LICENSE for licensing information
