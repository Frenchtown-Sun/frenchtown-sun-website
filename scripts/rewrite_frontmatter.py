#! /usr/bin/env python3

"""
One-off to add dates to things
"""

import argparse
import os

def parse_args(args=None):
    """Parse sys.args or a passed array of args, return argparse namespace"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'dir',
        help='')

    return parser.parse_args(args)

def load_date(index):
    with open(index) as rfp:
        for line in rfp.readlines():
            stripped = line.strip()
            deprefixed = stripped.removeprefix('date: ')
            if deprefixed != stripped:
                return deprefixed

def add_dates(directory):
    index = os.path.join(directory, '_index.md')
    if not os.path.exists(index):
        print("Missing _index.md!")
        return

    all_files = os.listdir(directory)
    articles = [f for f in all_files if f.endswith('.md') and f != "_index.md"]

    date = load_date(index)

    for file in articles:
        file = os.path.join(directory, file)
        with open(file) as rfp:
            contents = rfp.readlines()

        for idx, line in enumerate(contents):
            if line.strip().startswith("edition:"):
                break

        contents.insert(idx, f'date: {date}\n')

        with open(file, 'w') as wfp:
            wfp.writelines(contents)

def main():
    """Trivial main"""
    args = parse_args()
    add_dates(args.dir)


if __name__ == '__main__':
    main()
