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
* Get the `<edition.pdf>`, put it in `static/editions/Frenchtown-Sun-<Month>-<YYYY>.pdf`
* Run `scripts/split_content.py`, passing in the markdown and the `YYYY-MM` format edition
* `pdfimages -all <edition.pdf> <edition>` to get the images, which we'll have to manually add to the articles. Then add them to the articles in one of the following ways:
  * If it's the top image for the paper, not part of an article, add it to the `content/<edition>/_index.md` with a markdown image tag.
  * If it's for a "Meet the staff"-type article, use the `portrait_with_text` hugo shortcode by putting `{{% portrait_with_text img="/editions/<path>.png" alt="<name>" %}}` before the text about the person and `{{% /portrait_with_text %}}` after.
  * If it's for Frenchtown then & now, use the `then_now_imgs` hugo shortcode by putting 
    ```
      {{% then_now_imgs 
        then=/editions/<path>.jpg
        now=/editions/<path>.jpg
      %}}
    ```
    at the bottom of the article.
  * For other cases, use a markdown image tag?
* ... probably other things?
* Review the content on the website, comparing it to the pdf. 
  * Most formatting should come through correctly, but sometimes it's not quite right and needs tweaking.
  * I like to make small edits to improve the format for web:
    * telephone numbers should turn into phone links: `<a href="tel:555-555-5555">555-555-5555</a>`
    * If something refers to another page (like _see page 4_), just link to the relevant thing.

## TODO
* Figure out how to pull the text and images and use those in a consistent, automated way, not just pngs of the pages.
  * Seems like I've got a path, but I want to make sure I include checks to make it hard to mess up:
    * If I need a flag to make the current edition show up on the main page, enforce only one edition has that flag
    * more generally, check each `edition/_index.md` has good frontmatter, and each article under an edition has correct frontmatter
    * Check for images in static/ that aren't referenced in any .md
    * alt text on all images
    * Telephone numbers should be links with href="tel:555-555-5555"
  * If I'm going to make things look nice manually, I need to add guides on how to do each thing.
    * instructions for shortcodes
  * Q for maria:
    * things like the picture from the April edition on the first page. Does that go with the S. Wash. improvements, or the edition?
* Digital Calendar
* How to handle Corrections?
  * It would be neat if corrected articles had a ~~strikethrough~~ and a \[CORRECTION: something something\] with a link to the "corrections" from the next issue.
