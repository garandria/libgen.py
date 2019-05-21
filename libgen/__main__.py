import argparse

import requests

from .exceptions import NoAvailableMirror
from .mirrors import MIRRORS


class MirrorFinder(object):
    def __init__(self) -> None:
        self.mirrors = MIRRORS

    def run(self, search_term: str, non_interactive: bool, download_all: bool):
        """Tries to find an active mirror and runs the search on it."""
        try:
            mirror = self.find_active_mirror()
            if mirror is None:
                raise NoAvailableMirror
            mirror(search_term).run(non_interactive, download_all)
        except NoAvailableMirror as e:
            print(e)

    # TODO: eliminate this method
    # Maybe use the chain of responsability pattern
    def find_active_mirror(self):
        for (homepage, mirror) in self.mirrors.items():
            r = requests.get(homepage)
            if r.status_code == 200:
                return mirror
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--search',
                   dest='search',
                   required=True,
                   help='search term')
    p.add_argument('-n', '--non-interactive',
                   dest='non_interactive',
                   help='non interactive mode, download first available choice',
                   action='store_true',
                   default=False)
    p.add_argument('-a', '--all',
                   dest='all',
                   help='download every book from the result',
                   action='store_true',
                   default=False)
    args = p.parse_args()
    MirrorFinder().run(args.search, args.non_interactive, args.all)


if __name__ == '__main__':
    main()
