import re
from lxml import html
import json
from bs4 import BeautifulSoup

import requests

from MyParser import MyHTMLParser

removed_tags = ["script", "link", "meta"]
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



def regular_expression_overstock(pages):
    title_regex = r"<a.*<b>(.*)<\/b>\n*<\/a><br>"
    list_price_regex = r"<td align=\"left\" nowrap=\"nowrap\"><s>(.*)<\/s><\/td>"
    price_regex = r"<span class=\"bigred\"><b>(.*)<\/b><\/span>"
    saving_regex = r"<span class=\"littleorange\">(.*) \(.*\)<\/span>"
    saving_percent_regex = r"<span class=\"littleorange\">\$.* (.*)<\/span>"
    content_regex = r"<td valign=\"top\"><span class=\"normal\">([\s\S]*?)<br><a href.*><span class=\"tiny\"><b>(.*)<\/b>"

    for page in pages:
        titles = re.compile(title_regex).findall(page)
        list_prices = re.compile(list_price_regex).findall(page)
        prices = re.compile(price_regex).findall(page)
        savings = re.compile(saving_regex).findall(page)
        saving_percents = re.compile(saving_percent_regex).findall(page)

        matches = re.compile(content_regex).findall(page)
        contents = []
        for match in matches:
            contents.append(match[0] + "\n" + match[1])

        for i in range(len(titles)):
            dataItem = {
                "Title": titles[i],
                "ListPrice": list_prices[i],
                "Price": prices[i],
                "Saving": savings[i],
                "SavingPercent": saving_percents[i],
                "Content": contents[i]
            }

def xpath_overstock(pages):
    for page in pages:
        tree = html.fromstring(page)

        titles = tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a/b')
        titles = [title.text for title in titles]

        list_prices = tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s')
        list_prices = [list_price.text for list_price in list_prices]

        prices = tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b')
        prices = [price.text for price in prices]

        saving_elements = tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span')

        contents = tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span')
        contents = [content.text for content in contents]

        savings = []
        saving_percents = []
        for saving_element in saving_elements:
            savings.append(saving_element.text[:-6])
            saving_percents.append(saving_element.text[-5:])

        for i in range(len(titles)):
            dataItem = {
                "Title": titles[i],
                "ListPrice": list_prices[i],
                "Price": prices[i],
                "Saving": savings[i],
                "SavingPercent": saving_percents[i],
                "Content": contents[i]
            }


def regular_expression_slonovice(pages):
    title_regex = r"<h1 class=\"itemTitle\">\s*([\s\S]*)<\/h1>"
    subject_regex = r"<span class=\"itemSuperscript\">(.*)<\/span>"
    author_regex = r"<span class=\"itemAuthor\">\s*Piše:\s+<span>(.*)<\/span>"
    submit_date_regex = r"<span class=\"itemDatePublished\">\s*Objavljeno (.*)<\/span>"
    subtitle_regex = r"<h2 class=\"itemSubtitle\">\s*<span>(.*)<\/span>"
    content_regex = r"<div class=\"itemFullText\" .*>([\s\S]*)<div class=\"itemInfoboxText\""

    for page in pages:
        page = page.replace("&nbsp", "")

        title = re.compile(title_regex).search(page).group(1).strip()
        subject = re.compile(subject_regex).search(page).group(1).strip()
        submit_date = re.compile(submit_date_regex).search(page).group(1)
        author = re.compile(author_regex).search(page).group(1)
        subtitle = re.compile(subtitle_regex).search(page).group(1)
        content = re.compile(content_regex).search(page).group(1)

        dataItem = {
            "Title": title,
            "Subject": subject,
            "SubmitDate": submit_date,
            "Author": author,
            "Subtitle": subtitle,
            "Content": content
        }
        print("Output object:\n%s" % json.dumps(dataItem, indent=8, ensure_ascii=False))


def xpath_slonovice(pages):
    for page in pages:
        tree = html.fromstring(page)
        title = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[3]/h1')[0].text).strip()
        subject = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[2]/span')[0].text).strip()
        submit_date = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[4]/span/span[1]')[0].text).strip()
        author = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[4]/span/span[5]/span')[0].text).strip()
        subtitle = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[6]/h2/span')[0].text).strip()
        content = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[2]/div[1]/div[1]/div[1]/text()')[0]).strip('\n').strip()

        dataItem = {
            "Title": title,
            "Subject": subject,
            "SubmitDate": submit_date,
            "Author": author,
            "Subtitle": subtitle,
            "Content": content
        }
        print("Output object:\n%s" % json.dumps(dataItem, indent=8, ensure_ascii=False))


rtv1 = open('rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html', 'r', encoding='utf8').read()
rtv2 = open('rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r', encoding='utf8').read()





"""#regular_expression_rtv([rtv1, rtv2])
xpath_rtv([rtv1, rtv2])

overstock1 = open('overstock.com/jewelry01.html', 'r', encoding="ISO-8859-1").read()
overstock2 = open('overstock.com/jewelry02.html', 'r', encoding="ISO-8859-1").read()
regular_expression_overstock([overstock1, overstock2])

slovenskenovice1 = open('slovenskenovice.si/Aljaž, ki je prebolel covid-19_ Lahko se že počutiš izvrstno, pa pride spet udar in ne moreš nič.html', 'r', encoding='utf-8').read()
slovenskenovice2 = open('slovenskenovice.si/Hrvaška podaljšala ukrep, ki se tiče tudi Slovencev.html', 'r', encoding='utf-8').read()
xpath_slonovice([slovenskenovice1, slovenskenovice2])
"""
def get_beautiful_page(page):
    soup = BeautifulSoup(page, "html.parser")
    clean_page(soup)
    return soup

def remove_html_tag(text, tag):
    clean_one_tag = re.compile('<' + tag + '.*?/>', re.S)
    text = re.sub(clean_one_tag, '', text)
    clean = re.compile('<' + tag + '.*?>.*?</'+tag+'>', re.S)
    return re.sub(clean, '', text)

def clean_page(page):
    head = page.find('head')
    if head:
        head.replace_with(page.find('title'))
    [x.extract() for x in page.findAll('script')]


page1 = get_beautiful_page(rtv1)
page2 = get_beautiful_page(rtv2)

page1_parser = MyHTMLParser()
page1_parser.feed(page1.prettify())

page2_parser = MyHTMLParser()
page2_parser.feed(page2.prettify())

#TODO compare tables and and create regular expresion
print("page len:", len(page1.prettify()))
print("rtv1 len:", len(page2.prettify()))