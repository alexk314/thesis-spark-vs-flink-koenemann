#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This application is creating input data for batch processing
# Features:
# - take input param of how many MiB of words are required
# - Create random words file
import os
import socket
import time
import urllib.request  # for retrieving a dictionary for random words
import random  # for selecting random words


class WordFileCreator:
    dictionary = list()


def main():
    import_dictionary()
    target_file_size = set_file_size()
    create_file(target_file_size)
    return 0


def import_dictionary():
    word_input_url = "https://www.mit.edu/~ecprice/wordlist.100000"  # 100.000 words
    response = urllib.request.urlopen(word_input_url)
    WordFileCreator.dictionary = response.read().decode().splitlines()
    print(f"Imported dictionary from MIT with {format(len(WordFileCreator.dictionary), ',d')} words")


def set_file_size():
    print("How many MiB of randoms words shall I create?")
    return int(input())


def take_a_line():
    words_per_line = 10
    random_words = ' '.join(random.sample(WordFileCreator.dictionary, words_per_line)) + "\n"
    return random_words


def take_n_lines(number_of_lines):
    random_lines = ""
    for n in range(number_of_lines):
        random_lines += take_a_line()
    return random_lines


def create_file(file_size_mib):
    file_size_kib = file_size_mib * 1024 * 2014  # just maybe correct
    file_name = str(file_size_mib) + "MiB"
    file_full_of_jibberish = open(file_name, 'w+')  # existing file will be overwritten
    current_size = 0
    while current_size < file_size_kib:
        file_full_of_jibberish.write(take_n_lines(10))
        current_size = os.path.getsize(file_name) * 2
    file_full_of_jibberish.close()


if __name__ == "__main__":
    main()
