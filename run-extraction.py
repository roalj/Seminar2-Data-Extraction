import re
from lxml import html
import json

import requests

# TODO 1  If the extracted value should be further processed, use regular expressions or other techniques to normalize them.?? a more bit datum dejasko datum al to kar je napisano?
# TODO 2  a more bit content brez html tagov?
def regular_expression_rtv(pages):
    author_regex = r"<div class=\"author-name\">(.*)<\/div>"
    published_time_regex = r"<div class=\"publish-meta\">[\n\s]*(.*)<br>"
    title_regex = r"<header class=\"article-header\">(.|\n)*<h1>(.*)<\/h1>"
    sub_title_regex = r"<header class=\"article-header\">(.|\n)*<div class=\"subtitle\">(.*)<\/div>"
    lead_regex = r"<header class=\"article-header\">(.|\n)*<p class=\"lead\">[\n\s]*(.*)<\/p>"
    content_regex = r"<div class=\"article-body\">(\s|\n|.)*?<div class=\"article-column\""

    for page in pages:
        author = re.compile(author_regex).search(page).group(1)
        published_time = re.compile(published_time_regex).search(page).group(1)
        title = re.compile(title_regex).search(page).group(2)
        subtitle = re.compile(sub_title_regex).search(page).group(2)
        lead = re.compile(lead_regex).search(page).group(2)
        content = re.compile(content_regex).search(page).group(0)
        print(content)
        dataItem = {
            "Author": author,
            "PublishedTime": published_time,
            "Title": title,
            "SubTitle": subtitle,
            "Lead": lead,
            "Content": content
        }
        #print(dataItem)

def xpath_rtv(pages):
    for page in pages:
        tree = html.fromstring(page)
        author = str(tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div')[0].text)
        published_time = str(tree.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0])
        title = str(tree.xpath('//*[@id="main-container"]/div[3]/div/header/h1')[0].text)
        subtitle = str(tree.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]')[0].text)
        lead = str(tree.xpath('//*[@id="main-container"]/div[3]/div/header/p')[0].text)

        content = ""
        for items in tree.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p'):
            content += items.text_content() + "\n"

        dataItem = {
            "Author": author,
            "PublishedTime": published_time.strip(),
            "Title": title,
            "SubTitle": subtitle,
            "Lead": lead,
            "Content": content
        }


rtv1 = open('rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html', 'r', encoding='utf8').read()
rtv2 = open('rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r', encoding='utf8').read()

#regular_expression_rtv([rtv1, rtv2])
xpath_rtv([rtv1, rtv2])
