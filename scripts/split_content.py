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

def split_into_articles(content):
    articles = []
    most_recent = None
    for line in content:
        if line.startswith('**'):
            title = line.strip().strip('*')
            filename = re.sub(r'[^\w\d -]', '', title)
            filename = re.sub(r'\s+', '_', filename) + '.md'
            print(f'Found article: {title}')
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

def format_article(article):
    non_digit = r'(\D|^)'
    phone_regex = r'(\d{3}-\d{3}-\d{4})'
    list_regex = r'^•\t?'
    link_regex = r'(https?://)(\S+)'
    lines = article['text']
    for i in range(len(lines)):
        # Strip trailing whitespace
        lines[i] = lines[i].rstrip(' ')
        # Find-then-update, rather than just calling re.sub, so we can log nicely.
        if re.search(non_digit + phone_regex + non_digit, lines[i]) is not None:
            print(f'Replacing phone number with link in: {lines[i]}')
            lines[i] = re.sub(phone_regex, r'<a href="tel:\1">\1</a>', lines[i])
        if re.match(r'•', lines[i]) is not None:
            print(f'Reformatting list in line: {lines[i]}')
            lines[i] = re.sub(list_regex, '* ', lines[i])
        links = re.findall(link_regex, lines[i])
        if links:
            for protocol, link in links:
                print(f'Formatting link in line: {lines[i]}')
                link = link.rstrip('.')
                whole_link = f'{protocol}{link}'
                md_link = f'[{link}]({whole_link})'
                lines[i] = re.sub(re.escape(whole_link), md_link, lines[i])

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

# TODO: Replace with date.strptime from python 3.14 when I can use that.
def get_month_name(month_int):
    if month_int == 1:
        return "January"
    if month_int == 2:
        return "February"
    if month_int == 3:
        return "March"
    if month_int == 4:
        return "April"
    if month_int == 5:
        return "May"
    if month_int == 6:
        return "June"
    if month_int == 7:
        return "July"
    if month_int == 8:
        return "August"
    if month_int == 9:
        return "September"
    if month_int == 10:
        return "October"
    if month_int == 11:
        return "November"
    if month_int == 12:
        return "December"

def add_index(edition, edition_dir):
    year, month = edition.split('-')
    year = int(year)
    month = int(month)
    month_name = get_month_name(month)

    with open(os.path.join(edition_dir, '_index.md'), 'w') as wfp:
        front_matter = (
            '---',
            f'title: "{month_name}, {year}"',
            f'year: {year}',
            f'monthIndex: {month}',
            f'date: {year}-{month:02}-01',  # Just mark it as the first of the month. Currently just used for sorting.
            f'pdf: /editions/Frenchtown-Sun-{month_name}-{year}.pdf',
            '---',
        )
        wfp.writelines('\n'.join(front_matter))

def main():
    """Trivial main"""
    args = parse_args()

    with open(args.content) as rfp:
        articles = split_into_articles(rfp.readlines())

    for article in articles:
        format_article(article)
        article["edition"] = args.edition

    edition_dir = ensure_edition_dir(args.edition)
    write_articles(articles, edition_dir)
    add_index(args.edition, edition_dir)

    print('Remember to extract images with: ')
    print('`pdfimages -png -all Frenchtown-Sun-<Month>-<YYYY>.pdf Frenchtown-Sun-<Month>-<YYYY>`')
    print(' and then add them to the articles.')


if __name__ == '__main__':
    main()



