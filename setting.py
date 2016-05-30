#!/usr/bin/env python
# coding=utf-8
"""
Filename:       setting.py
Last modified:  2016-05-30 16:20

Description:
"""

import os
root_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(root_dir, "download")
if not os.path.exists(download_dir):
    os.mkdir(download_dir)

#your jk url
JK_URL = "your.domain.jk.com"
USERNAME = 'username'
PASSWORD = 'password'

