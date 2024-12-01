import nltk
import os.path as path
import re

from functools import partial
from itertools import filterfalse
from nltk.corpus import stopwords, wordnet as wn
from nltk.data import find
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from toolz import compose_left as compose, unique
from toolz import compose_left as compose
from typing import Callable, Iterable

_tokenize: Callable[[str], Iterable[str]] = \
    compose(re.compile(r'[^\s!"&()+,\-./:;?\[\]{{}}][^\s!"()+\-/:;?\[\]{{}}]*[^\s!"()+,\-./:;?\[\]{{}}®™]')
              .finditer,
            partial(map, re.Match.group))

def _ensure_nltk_data(names: Iterable[str]) -> None:
    for name in names:
        try:
            find(name)
        except LookupError:
            nltk.download(path.basename(name))


_ensure_nltk_data(('corpora/omw-1.4', 'corpora/stopwords', 'corpora/wordnet', 'taggers/averaged_perceptron_tagger_eng',
                   'tokenizers/punkt'))

_lemmatizer = WordNetLemmatizer()

def _map_to_wordnet_pos(words: Iterable[tuple[str, str]]) -> Iterable[tuple[str] | tuple[str, str]]:
    for word, pos in words:
        match pos:
            case 'JJ' | 'JJR' | 'JJS' | 'PDT' | 'RP':
                yield word, wn.ADJ
            case 'CD' | 'NN' | 'NNS' | 'NNP' | 'NNPS':
                yield word, wn.NOUN
            case 'VB' | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ':
                yield word, wn.VERB
            case 'EX' | 'IN' | 'RB' | 'RBR' | 'RBS':
                yield word, wn.ADV
            case _: # Other tags have no equivalent in WordNet.
                yield word, None

def _lemmatize_tagged_words(tagged_words: Iterable[str]) -> Iterable[tuple[str, str | None]]:
    for word, pos in tagged_words:
        if pos is not None and word != (lemma := _lemmatizer.lemmatize(word, pos)):
            yield lemma # The lemmatized form takes precedence over the original.
        else:
            yield word # Cannot lemmatize? Just return the word back.

lemmatize: Callable[[str], Iterable[tuple[str, str | None]]] = \
    compose(str.lower,
            _tokenize,
            partial(filterfalse, frozenset(stopwords.words('english')).__contains__),  # Filter out stop words.
            tuple,  # The next function does not work with Iterables, so it needs to be converted into a tuple.
            pos_tag,  # Tag each token (or “word”) with a part of speech (POS).
            _map_to_wordnet_pos,  # Map NLTK’s POS tags to WordNet’s tags.
            _lemmatize_tagged_words,
            ' '.join)
