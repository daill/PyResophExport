import argparse
import base64
import re
from xml.sax import make_parser, handler


class NoteHandler(handler.ContentHandler):
    def __init__(self):
        self.p = re.compile("^(.*?)\n", re.M)
        self.notes = {}
        self.content = ""

    def startElement(self, name, attrs):
        self.content = ""

    def characters(self, content):
        self.content += content.strip()

    def endElement(self, name):
        if name == "content":
            cnt = base64.b64decode(self.content).decode("utf-8")
            try:
                ttl = self.p.search(cnt).group(1)
                self.notes[ttl] = cnt
            except (AttributeError):
                self.notes[""] = cnt
                pass

    def get_notes(self):
        return self.notes


handler = NoteHandler()


def convert():
    print(handler.get_notes())


def parsing(f):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(f)
    convert()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', metavar='datafile', type=str,
                        help='the file which contains the ResophNotes data')
    args = parser.parse_args()
    parsing(args.f)


if __name__ == "__main__":
    main()
