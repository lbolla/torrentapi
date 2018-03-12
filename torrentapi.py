#!/usr/bin/env python3
import sys
import requests


URL = 'https://torrentapi.org/pubapi_v2.php'


class TorrentAPI:

    def __init__(self, url=URL):
        self._url = url
        self._session = requests.Session()
        self._token = None

    @property
    def token(self):
        if self._token is None:
            self._token = self.get_token()
        return self._token

    def get_token(self):
        rs = self._session.get(self._url, params={
            'get_token': 'get_token',
        })
        rs.raise_for_status()
        return rs.json()['token']

    def search(self, q):
        params = {
            'mode': 'search',
            'format': 'json_extended',
            'sort': 'seeders',
            'search_string': q,
            'token': self.token,
        }
        rs = self._session.get(self._url, params=params)
        rs.raise_for_status()
        return rs.json()


def main():
    what = ' '.join(sys.argv[1:])
    c = TorrentAPI()
    torrents = c.search(what)
    if 'error' in torrents:
        print('Nothing!')
        sys.exit(1)

    nresults = 10
    for itorrent, torrent in enumerate(torrents['torrent_results'][:nresults]):
        print(f'''{itorrent}. {torrent["title"]}
{torrent["download"]}
{torrent["size"] / (1024 ** 2):.2f}M {torrent["seeders"]}/{torrent["leechers"]}
''')


if __name__ == '__main__':
    main()
