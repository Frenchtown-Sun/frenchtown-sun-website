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

### Layout
* Articles are individual .md files with hugo frontmatter at the top.
* Articles are arranged into "editions", which also depend on info in the frontmatter of a corresponding `editions/<YYYY-MM>/_index.md`
* scripts/split_content.py can be used to split a markdown file containing all the articles into a set of articles with correct frontmatter.
* The `/archives` is where editions are listed, and `/editions` is set up to redirect there. This could've been done the other way around, but I liked this slightly better.

## Updating
When a new edition comes out (current workflow):
* Get the doc with article content from Maria, and export to markdown
* Get the `<edition.pdf>`, put it in `static/editions`
* Run `scripts/split_content.py`, passing in the markdown and the `YYYY-MM` format edition
* `pdfimages -all <edition.pdf>` to get the images, which we'll have to manually add to the articles. Then add them to the articles with a markdown image tag.
* Add the `editions/<YYYY-MM>/_index.md` file with correct frontmatter (look at the previous one for an example).
* ... probably other things?

## TODO
* Figure out how to pull the text and images and use those in a consistent, automated way, not just pngs of the pages.
* Digital Calendar
