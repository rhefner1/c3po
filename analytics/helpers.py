"""These are the map, reduce and other helper functions to support the
analysis piplines."""

import logging
import re
import string


def clean_text(text):
    text = text.encode('utf-8', 'ignore')

    trans_punctuation = string.punctuation
    trans_replace = ' ' * len(trans_punctuation)
    translator = string.maketrans(trans_punctuation, trans_replace)

    return text.translate(translator).strip().lower()


def split_into_words(text):
    """Split a sentence into list of words."""
    regex = re.compile(r'\S+\s*')
    text = clean_text(text)
    words = [w.strip() for w in re.findall(regex, text)]
    return [w for w in words if w is not None]


def word_count_map(msg):
    """Word count map function."""
    if msg.text:
        for word in split_into_words(msg.text):
            yield (word, None)


def word_count_reduce(key, values):
    """Word count reduce function."""
    logging.info("WOMBAT REDUCING KEY %s w/vals %s", key, values)
    yield "%s: %d\n" % (key, len(values))


def reduce_map(readbuffer):
    """Word count map function."""
    while True:
        try:
            line = readbuffer.readline()
            if not line:
                break
            logging.info("WOMBAT READBUFFER LINE %s", line)
            yield (line, None)
        except StopIteration:
            break


def reduce_reduce(key, values):
    """Word count reduce function."""
    logging.info("WOMBAT REDUCING KEY %s w/vals %s", key, values)
    yield key
