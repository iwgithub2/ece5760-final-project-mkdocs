---
layout: page
title: updating
permalink: /updating/
description: How to edit and publish the site.
nav: true
nav_order: 5
---

## Edit Markdown

Update content in these files:

| Path | Purpose |
| --- | --- |
| `_pages/introduction.md` | Home page. |
| `_pages/*.md` | Top-level pages. |
| `_posts/YYYY-MM-DD-title.md` | Blog-style project notes. |
| `_projects/*.md` | Project cards and detail pages. |
| `_news/*.md` | News snippets on the home page. |
| `_config.yml` | Site title, URL, features, navigation metadata. |

## Preview Locally

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000/ece5760-final-project-mkdocs/`.

## Publish

Push changes to `main`.
The GitHub Actions workflow builds static HTML into `_site/` and deploys it to GitHub Pages.
