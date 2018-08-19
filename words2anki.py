import genanki
import random
import hashlib
import json
import codecs
import sys
import argparse

WORDEXTRACT_MODEL_ID = 1143492387
WORDEXTRACT_SALT = '1996795313'

model = genanki.Model(WORDEXTRACT_MODEL_ID,
        'wordextract',
        fields=[{'name': 'Japanese'},{'name':'English'}],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<span style="font-size: 30px" lang="ja">{{Japanese}}</span>',
                'afmt': '{{FrontSide}}<hr id="answer"><span lang="ja">{{English}}</span>',
            },
        ])

parser = argparse.ArgumentParser(description='convert list of json dict entries to anki deck')
parser.add_argument('-N',
        dest='levels',
        metavar='N',
        type=int,
        action='append',
        help='JLPT levels to include; use 0 for unrecognized')
parser.add_argument('--name',
        dest='name',
        type=str,
        help='The name of the Anki deck, for example the name of the book that the words are from')
parser.add_argument('files',
        metavar='FILE',
        type=str,
        action='append',
        nargs='*',
        help='files to read words from; will read stdin if no files are supplied')

blocks = [(0x3040,0x309f),(0x30a0,0x30ff),(0x31f0,0x31ff),(0xff66,0xff9d),(0x1b000,0x1b0ff)]

def is_kana(chr):
    return any([chr >= b and chr <= e for b, e in blocks])

def all_kana(s):
    return all([is_kana(ord(c)) for c in s])


if __name__ == '__main__' and '__file__' in globals():
    args = parser.parse_args()

    deckname = args.name
    if deckname.strip() == '':
        print('Must supply deck name with --name')
        sys.exit(1)

    m = hashlib.sha256()
    m.update((deckname + WORDEXTRACT_SALT).encode('utf8'))
    deck_id = int.from_bytes(m.digest()[0:4], byteorder='little')
    deck = genanki.Deck(deck_id, deckname)

    def add_note(line):
        j = json.loads(line)
        japanese = j['word']
        if all_kana(japanese):
            return
        english = '(unknown)'
        dict_ = j['dict']
        if len(dict_) > 0:
            english = ''
            intr = ''
            for d in dict_:
                english += intr + d['definition'].replace('\n', ' | ') + ' (' + d['dict'] + ')'
                intr = '<br>'

        deck.add_note(genanki.Note(model=model, fields=[japanese, english]))

    if len(args.files[0]) == 0:
        for line in sys.stdin:
            add_note(line)
        for fname in args.files[0]:
            with codecs.open(fname, 'r', 'utf8') as f:
                for line in f:
                    add_note(line)

    genanki.Package(deck).write_to_file(deckname + '.apkg')

