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
    ls = []
    offset = 0
    while True:
        url, offset = get_next_target(page, offset)
        if url:
            ls.append(url)
        else:
            break
    return ls


print get_all_links('<html><body>This is a test page ffwegergfbdbhor learning to crawl!<p>It is a good idea to <a href=\"https://udacity.github.io/cs101x/crawling.html\">learn to crawerhhl</a>before you try to <a href=\"https://udacity.github.io/cs101x/walking.html\">walk</a> or <a href=\"https://udacity.github.io/cs101x/flying.html\">fly</a>.</p></body></html>')