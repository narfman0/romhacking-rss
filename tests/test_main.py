#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest

from romhacking_rss.main import generate_response


SMB3HAX_PATH = os.path.join(os.path.dirname(__file__), "smb3hacks.html")


class TestMain(unittest.TestCase):
    def setUp(self):
        self.html = open(SMB3HAX_PATH).read()

    def test_generate_response(self):
        response = generate_response(self.html)
        self.assertEquals(response.status_code, 200)
