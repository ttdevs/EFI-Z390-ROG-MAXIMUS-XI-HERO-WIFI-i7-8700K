#!/usr/bin python3
# coding:utf-8

import os
import requests
from github import Github

base_path = './OpenCore'
debug = 'DEBUG'
repo_oc = 'acidanthera/OpenCorePkg'
repo_other = [
    'acidanthera/OpenCorePkg',
    'acidanthera/WhateverGreen',
    'acidanthera/Lilu',
    'acidanthera/VirtualSMC',
    'acidanthera/AppleALC',
    'acidanthera/RTCMemoryFixup',
    'acidanthera/BrcmPatchRAM',
    'acidanthera/AirportBrcmFixup',
    'acidanthera/IntelMausi'
]

# https://github.com/settings/tokens
g = Github('ghp_4pssx')


def get_local_path(version):
    return '%s/%s/' % (base_path, version)


def get_local_file(version, name):
    return '%s/%s/%s' % (base_path, version, name)


class Downloader:
    """
    Download file
    """

    def __init__(self, file_name, file_size, file_url):
        self.name = file_name
        self.total_size = file_size
        self.url = file_url

    def download(self):
        print('%s(%d), %s' % (self.name, self.total_size, self.url))
        response = requests.get(self.url, stream=True)
        progress = 0
        with open(self.name, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024 * 1):
                fd.write(chunk)
                progress += len(chunk)
                self.show_progress(progress, self.total_size)
            fd.close()
        print('')

    @staticmethod
    def show_progress(progress, total_size):
        rate = progress / total_size
        rate_num = int(rate * 100)
        number = int(50 * rate)
        r = '\r[%s%s]%d%%' % ("#" * number, " " * (50 - number), rate_num,)
        print("\r {}".format(r), end=" ")  # \r回到行的开头


if __name__ == '__main__':
    oc_repo = g.get_repo(repo_oc)
    version_name = oc_repo.get_latest_release().title
    print('Latest version: %s' % version_name)
    path = get_local_path(version_name)
    if not os.path.exists(path):
        os.makedirs(path)
        print('Make directory: %s' % path)
    else:
        print('Version %s exist, stop.' % version_name)
        exit()
    for item in repo_other:
        repo = g.get_repo(item)
        release = repo.get_latest_release()
        for asset in release.get_assets():
            if debug in asset.name:
                Downloader(get_local_file(version_name, asset.name), asset.size, asset.browser_download_url).download()
