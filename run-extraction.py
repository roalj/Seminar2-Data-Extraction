import re
import json

import requests


def regular_expression_rtv(pages):
    author_regex = r"<div class=\"author-name\">(.*)<\/div>"

    for page in pages:
        match = re.compile(author_regex).search(page)
        author = match.group(1)
        print(author)
        """
        dataItem = {
            "Author": title,
            "PublishedTime": date,
            "Title": imageUrl,
            "SubTitle": subTitle,
            "Lead": lead,
            "Content": content
        }"""

pageContent1 = open('rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html', 'r').read()
pageContent2 = open('rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r').read()

regular_expression_rtv([pageContent1, pageContent2])
