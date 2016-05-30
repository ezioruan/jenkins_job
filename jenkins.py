#!/usr/bin/env python
# coding=utf-8
"""
Filename:       jenkins.py
Last modified:  2016-05-30 16:23

Description:

"""

import requests
from bs4 import BeautifulSoup


class Jenkins(object):

    def __init__(self, base_url, auth=None, verify_ssl_cert=True, proxies={}):
        self.base_url = base_url
        self.session = requests.session()
        self.auth = auth
        self.verify_ssl_cert = verify_ssl_cert
        self.proxies = proxies
        url = "%s/api/json" % self.base_url
        resp = self.get(url).json()
        self.jobs = resp.get('jobs', [])

    def get(self, url, *args, **kwargs):
        return self.session.get(
            url, auth=self.auth, verify=self.verify_ssl_cert, proxies=self.proxies, *args, **kwargs
        )

    def get_all_last_success_build(self):
        builds = []
        for job in self.jobs:
            builds.append(self.get_last_success_build(job["name"]))
        return builds

    def get_last_success_build(self, job_name):
        print 'job name [%s]' % job_name
        url = "%s/job/%s/lastSuccessfulBuild/" % (
            self.base_url, job_name)
        soup = BeautifulSoup(self.get(url).text, 'lxml')
        table = soup.findAll('table', 'fileList')[0]
        tds = table.findAll('td')
        download_href = tds[1].a.get('href')
        file_name = tds[1].a.text
        download_url = "%s%s" % (url, download_href)
        change_log_icon = soup.findAll("img", "icon-notepad icon-xlg")[0]
        change_log_td = change_log_icon.parent.parent.findAll('td')[1]
        change_log = change_log_td.text
        file_size = soup.findAll("td", "fileSize")[0].text
        return {"download_url": download_url,
                'file_name': file_name,
                "change_log": change_log,
                "job_name": job_name,
                "file_size": file_size,
                }

    def download(self, url, file_path, *args, **kwargs):
        print 'download %s' % url
        resp = self.get(url, stream=True, *args, **kwargs)
        if resp.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            print 'save %s ok ' % file_path
        else:
            print 'download %s error' % (url, resp.text)

