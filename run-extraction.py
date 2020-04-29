import re
from lxml import html
import json
from bs4 import BeautifulSoup, NavigableString
import difflib
import requests

from MyParser import MyHTMLParser, DifferentLines

PLACE_HOLDER = "#qwe1qwe"


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
        # print(dataItem)


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

        titles = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a/b')
        titles = [title.text for title in titles]

        list_prices = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s')
        list_prices = [list_price.text for list_price in list_prices]

        prices = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b')
        prices = [price.text for price in prices]

        saving_elements = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span')

        contents = tree.xpath(
            '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span')
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
        submit_date = str(
            tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[4]/span/span[1]')[0].text).strip()
        author = str(
            tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[4]/span/span[5]/span')[0].text).strip()
        subtitle = str(
            tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[1]/div[1]/div/div[6]/h2/span')[0].text).strip()
        content = str(tree.xpath('//*[@id="ocmContainer"]/div[1]/div/div[2]/div[1]/div[1]/div[1]/text()')[0]).strip(
            '\n').strip()

        dataItem = {
            "Title": title,
            "Subject": subject,
            "SubmitDate": submit_date,
            "Author": author,
            "Subtitle": subtitle,
            "Content": content
        }
        print("Output object:\n%s" % json.dumps(dataItem, indent=8, ensure_ascii=False))

def get_beautiful_page(page):
    soup = BeautifulSoup(page, "html.parser")
    clean_page(soup)
    return soup

def get_beautiful_table(page):
    page1 = get_beautiful_page(page)
    return combine_text(str(page1).splitlines())

def remove_html_tag(text, tag):
    clean_one_tag = re.compile('<' + tag + '.*?/>', re.S)
    text = re.sub(clean_one_tag, '', text)
    clean = re.compile('<' + tag + '.*?>.*?</' + tag + '>', re.S)
    return re.sub(clean, '', text)


def clean_page(page):
    head = page.find('head')
    if head:
        # head.replace_with(page.find('title'))
        head.extract()
    [x.extract() for x in page.findAll('script')]
    [x.extract() for x in page.findAll('iframe')]
    [x.extract() for x in page.findAll('img')]
    [x.extract() for x in page.findAll('br')]


def is_junk(text):
    return text.isspace()


def parse_to_tags(page1, page2):
    page1_parser = MyHTMLParser()
    page1_parser.feed(page1.prettify())

    page2_parser = MyHTMLParser()
    page2_parser.feed(page2.prettify())

    # TODO compare tables and and create regular expresion
    result = ""
    for i in range(0, len(page1_parser.page_content), 1):
        a = page1_parser.page_content[i]
        b = page2_parser.page_content[i]
        if a.type == b.type:
            if a == b:
                result += str(a)
            elif a.is_data_type() and b.is_data_type():
                result += " #text "
            # add same type with #... for atributs
        else:
            if a.is_end_type():
                result += "\ntag missmatch ( " + str(a) + " | " + str(b) + " )"
    return result


def retrieve_content(string):
    page_parser = MyHTMLParser()
    page_parser.feed(string)
    return page_parser


def contains_content(data_tag):
    for x in data_tag.page_content:
        if x.is_data_type():
            return True
    return False


def combine_text(text):
    combined = []
    new_combined = ""
    for x in text:
        if len(x) > 0 and x[0] == '<' and not new_combined == "":
            combined.append(new_combined)
            new_combined = x
        else:
            new_combined += x
    combined.append(new_combined)
    return combined


def get_ratio(start_tag1, start_tag2):
    if not start_tag1.attrs:
        start_tag1.attrs = ''
    if not start_tag2.attrs:
        start_tag2.attrs = ''

    return difflib.SequenceMatcher(None, start_tag1.attrs, start_tag2.attrs).ratio()


# TODO find first start tag?
def is_similar_start_tag(x, y):
    # ratio = get_ratio(x.parse_content[0], y.parse_content[0])
    return (not (x.get_first_content() == y.get_first_content())) \
           and x.parse_content[0].is_same_start_tag(y.parse_content[0]) \
           and get_ratio(x.parse_content[0], y.parse_content[0]) > 0

def get_duplicates_with_diff_content(diff_with_content):
    result = []
    i = 0
    while (i < len(diff_with_content) - 1):
        first = diff_with_content[i]
        second = diff_with_content[i + 1]
        if first.line.startswith("-") and second.line.startswith("+") or (
                first.line.startswith("+") and second.line.startswith("-")
        ):
            if is_similar_start_tag(first, second):
                result.append(first)
                result.append(second)
                i += 2
            else:
                i += 1
        else:
            i += 1
    return result


def remove_unwanted_lines(all_lines, unwanted):
    for x in list(all_lines):
        if x[0] in unwanted:
            all_lines.remove(x)
    return all_lines


def get_lines_with_content(_diff_lines):
    _diff_with_content = []
    for x in _diff_lines:
        parsed_data_tag = retrieve_content(x[1:])
        if contains_content(parsed_data_tag):
            _diff_with_content.append(DifferentLines(x, parsed_data_tag.page_content))
    return _diff_with_content


def replace_dynamic_text(pairs, lines):
    new_lines = []
    for line in lines:
        for pair in pairs:
            if pair.line == line:
                first_content = pair.get_first_content().name
                line = line.replace(first_content, PLACE_HOLDER)[1:]
                continue
        if line.startswith("-"):
            line = line[1:]
        new_lines.append(line)
    return new_lines


def list_to_string(s):
    str1 = " "
    return (str1.join(s))

def walker(soup):
    # soup = BeautifulSoup.BeautifulSoup(html)
    for child in soup.recursiveChildGenerator():
        name = getattr(child, "name", None)

        if name is not None:
            print(name)
        elif not child.isspace():  # leaf node, don't print spaces
            print(child)

def recursiveChildren(x):
    contains_diff_child = []
    is_this_one_needed = False
    if "childGenerator" in dir(x):
        children = list(x.childGenerator())
        for child in children:
            new_children, is_child_needed = recursiveChildren(child)  # name = getattr(child, "name", None)
            if is_child_needed:
                is_this_one_needed = True
            contains_diff_child = contains_diff_child + new_children
                # child.extract()
    else:
        if not x.isspace():  # Just to avoid printing "\n" parsed from document.
            print("[Terminal Node]", x)
            if PLACE_HOLDER in str(x.encode('utf-8')):
                is_this_one_needed = True

    if not is_this_one_needed:
        contains_diff_child.append(x)
    return contains_diff_child, is_this_one_needed

def compare_files(_page1, _page2):
    differ = difflib.Differ()
    str_page1 = get_beautiful_table(_page1)
    str_page2 = get_beautiful_table(_page2)
    return list(differ.compare(str_page1, str_page2))

def get_pairs(diff_lines):
    cleaned_lines = remove_unwanted_lines(list(diff_lines), ['?', ' '])
    diff_with_content = get_lines_with_content(cleaned_lines)
    pairs = get_duplicates_with_diff_content(diff_with_content)
    return pairs

def get_page_wrapper(_page1, _page2):
    diff_lines = compare_files(_page1, _page2)
    cleaned_lines_copy = remove_unwanted_lines(list(diff_lines), ['?', '+'])
    pairs = get_pairs(diff_lines)
    result = replace_dynamic_text(pairs, cleaned_lines_copy)
    soup = get_beautiful_page(list_to_string(result))
    to_remove, is_child_needed = recursiveChildren(soup)
    for element in to_remove:
        element.extract()
    return soup


rtv1 = open('rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html', 'r', encoding='utf8').read()
rtv2 = open('rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r', encoding='utf8').read()
overstock1 = open('overstock.com/jewelry01.html', 'r', encoding="ISO-8859-1").read()
overstock2 = open('overstock.com/jewelry02.html', 'r', encoding="ISO-8859-1").read()
slovenskenovice1 = open('slovenskenovice.si/Aljaž, ki je prebolel covid-19_ Lahko se že počutiš izvrstno, pa pride spet udar in ne moreš nič.html','r', encoding='utf-8').read()
slovenskenovice2 = open('slovenskenovice.si/Hrvaška podaljšala ukrep, ki se tiče tudi Slovencev.html', 'r', encoding='utf-8').read()

wrapper = get_page_wrapper(rtv1, rtv2)
test = wrapper.prettify()

1
"""#regular_expression_rtv([rtv1, rtv2])
xpath_rtv([rtv1, rtv2])

overstock1 = open('overstock.com/jewelry01.html', 'r', encoding="ISO-8859-1").read()
overstock2 = open('overstock.com/jewelry02.html', 'r', encoding="ISO-8859-1").read()
regular_expression_overstock([overstock1, overstock2])

slovenskenovice1 = open('slovenskenovice.si/Aljaž, ki je prebolel covid-19_ Lahko se že počutiš izvrstno, pa pride spet udar in ne moreš nič.html', 'r', encoding='utf-8').read()
slovenskenovice2 = open('slovenskenovice.si/Hrvaška podaljšala ukrep, ki se tiče tudi Slovencev.html', 'r', encoding='utf-8').read()
xpath_slonovice([slovenskenovice1, slovenskenovice2])
"""
# print("rtv1 len:", len(page2.prettify()))
