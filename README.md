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
  * Seems like I've got a path, but I want to make sure I include checks to make it hard to mess up:
    * If I need a flag to make the current edition show up on the main page, enforce only one edition has that flag
    * more generally, check each `edition/_index.md` has good frontmatter, and each article under an edition has correct frontmatter
    * Check for images in static/ that aren't referenced in any .md
    * alt text on all images
  * If I'm going to make things look nice manually, I need to add guides on how to do each thing.
    * person-tables for obituaries and "meet the people" articles? General strategy of "wrap in a div to target class -> img or class -> p in css"?
    * OR is it better to just do some in straight html?
  * Q for maria:
    * things like the picture from the April edition on the first page. Does that go with the S. Wash. improvements, or the edition?
* Digital Calendar
