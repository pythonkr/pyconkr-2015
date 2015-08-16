# -*- coding: utf-8 -*-

from django.test import TestCase
from django.http import HttpResponse

from pyconkr.helper import render_io_error


class HelperFunctionTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_render_io_error(self):
        a = render_io_error("test reason")
        self.assertEqual(a.status_code, 406, "render io error status code must be 406")



