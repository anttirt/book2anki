from html.parser import HTMLParser
import codecs
import sys

class Textractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.care = [False]
        self.text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.text += '\n'
            self.care.append(True)
        elif tag == 'ruby':
            self.care.append(True)
        elif tag == 'rt':
            self.care.append(False)

    def handle_endtag(self, tag):
        if tag == 'p' or tag == 'ruby' or tag == 'rt':
            self.care = self.care[:-1]

    def handle_data(self, data):
        if self.care[-1]:
            self.text += data

t = Textractor()
with codecs.open(sys.argv[1], 'r', encoding='utf8') as f:
    text = f.read()

t.feed(text)

sys.stdout.buffer.write(t.text.encode('utf8'))

