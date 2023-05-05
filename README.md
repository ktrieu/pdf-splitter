# PDF Splitter

A small utility to split PDFs on a list of page numbers. I'm sure this already exists (Acrobat can do this, for one), but this is a faster way if you just have page numbers you want to split at.

## Usage

`pdf-splitter.py [pdf] [pages]`

`pages` is a comma separated list of pages to split at, e.g. (23,45,..).
By default a split page will be included in the _first_ PDF. Suffix the page number with `!` to include it in both.

## Dependencies

This needs `pypdf` installed. You can either use the included `Pipfile` to get it, or just install it globally if you're a Pipenv disliker.
