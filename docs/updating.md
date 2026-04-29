# Updating the Site

## Edit Markdown

Change files under `docs/`.
Add new pages in `docs/`, then add them to `nav` in `mkdocs.yml`.

## Preview Locally

```sh
uv run --with mkdocs==1.6.1 mkdocs serve
```

## Validate Build

```sh
uv run --with mkdocs==1.6.1 mkdocs build --strict
```

## Publish

Push changes to `main`.
The GitHub Actions workflow builds static HTML and deploys it to GitHub Pages.

Repository setting required once:

1. Open repository Settings.
2. Open Pages.
3. Set source to GitHub Actions.
