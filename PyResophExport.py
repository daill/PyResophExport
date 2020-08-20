import argparse
import base64
import datetime
import random
import re
import hashlib
import json
import string
from xml.sax import make_parser, handler


class NoteHandler(handler.ContentHandler):
    def __init__(self):
        self.p = re.compile("^(.*?)\n", re.M)
        self.notes = {}
        self.note = {}
        self.content = ""

    def startElement(self, name, attrs):
        self.content = ""

    def characters(self, content):
        self.content += content.strip()

    def endElement(self, name):
        cnt = self.content
        if name == "content":
            dc = base64.b64decode(cnt).decode("utf-8")
            self.note["content"] = dc
            try:
                self.note["key"] = self.p.search(dc).group(1)
            except (AttributeError):
                self.note["key"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                pass
        elif name == "create":
            date_time_obj = datetime.datetime.strptime(cnt, '%Y-%m-%d %H:%M:%S')
            self.note["createdate"] = date_time_obj.timestamp()
        elif name == 'modify':
            date_time_obj = datetime.datetime.strptime(cnt, '%Y-%m-%d %H:%M:%S')
            self.note["modifydate"] = date_time_obj.timestamp()
        elif name == 'object':
            self.notes[self.note["key"]] = self.note
            self.note = {}


    def get_notes(self):
        return self.notes


handler = NoteHandler()


# {
# "content": "bla",
# "modifydate": 1597913383.9847322,
# "createdate": 1597912945.8167322,
# "savedate": 1597913378.271347,
# "syncdate": 0,
# "tags": []
# }
def convert_nvpy():

    for key, val in handler.get_notes().items():

        outputdict = {"content": val["content"], "modifydate": val["modifydate"], "createdate": val["createdate"],
                      "savedate": 0, "syncdate": 0, "tags": []}

        hash_object = hashlib.sha256(bytes(key, encoding='utf8'))
        hex_dig = hash_object.hexdigest()
        f = open(hex_dig[10:] + ".json", 'w')
        json.dump(outputdict, f)


def parse(f):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(f)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', type=str,
                        help='the file which contains the ResophNotes data')
    parser.add_argument('-f', type=str, help='exports to chosed format. Avalable formats: nvpy')
    args = parser.parse_args()
    parse(args.d)

    if args.f == 'nvpy':
       convert_nvpy()


if __name__ == "__main__":
    main()
