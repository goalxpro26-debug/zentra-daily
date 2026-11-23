"""Rebuild blogger-import.xml in Blogger's own export format (v2).
Reads v1 (verified article content) and re-wraps each entry with:
- Blogger-format id: tag:blogger.com,1999:blog-<BLOGID>.post-<POSTID>
- kind category (#post) + label category
- replies/edit/self/alternate links, thr:total
- feed-level id/links/generator matching a real Blogger backup export.
v1 failed silently (0 posts after import) - most likely cause: entries had
custom ids and no kind category, so the importer did not recognise them as posts.
"""
import re, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

BLOG_ID = "5791451479325314145"
BLOG_URL = "https://zentradaily.blogspot.com"
NS = {'a': 'http://www.w3.org/2005/Atom'}

t = ET.parse('blogger-import.xml')
root = t.getroot()
entries = root.findall('a:entry', NS)
print('v1 entries:', len(entries))

def post_id(i):
    # unique 19-digit Blogger-style post id
    return str(7000000000000000000 + i)

out = []
out.append('<?xml version="1.0" encoding="UTF-8"?>')
out.append('<?xml-stylesheet href="http://www.blogger.com/styles/atom.css" type="text/css"?>')
out.append('<feed xmlns="http://www.w3.org/2005/Atom" xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/" xmlns:blogger="http://schemas.google.com/blogger/2008" xmlns:georss="http://www.georss.org/georss" xmlns:gd="http://schemas.google.com/g/2005" xmlns:thr="http://purl.org/syndication/thread/1.0">')
out.append(f'  <id>tag:blogger.com,1999:blog-{BLOG_ID}</id>')
out.append('  <title type="text">Zentra Daily</title>')
out.append('  <subtitle type="text">World news, sports, entertainment, AI &amp; learning, clearly explained.</subtitle>')
feed_updated = root.find('a:updated', NS).text
out.append(f'  <updated>{feed_updated}</updated>')
out.append('  <author><name>Zentra Daily Newsroom</name><email>noreply@blogger.com</email></author>')
out.append('  <generator version="7.00" uri="http://www.blogger.com">Blogger</generator>')
out.append(f'  <link rel="self" type="application/atom+xml" href="https://www.blogger.com/feeds/{BLOG_ID}/posts/default"/>')
out.append(f'  <link rel="alternate" type="text/html" href="{BLOG_URL}/"/>')

for i, e in enumerate(entries, start=1):
    old_id = e.find('a:id', NS).text
    slug = old_id.split(':', 2)[2]
    title = e.find('a:title', NS).text
    published = e.find('a:published', NS).text
    updated = e.find('a:updated', NS).text
    content = e.find('a:content', NS).text
    label = e.find('a:category', NS).get('term')
    pid = post_id(i)
    ym = published[:4] + '/' + published[5:7]
    permalink = f'{BLOG_URL}/{ym}/{slug}.html'
    out.append('  <entry>')
    out.append(f'    <id>tag:blogger.com,1999:blog-{BLOG_ID}.post-{pid}</id>')
    out.append(f'    <published>{published}</published>')
    out.append(f'    <updated>{updated}</updated>')
    out.append('    <category scheme="http://schemas.google.com/blogger/2008/kind" term="http://schemas.google.com/blogger/2008/kind#post"/>')
    out.append(f'    <category scheme="http://www.blogger.com/atom/ns#" term={quoteattr(label)}/>')
    out.append(f'    <title type="text">{escape(title)}</title>')
    out.append(f'    <content type="html">{escape(content)}</content>')
    out.append(f'    <link rel="replies" type="application/atom+xml" href="{BLOG_URL}/feeds/{pid}/comments/default" title="Post Comments"/>')
    out.append(f'    <link rel="replies" type="text/html" href="{permalink}#comment-form" title="0 Comments"/>')
    out.append(f'    <link rel="edit" type="application/atom+xml" href="https://www.blogger.com/feeds/{BLOG_ID}/posts/default/{pid}"/>')
    out.append(f'    <link rel="self" type="application/atom+xml" href="https://www.blogger.com/feeds/{BLOG_ID}/posts/default/{pid}"/>')
    out.append(f'    <link rel="alternate" type="text/html" href="{permalink}" title={quoteattr(title)}/>')
    out.append('    <author><name>Zentra Daily Newsroom</name><email>noreply@blogger.com</email></author>')
    out.append('    <thr:total>0</thr:total>')
    out.append('  </entry>')

out.append('</feed>')
open('blogger-import.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('v2 written, bytes:', len('\n'.join(out)))
