#! /usr/bin/env python3

"""
Takes a markdown download of Maria's Google doc of content, and splits it into articles in an edition.
"""

import argparse
import collections
import os
import re

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def parse_args(args=None):
    """Parse sys.args or a passed array of args, return argparse namespace"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'content',
        help='the markdown file to split')

    parser.add_argument(
        'edition',
        help='the edition, e.g. 2026-05, which will serve as the name of the folder in content/editions')

    return parser.parse_args(args)

def ensure_edition_dir(edition):
    edition_dir = os.path.join(ROOT_DIR, f'content/editions/{edition}')
    os.makedirs(edition_dir, exist_ok=True)
    return edition_dir

def split_into(content):
    articles = []
    most_recent = None
    for line in content:
        if line.startswith('**'):
            title = line.strip().strip('*')
            filename = re.sub(r'[^\w\d -]', '', title)
            filename = re.sub(r'\s+', '_', filename) + '.md'
            most_recent = {
                "title": title,
                "filename": filename,
                "text": []
            }
            articles.append(most_recent)
            continue

        if most_recent is None:
            print(f"discarding: {line}")
        else:
            most_recent['text'].append(line)

    return articles

def write_articles(articles, edition_dir):
    for weight, article in enumerate(articles):
        with open(os.path.join(edition_dir, article["filename"]), 'w') as wfp:
            front_matter = (
                '---\n'
                f'title: "{article["title"]}"\n'
                f'edition: "{article["edition"]}"\n'
                f'weight: {weight+1}\n'
                'layout: "article"\n'
                '---\n'
            )
            wfp.writelines(front_matter)
            wfp.writelines(article["text"])

def main():
    """Trivial main"""
    args = parse_args()

    with open(args.content) as rfp:
        articles = split_into(rfp.readlines())

    for article in articles:
        article["edition"] = args.edition

    edition_dir = ensure_edition_dir(args.edition)
    write_articles(articles, edition_dir)


if __name__ == '__main__':
    main()



