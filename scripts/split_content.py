#! /usr/bin/env python3

"""
Takes a markdown download of Maria's Google doc of content, and splits it into articles in an edition.
"""

import argparse
import os
import re

import edition

def parse_args(args=None):
    """Parse sys.args or a passed array of args, return argparse namespace"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'content',
        help='the markdown file to split')

    parser.add_argument(
        'edition',
        default=utils.next_month(),
        help='the edition, e.g. 2026-05, which will serve as the name of the folder in content/editions')

    return parser.parse_args(args)

def split_into_articles(content):
    articles = []
    most_recent = None
    for line in content:
        if line.startswith('**'):
            title = line.strip().strip('*')
            filename = utils.filename_from_title(title)
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
    protocol_regex = r'(https?://)'
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
        # Sometimes the links have already been converted to markdown, but
        # not in the way we want on the website.
        links = re.findall(protocol_regex+r'(.+)\]', lines[i])
        if links:
            for protocol, link in links:
                print(f'Attempting to de-format link in line: {lines[i]}')
                whole_link = f'{protocol}{link}'
                already_md_regex = f'\\[({re.escape(whole_link)})\\]\\(\\1\\)'
                print(already_md_regex)
                lines[i] = re.sub(already_md_regex, whole_link, lines[i])
        links = re.findall(protocol_regex+r'(\S+)', lines[i])
        if links:
            for protocol, link in links:
                print(f'Formatting link in line: {lines[i]}')
                link = link.rstrip('.')
                whole_link = f'{protocol}{link}'
                md_link = f'[{link}]({whole_link})'
                lines[i] = re.sub(re.escape(whole_link), md_link, lines[i])

def write_articles(articles, edition_dir, date):
    for weight, article in enumerate(articles):
        with open(os.path.join(edition_dir, article["filename"]), 'w') as wfp:
            front_matter = (
                '---\n'
                f'title: "{article["title"]}"\n'
                f'edition: "{article["edition"]}"\n'
                f'weight: {weight+1}\n'
                f'date: {date.date}\n'
                'layout: "article"\n'
                '---\n'
            )
            wfp.writelines(front_matter)
            wfp.writelines(article["text"])

def main():
    """Trivial main"""
    args = parse_args()
    date = utils.parse_date(args.edition)

    with open(args.content) as rfp:
        articles = split_into_articles(rfp.readlines())

    for article in articles:
        format_article(article)
        article["edition"] = args.edition

    edition_dir = utils.ensure_edition_dir(args.edition)
    write_articles(articles, edition_dir, date)
    utils.add_index(date, edition_dir)

    print('Remember to extract images with: ')
    print('`pdfimages -png -all Frenchtown-Sun-<Month>-<YYYY>.pdf Frenchtown-Sun-<Month>-<YYYY>`')
    print(' and then add them to the articles.')


if __name__ == '__main__':
    main()



