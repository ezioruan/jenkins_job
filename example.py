#!/usr/bin/env python
# coding=utf-8
"""
Filename:       example.py
Last modified:  2016-05-30 16:26

Description:

"""
import jenkins
import setting
import os
import apk


if __name__ == "__main__":
    jk = jenkins.Jenkins(setting.JK_URL, auth=( setting.USERNAME, setting.PASSWORD))
    for build in jk.get_all_last_success_build():
        download_url = build.get('download_url')
        change_log = build.get('change_log')
        file_name = build.get('file_name')
        file_path = os.path.join(setting.upload_dir, file_name)
        if not os.path.exists(file_path):
            print 'file not exists...... download (%s) %s now ..........\n' % (build.get('file_size'),file_path)
            jk.download(download_url, file_path)
        try:
            apk_info = apk.get_apk_info(file_path)
        except Exception, e:
            print 'run appt error %s' % e
            print 'file maybe invalid ...... '
            os.remove(file_path)
        apk_info.update(
            {"file_path": file_path, "change_log": change_log})
        print apk_info
