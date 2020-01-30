#!/usr/bin/python3
import random


class LexicalReduplicate:
    file_name = 're.txt'
    vowels = ['а', 'е', 'е', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']
    changeable = ['а', 'е', 'и', 'о']

    def __init__(self):
        self.prefixes = []

    def run(self):
        """function starts the reduplicator"""
        self.request_prefixes()
        self.result = self.make_reduplication()

    def request_prefixes(self):
        """function prompts the user for three prefixes"""
        while len(self.prefixes) != 3:
            print(f'Please enter the prefix No. {len(self.prefixes) + 1}')
            word = input()
            if not word.isdigit():
                self.prefixes.append(word)

    def select_prefix(self):
        """This function selects the prefix"""
        rd = random.randint(0, 2)
        return self.prefixes[rd]

    def make_reduplication(self):
        """the function makes text reduplication according to a given prefix"""
        result_list = []
        with open(self.file_name, encoding="windows-1251") as file:
            for line in file:
                split_line = line.split()
                result = []
                for word in split_line:
                    current_prefix = self.select_prefix()
                    if len(word) < 4 or word.isdigit():
                        result.append(f'{word}')
                    else:
                        result.append(self.word_analyze(word, current_prefix))
                result_list.append(' '.join(result))
        return result_list

    def word_analyze(self, word, prefix):
        """the function analyzes the word for punctuation
            and hyphenated characters."""
        current_word = word
        punctuation_marks = [',', '.', '?', '!']
        punctuation = ''
        result = []
        if current_word[-1] in punctuation_marks:
            punctuation = current_word[-1]
            current_word = current_word[:-1]
        if current_word[2] in self.vowels:
            current_prefix = self.change_prefix_form(prefix, current_word[2:])
            result.append(f'{current_word}-{current_prefix}{current_word[3:]}')
        else:
            current_prefix = self.change_prefix_form(prefix, current_word[1:])
            result.append(f'{current_word}-{current_prefix}{current_word[2:]}')
        if punctuation != '':
            result.append(punctuation)
        return ''.join(result)

    def change_prefix_form(self, prefix, word):
        """this function changes the prefix form"""
        prefix_end = prefix[-1]
        word_start = word[0]
        if prefix_end in self.changeable and word_start in self.changeable:
            if (prefix_end == 'е' and word_start == 'а') \
                    or (prefix_end == 'а' and word_start == 'е'):
                return f'{prefix[:-1]}я'
            if (prefix_end == 'е' and word_start == 'и') \
                    or (prefix_end == 'и' and word_start == 'е'):
                return f'{prefix[:-1]}и'
            if (prefix_end == 'е' and word_start == 'о') \
                    or (prefix_end == 'о' and word_start == 'е'):
                return f'{prefix[:-1]}ё'
        return prefix


if __name__ == '__main__':
    red = LexicalReduplicate()
    red.run()
    for line in red.result:
        print(line)
