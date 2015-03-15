from collections import defaultdict
import json
import random
import string

from apps.wordnet import all_words

class MarkovWords:
    def __init__(self, past):
        self.past = past
        self.words = {}
        self.word_set = set()

        def tuples():
            for entry in all_words:
                word = entry.get('w')
                if len(word) > self.past:
                    self.words[word] = entry
                    self.word_set.add(word)
                    for i in range(len(word) - past):
                        s = word[i:i+self.past + 1]
                        yield s

        self.cache = defaultdict(list)
        for t in tuples():
            key, value = t[0:-1], t[-1]
            self.cache[key].append(value)

    def generate_word(self, word_length):
        seed = random.sample(self.word_set,1)[0]
        s = seed[0:self.past]
        generated_word = s

        for i in range(word_length - self.past + 1):
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
            word = random.sample(self.word_set,1)[0]
            if len(word) >= word_length_min and len(word) <= word_length_max:
                word_list_to_show.append(self.words[word])
                real_words_to_show += -1

        while fake_words_to_show > 0:
            word_length = random.randint(word_length_min, word_length_max)
            word = self.generate_word(word_length)
            if word and not word in self.word_set:
                word_list_to_show.append({
                    'w': word
                })
                fake_words_to_show += -1

        random.shuffle(word_list_to_show)
        return word_list_to_show
