import glob
import re

import requests
import nltk
import re
from lxml.html.clean import Cleaner
import  pymorphy2


def get_tokens_from_file(filename):
    tokens = []

    with open(filename, encoding='utf-8') as file:
        content = file.read()
        TAG_RE = re.compile(r'<[^>]+>')
        TAG_NUM = re.compile(r'\d+')
        TAG_UP_RU = re.compile(r'([А-Я][а-я]+[А-Я][а-я]+)')
        TAG_UP_RU2 = re.compile(r'([А-Я][а-я]+[А-Я]+)')
        TAG_UP_RU3 = re.compile(r'([а-я]+[А-Я]+[а-я]+)')
        TAG_UP_RU4 = re.compile(r'([А-Я]+[а-я]+)')
        TAG_UP_RU6 = re.compile(r'([А-Я]+[а-я]+)')
        TAG_UP_RU5 = re.compile(r'([а-я]+[А-Я]+)')
        TAG_UP_RU7 = re.compile(r'([а-я]+[А-Я]+)')
        content = TAG_RE.sub('', content)
        content = TAG_NUM.sub('', content)
        content = TAG_UP_RU.sub('', content)
        content = TAG_UP_RU2.sub('', content)
        content = TAG_UP_RU3.sub('', content)
        content = TAG_UP_RU4.sub('', content)
        content = TAG_UP_RU5.sub('', content)
        content = TAG_UP_RU6.sub('', content)
        content = TAG_UP_RU7.sub('', content)
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(content)

    def pos(word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].tag.POS

    def pos_inflect(word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].lexeme

    remove_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}  # remove
    tokens = [token for token in tokens if
              ((pos(token) not in remove_pos) and (pos(token) is not None) and (len(token) != 1))]

    tokens = list(set(tokens))  # дубликаты

    return tokens


