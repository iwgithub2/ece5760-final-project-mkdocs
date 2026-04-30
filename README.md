# ECE 5760 Final Project Site

Static GitHub Pages site built with Jekyll and the al-folio template.

## Edit Content

- Home page: `_pages/introduction.md`
- Main pages: `_pages/*.md`
- Blog-style notes: `_posts/YYYY-MM-DD-title.md`
- Project cards/pages: `_projects/*.md`
- News snippets: `_news/*.md`
- Site metadata/navigation: `_config.yml`

Most content updates are Markdown plus YAML front matter.

## Local Preview

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000/ece5760-final-project-mkdocs/`.

## Build

```sh
JEKYLL_ENV=production bundle exec jekyll build
```

## Deploy

Push to `main`. GitHub Actions builds the static `_site/` output and deploys it to GitHub Pages.

In repository Settings -> Pages, set source to GitHub Actions.
