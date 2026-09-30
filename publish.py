#!/usr/bin/env python3
"""Publish local markdown blog posts to Dev.to via their API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def load_env(filepath=".env"):
    """Load key=value pairs from a .env file into os.environ."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    value = value.strip().strip("\"'")
                    os.environ.setdefault(key.strip(), value)


def get_api_key():
    load_env()
    key = os.environ.get("DEVTO_API_KEY")
    if not key:
        print("Error: DEVTO_API_KEY not found.", file=sys.stderr)
        print("Set it in .env or export DEVTO_API_KEY=your_key", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method, path, api_key, data=None):
    url = f"https://dev.to/api{path}"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "DevToPublisher/1.0",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def publish_article(file_path, published, article_id=None):
    api_key = get_api_key()

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        body_markdown = f.read()

    payload = {
        "article": {
            "body_markdown": body_markdown,
            "published": published,
        }
    }

    if article_id:
        result = api_request("PUT", f"/articles/{article_id}", api_key, payload)
        action = "Updated & published" if published else "Updated"
    else:
        result = api_request("POST", "/articles", api_key, payload)
        action = "Published" if published else "Draft created"

    print(f"{action}: {result.get('title', 'Untitled')}")
    print(f"URL: {result.get('url', 'N/A')}")
    print(f"ID:  {result.get('id', 'N/A')}")


def list_articles():
    api_key = get_api_key()
    articles = api_request("GET", "/articles/me/all?per_page=30", api_key)

    if not articles:
        print("No articles found.")
        return

    for a in articles:
        status = "LIVE" if a.get("published") else "DRAFT"
        print(f"[{status}] {a.get('title', 'Untitled')}")
        print(f"        {a.get('url', 'N/A')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Publish markdown posts to Dev.to")
    parser.add_argument("file", nargs="?", help="Path to markdown file")
    parser.add_argument("--publish", action="store_true", help="Publish live (default: draft)")
    parser.add_argument("--update", type=int, metavar="ID", help="Update existing article by ID")
    parser.add_argument("--list", action="store_true", help="List your Dev.to articles")

    args = parser.parse_args()

    if args.list:
        list_articles()
    elif args.file:
        publish_article(args.file, args.publish, args.update)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
