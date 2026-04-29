# ECE 5760 Final Project Site

Static GitHub Pages site built with MkDocs.

## Edit Content

Update Markdown files in `docs/`.

```sh
uv run --with mkdocs==1.6.1 mkdocs serve
```

Open the local URL printed by MkDocs and edit Markdown as needed.

## Build

```sh
uv run --with mkdocs==1.6.1 mkdocs build --strict
```

## Deploy

Push to `main`. GitHub Actions builds `docs/` into static HTML and deploys the `site/` artifact to GitHub Pages.

In GitHub repository settings, set Pages source to GitHub Actions.
