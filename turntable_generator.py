#!/bin/bash python
'''
Generates a turntable using words from a curated list on GitHub:
https://github.com/dolph/dictionary/blob/master/popular.txt
'''

import random
import sys
from typing import Dict, List, FrozenSet, Set, Tuple

from numpy import character

WORDS_FILENAME = "popular.txt"
NUM_LETTERS = 7
NUM_WORDS_MAX = 50
NUM_WORDS_MIN = 25


# Reads a file of line separated words into a dictionary of word -> character set
def process_words_from_file(filename: str) -> Dict[str, FrozenSet[character]]:
    words_to_charsets = dict()
    with open(filename) as f:
        for line in f.read().splitlines():
            word = line.lower()
            charset = frozenset(word)
            if len(word) > 3 and (len(word) <= NUM_LETTERS or len(charset) <= NUM_LETTERS):
                words_to_charsets[word] = charset
    return words_to_charsets


# Get all words with exactly NUM_LETTERS distinct characters
def get_pentagrams(words_to_charsets: Dict[str, FrozenSet[character]]) -> List[str]:
    return [w for w, c in words_to_charsets.items() if len(c) == NUM_LETTERS]


# Get all DISTINCT character sets of pentagrams along with their pentagrams
def get_penta_charsets(words_to_charsets: Dict[str, FrozenSet[character]]) -> Dict[FrozenSet[character], Set[str]]:
    penta_charsets = dict()
    for w, c in words_to_charsets.items():
        if len(c) == NUM_LETTERS:
            if c not in penta_charsets:
                penta_charsets[c] = set()
            penta_charsets[c].add(w)
    return penta_charsets


# Generate answers for each letter as a central letter for a selected pentagram character set
def get_words_for_penta_charset(penta_charset: FrozenSet[character],
                                words: Dict[str, FrozenSet[character]]) -> Dict[character, Set[str]]:
    answers = dict()
    viable_words = {w: c for w, c in words.items() if c.issubset(penta_charset)}
    print(f"The number of viable words for {penta_charset} is {len(viable_words)}")
    for c in penta_charset:
        answers[c] = [w for w in viable_words if c in words[w]]
    return answers


# Prints details of the valid answers given a pentagram
def print_answers_details(penta_charset: FrozenSet[character],
                          charsets_to_pentagrams: Dict[FrozenSet[character], Set[str]],
                          answers: Dict[character, Set[str]], file=sys.stdout) -> None:
    print("-------------------------------------------------------------------", file=file)
    print(f"For character set: {penta_charset}", file=file)
    for c, s in answers.items():
        print(f"The number of answers with center {c} is {len(s)}", file=file)
    print(f"Valid pentagrams: {charsets_to_pentagrams[penta_charset]}", file=file)
    print("-------------------------------------------------------------------", file=file)


# Separate pentagram charsets into usable ones vs not
def discern_penta_charsets(penta_charsets: Dict[FrozenSet[character], Set[str]], words: Dict[str, FrozenSet[character]]) \
                        -> Tuple[Dict[str, Dict[character, Set[str]]], Dict[str, Dict[character, Set[str]]]]:
    good_pentagrams = dict()
    bad_pentagrams = dict()

    with open("good_pentagrams.txt", "w+") as g:
        with open("bad_pentagrams.txt", "w+") as b:
            for c in penta_charsets:
                answers = get_words_for_penta_charset(c, words)
                is_good = False
                for _, s in answers.items():
                    is_good = len(s) >= NUM_WORDS_MIN and len(s) <= NUM_WORDS_MAX
                if is_good:
                    good_pentagrams[c] = answers
                    print_answers_details(c, penta_charsets, answers, g)
                else:
                    bad_pentagrams[c] = answers
                    print_answers_details(c, penta_charsets, answers, b)
    return good_pentagrams, bad_pentagrams


# Much faster function that just randomly tries to find a good pentagram. Results not guaranteed.
def try_random_penta(words: Dict[str, FrozenSet[character]], penta_charsets: Dict[FrozenSet[character], Set[str]]):
    random_penta_charset = list(penta_charsets.keys())[random.randint(0, len(penta_charsets))]
    answers = get_words_for_penta_charset(random_penta_charset, words)
    print_answers_details(random_penta_charset, penta_charsets, answers)


def main():
    words_to_charsets = process_words_from_file("popular.txt")
    penta_charsets = get_penta_charsets(words_to_charsets)
    # good, bad = discern_penta_charsets(penta_charsets, words_to_charsets)
    # print(len(good))
    # print(len(bad))
    try_random_penta(words_to_charsets, penta_charsets)
    return

if __name__ == "__main__":
    main()