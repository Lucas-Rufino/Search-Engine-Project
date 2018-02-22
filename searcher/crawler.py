import requests
import re

_patternTags = re.compile(r'<\s*a(\s+\w+\s*=\s*(\w*|\"[^\"]*\"))*\s*>')
_patternLink = re.compile(r'href\s*=\s*\"')

def get_next_target(page, offset):
    attr = None
    while not attr:
        tag = _patternTags.search(page, offset)
        if not tag:
            return None, 0
        attr = _patternLink.search(page, tag.start(), tag.end())
        offset = tag.end()
    bgn_quote = attr.end()
    end_quote = page.find('"', bgn_quote)
    return page[bgn_quote:end_quote], end_quote

def get_all_links(page):
    urls = set()
    offset = 0
    while True:
        url, offset = get_next_target(page, offset)
        if url:
            urls.add(url)
        else:
            break
    return urls

def get_page(url):
    try:
        page = requests.get(url)
    except Exception:
        return None
    if page.status_code != 200:
        return None
    return page.content
    
def crawl_web(seed, max_depth = -1):
    data = []
    depth = 0
    depthnx = set()
    crawled = set()
    tocrawl = set()
    tocrawl.add(seed)
    while tocrawl and (depth <= max_depth or max_depth == -1):
        url = tocrawl.pop()
        if url not in crawled:
            page = get_page(url)
            if page:
                urls = get_all_links(page)
                depthnx = depthnx.union(urls)
                crawled.add(url)
                data.append((url, page))
        if not tocrawl:
            tocrawl = depthnx
            depthnx = set()
            depth += 1
    return data