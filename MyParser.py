from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.page_content = []
        self.page_trash = []

    def handle_starttag(self, tag, attrs):
        self.page_content.append(DataTag(tag, "start", attrs))

        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        self.page_content.append(DataTag(tag, "end", None))
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if not "".__eq__(data) and not data.isspace():
            data = self.remove_spaces_new_line(data)
            self.page_content.append(DataTag(data, "data", None))
            print("Encountered some data  :", data)
        else:
            self.page_trash.append(data)
            print("zmesal se mi bo")

    def remove_spaces_new_line(self, data):
        regex = r'\s+'
        return re.sub(regex, " ", data)



class DataTag:
    def __init__(self, name, type, attrs):
        self.name = name
        self.type = type
        self.attrs = attrs

