#!/usr/bin/env python
# coding=utf-8
"""
Filename:       apk.py
Last modified:  2016-05-23 14:28

Description:

"""
import os


def get_apk_info(apk_path):
    cmd = """
    aapt dump badging %s | grep package:\ name
    """ % apk_path
    out_put = os.popen(cmd).read()
    tuple_info = out_put.split(":")[1]
    tuples = tuple_info.split(" ")
    return {info.split("=")[0]: info.split("=")[1].replace("'", "") for info in tuples[1:]}


if __name__ == "__main__":
    for dirpath, dirnames, filenames in os.walk("./upload//"):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            print filepath
            print get_apk_info(filepath)
