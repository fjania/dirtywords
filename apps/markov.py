from collections import defaultdict
import json
import random
import string

from apps.wordnet import all_defined_words
from apps.realwords import all_real_words

class MarkovWords:
    def __init__(self, past):
        self.past = past
        self.words = {}

        self.cache = defaultdict(list)
        self.endcache = defaultdict(list)

        for entry in all_defined_words:
            word = entry.get('w')

            if len(word) < self.past:
                continue

            self.words[word] = entry
            until = len(word) - past
            for i in range(until):
                s = word[i:i+self.past + 1]
                key, value = s[0:-1], s[-1]
                if i == until - 1:
                    self.endcache[key].append(value)
                else:
                    self.cache[key].append(value)

    def generate_word(self, word_length):
        seed = random.choice(all_defined_words).get('w')
        s = seed[0:self.past]
        generated_word = s

        until = word_length - self.past + 1
        for i in range(until):
            if i == until - 1:
                next_letters = self.endcache.get(s, [])
            else:
                next_letters = self.cache.get(s, [])

            if not next_letters:
                return None

            next_letter = random.choice(next_letters)
            generated_word += next_letter
            s = s[1:] + next_letter

        return generated_word

    def create_board(self, words_to_show, real_words_to_show):
        fake_words_to_show = words_to_show - real_words_to_show

        word_list_to_show = []
        word_length_min = self.past+1
        word_length_max = self.past+3

        while real_words_to_show > 0:
            word = random.choice(all_defined_words).get('w')
            if len(word) >= word_length_min \
                and len(word) <= word_length_max \
                and self.words[word].get('s') > 10:
                word_list_to_show.append(self.words[word])
                real_words_to_show += -1

        while fake_words_to_show > 0:
            word_length = random.randint(word_length_min, word_length_max)
            word = self.generate_word(word_length)
            if word and not word in all_real_words:
                word_list_to_show.append({
                    'w': word
                })
                fake_words_to_show += -1

        random.shuffle(word_list_to_show)
        return word_list_to_show
