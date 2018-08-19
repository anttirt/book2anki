import codecs
import sys
import argparse

with codecs.open('res/jlpt-voc-1.utf', 'r', 'utf8') as f:
    lines1 = f.readlines()
with codecs.open('res/jlpt-voc-2.utf', 'r', 'utf8') as f:
    lines2 = f.readlines()
with codecs.open('res/jlpt-voc-3.utf', 'r', 'utf8') as f:
    lines3 = f.readlines()
with codecs.open('res/jlpt-voc-4.utf', 'r', 'utf8') as f:
    lines4 = f.readlines()

allwords = []

for words, N in [(lines1, 1), (lines2, 2), (lines3, 3), (lines4, 4)]:
    allwords += [
        (line.strip().split(' ')[0], N)
        for line
        in words
        if line[0] != '#' and line.strip() != ''
    ]

allwords = { w[0]: w[1] for w in allwords }

parser = argparse.ArgumentParser(description='filter words based on JLPT level')
parser.add_argument('-N',
        dest='levels',
        metavar='N',
        type=int,
        action='append',
        help='JLPT levels to include; use 0 for unrecognized')
parser.add_argument('files',
        metavar='FILE',
        type=str,
        action='append',
        nargs='*',
        help='files to read from; will read stdin if no files are supplied')

def filter_line(levels, line):
    n = allwords.get(line.strip(), None)
    if len(levels) == 0:
        sys.stdout.buffer.write((line[:-1] + ' ' + str(n) + '\n').encode('utf8'))
    elif n is None:
        if 0 in levels:
            sys.stdout.buffer.write(line.encode('utf8'))
    elif n in levels:
        sys.stdout.buffer.write(line.encode('utf8'))

if __name__ == '__main__' and '__file__' in globals():
    args = parser.parse_args()

    levels = args.levels or []

    if len(args.files[0]) == 0:
        for line in sys.stdin:
            filter_line(levels, line)
    else:
        for fname in args.files[0]:
            with codecs.open(fname, 'r', 'utf8') as f:
                for line in f:
                    filter_line(levels, line)

