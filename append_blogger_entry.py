#!/usr/bin/env python3
"""Append one new article to blogger-import.xml (v2 Blogger format).

Reads the article markdown from src/content/articles/<slug>.md, converts
the body to the same simple HTML the v2 builder used (paragraphs, *em*,
## Sources -> h2 + ul of source-name links), prepends the hero-image
paragraph (raw.githubusercontent URL), and inserts a new <entry> with the
next sequential Blogger-style post id (7000000000000000000 + n) just before
</feed>. Updates the feed <updated> timestamp.

Usage: python3 append_blogger_entry.py <slug>
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent
BLOG_ID = "5791451479325314145"
BLOG_URL = "https://zentradaily.blogspot.com"
REPO = "goalxpro26-debug/zentra-daily"


def md_to_html(body: str) -> list[str]:
    """Convert the article body (after frontmatter) to HTML lines."""
    lines: list[str] = []
    in_sources = False
    for raw in body.strip().split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            lines.append(f"<h2>{escape(line[3:].strip())}</h2>")
            in_sources = True
            continue
        if line.startswith("- ["):
            m = re.match(r"- \[(.*?)\]\((.*?)\)", line)
            if m:
                label = m.group(1).split(" — ")[0].split(" - ")[0]
                lines.append(f'<li><a href="{m.group(2)}">{escape(label)}</a></li>')
            continue
        # inline *emphasis*
        line = re.sub(r"\*([^*]+)\*", lambda m: f"<em>{escape(m.group(1))}</em>", escape(line))
        lines.append(f"<p>{line}</p>")
    # wrap consecutive <li> in <ul>
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("<li>"):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("<li>"):
                out.append(lines[i])
                i += 1
            out.append("</ul>")
        else:
            out.append(lines[i])
            i += 1
    return out


def main() -> None:
    slug = sys.argv[1]
    md_path = ROOT / "src/content/articles" / f"{slug}.md"
    text = md_path.read_text()
    fm, body = text.split("---", 2)[1], text.split("---", 2)[2]
    fm_d = dict(re.findall(r'^(\w+):\s*"(.*)"$', fm, flags=re.M))
    title = fm_d["title"]
    label = fm_d["category"]
    hero = fm_d.get("heroImage", "")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    xml_path = ROOT / "blogger-import.xml"
    xml = xml_path.read_text()
    n = xml.count("<entry>")
    pid = str(7000000000000000000 + n + 1)
    ym = now[:4] + "/" + now[5:7]
    permalink = f"{BLOG_URL}/{ym}/{slug}.html"

    content_lines: list[str] = []
    if hero:
        img_url = f"https://raw.githubusercontent.com/{REPO}/main/public{hero}"
        content_lines.append(f'<p><img src="{img_url}" alt="{escape(title)}" /></p>')
        content_lines.append("<p><em>Illustration — not a photograph</em></p>")
    content_lines += md_to_html(body)
    content_html = "\n".join(content_lines)

    entry = f"""  <entry>
    <id>tag:blogger.com,1999:blog-{BLOG_ID}.post-{pid}</id>
    <published>{now}</published>
    <updated>{now}</updated>
    <category scheme="http://schemas.google.com/blogger/2008/kind" term="http://schemas.google.com/blogger/2008/kind#post"/>
    <category scheme="http://www.blogger.com/atom/ns#" term={quoteattr(label)}/>
    <title type="text">{escape(title)}</title>
    <content type="html">{escape(content_html)}</content>
    <link rel="replies" type="application/atom+xml" href="{BLOG_URL}/feeds/{pid}/comments/default" title="Post Comments"/>
    <link rel="replies" type="text/html" href="{permalink}#comment-form" title="0 Comments"/>
    <link rel="edit" type="application/atom+xml" href="https://www.blogger.com/feeds/{BLOG_ID}/posts/default/{pid}"/>
    <link rel="self" type="application/atom+xml" href="https://www.blogger.com/feeds/{BLOG_ID}/posts/default/{pid}"/>
    <link rel="alternate" type="text/html" href="{permalink}" title={quoteattr(title)}/>
    <author><name>Zentra Daily Newsroom</name><email>noreply@blogger.com</email></author>
    <thr:total>0</thr:total>
  </entry>
</feed>"""
    xml = re.sub(r"  <updated>[^<]+</updated>", f"  <updated>{now}</updated>", xml, count=1)
    xml = xml.replace("</feed>", entry, 1)
    xml_path.write_text(xml)
    print(f"appended entry {n + 1} (post {pid}) for {slug}")


if __name__ == "__main__":
    main()
