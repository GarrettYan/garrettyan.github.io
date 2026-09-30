# garrettyan.github.io

Personal portfolio and technical blog. The site is hosted on GitHub Pages at [garrettyan.github.io](https://garrettyan.github.io/). Blog posts are written locally in markdown, published to [Dev.to](https://dev.to/) via a CLI script, and linked from the portfolio homepage.

## Project Structure

```
.
├── index.html          # Portfolio homepage (GitHub Pages)
├── publish.py          # CLI script to publish posts to Dev.to
├── blog-posts/         # Markdown source files for all posts
│   ├── kubernetes-cost-optimization.md
│   ├── serverless-vs-containers-cost-analysis.md
│   ├── container-cold-start-optimization.md
│   └── ...
└── .env                # Dev.to API key (gitignored)
```

## Setup

1. Get a Dev.to API key at https://dev.to/settings/extensions
2. Create a `.env` file in the repo root:
   ```
   DEVTO_API_KEY=your_key_here
   ```
   This file is gitignored and will not be committed.

## How to Create and Publish a New Blog Post

### Step 1: Write the Post

Create a new markdown file in `blog-posts/`:

```bash
touch blog-posts/my-new-post.md
```

Add Dev.to frontmatter at the top of the file:

```markdown
---
title: "Your Post Title Here"
published: true
description: A short description for SEO and social previews.
tags: aws, devops, tutorial
cover_image:
canonical_url:
series: Optional Series Name
---

Your post content starts here...
```

Notes:
- Set `published: true` to publish live, `false` to save as draft.
- Do NOT add a `# Title` heading in the body — Dev.to renders the title from frontmatter. Start with `##` headings.
- Tags: max 4, lowercase, no special characters.

### Step 2: Publish to Dev.to

```bash
# Upload as draft
python3 publish.py blog-posts/my-new-post.md

# Publish live
python3 publish.py blog-posts/my-new-post.md --publish
```

The script will print the article URL and ID. Save the ID for future updates.

### Step 3: Update an Existing Post

If you edit the markdown and want to push changes:

```bash
python3 publish.py blog-posts/my-new-post.md --update <ID>
python3 publish.py blog-posts/my-new-post.md --update <ID> --publish
```

### Step 4: List Your Dev.to Articles

```bash
python3 publish.py --list
```

### Step 5: Add the Post to the Portfolio

Open `index.html` and add a new `<li>` entry inside the `<ul class="publications">` section. Add it at the top of the list (newest first):

```html
<li class="publication-item">
  <div class="publication-date">Month Year</div>
  <div class="publication-title">Your Post Title Here</div>
  <span class="publication-platform">Dev.to</span>
  <a href="https://dev.to/garrett_yan/your-post-slug" class="publication-link" target="_blank">View Article →</a>
</li>
```

Use the URL from Step 2 for the `href`.

### Step 6: Commit and Push

```bash
git add blog-posts/my-new-post.md index.html
git commit -m "Add new blog post: Your Post Title"
git push
```

GitHub Pages will rebuild the site automatically within a couple of minutes.

## Quick Reference

| Command | Description |
|---|---|
| `python3 publish.py <file>` | Upload as draft |
| `python3 publish.py <file> --publish` | Publish live |
| `python3 publish.py <file> --update <ID>` | Update existing draft |
| `python3 publish.py <file> --update <ID> --publish` | Update and publish |
| `python3 publish.py --list` | List all your Dev.to articles |
