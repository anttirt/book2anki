# book2anki
Convert a Japanese ebook to a jp->en flash card deck for Anki

## What is this

A dirty little script that generates an Anki deck from a Japanese HTML ebook.
The ebook must contain its text within fully closed paragraph tags (`<p>こんにちは！</p>`).

### Requirements

* bash
* JDK 10
* Maven
* Python 3
* [sdcv](https://dushistov.github.io/sdcv/)

### Usage:

#### Setup/build:

```bash
pushd res
    for f in *.bz2; do tar xf $f; done
popd
./env-setup.sh
mvn compile assembly:single
```

#### To extract words from a book:

```bash
# This will produce "My Book.apkg" which can be imported into Anki.
./book2anki mybook.html 'My Book'
```

### Resources:

* [JLPT word lists](https://www.thbz.org/kanjimots/jlpt.php3)
* [kuromoji](https://github.com/atilika/kuromoji)
* [The JMDict Project](http://www.edrdg.org/jmdict/j_jmdict.html)
* [stardict format files for JMDict dictionaries](http://download.huzheng.org/ja/)
* [genanki](https://github.com/kerrickstaley/genanki)
