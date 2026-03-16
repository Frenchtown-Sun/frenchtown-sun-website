# Frenchtown Borough Sun

A civic newsletter focused on Frenchtown, NJ.

## Goals
This is the website for the Frenchtown Borough Sun.

The primary goals:
* Make sure the process is easy for the other volunteers running the newsletter
  * This is a print-first newsletter, so we should avoid pushing things through web-focused flows. Instead, we should automate converting the print-focused formats to the web. 
* Respect Frenchtonians
  * Keep tracking as minimal as we can. _No_ third-party ad networks.
* Keep it fast
  * We don't need a huge framework to serve some static updates on town happenings.

## Configuration

This is a static site, using [Hugo](https://gohugo.io). A github workflow automatically builds & deploys the site.

## TODO
* enable https
* About page
* figure out how to embed/include first issue
  * Make a few examples as hidden pages to show folks at the wednesday meeting.
    * Use https://robinmoisson.github.io/staticrypt/ to protect
    1. simple embed
    2. "view first issue, or download" with separate pure-embed page
    3. pdf to png (pdftoppm)
