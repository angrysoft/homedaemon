#!/usr/bin/env python3

import unittest
import requests


class MyTestCase(unittest.TestCase):
    def test_buttons(self):
        """setUp(self):"""
        l = {'1': 'off', '2': 'on'}
        req = requests.post('http://127.0.0.1:5000/buttons', params=l)
        print(req.url)
        print(req.text)

    def test_colors(self):
        l = {'RGB': '255.0.0', 'name': 'alice blue'}
        req = requests.post('http://127.0.0.1:5000/led', params=l)
        print(req.url)
        print(req.text)


if __name__ == '__main__':
    unittest.main()