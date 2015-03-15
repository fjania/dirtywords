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

    def generate_word(self):
        string_size = self.past + random.randint(0, 1)

        seed = random.sample(self.word_set,1)[0]
        s = seed[0:self.past]
        generated_word = s

        for i in range(string_size):
            next_letters = self.cache.get(s, [])

            if not next_letters:
                return None

            next_letter = random.choice(next_letters)
            generated_word += next_letter
            s = s[1:] + next_letter

        return generated_word

    def run_test(self, count):
        self.real_words = []
        self.fake_words = []

        for i in range(count):
            w = self.generate_word()
            if not w is None:
                is_word = w in self.word_set
                if is_word:
                    #real_words.append("[{}]".format(w))
                    self.real_words.append("{}".format(w))
                else:
                    self.fake_words.append(w)

        print "After {} attempts to generate words ({} successful)".format(
            count,
            len(self.real_words)+len(self.fake_words)
        )
        print "{:<20s}{}".format("Words", len(self.real_words))
        print "{:<20s}{}".format("Non-Words", len(self.fake_words))

    def create_board(self, words_to_show, real_words_to_show):
        fake_words_to_show = words_to_show - real_words_to_show

        word_list_to_show = []
        for _ in range(real_words_to_show):
            word = random.sample(self.word_set,1)[0]
            word_list_to_show.append(self.words[word])

        while fake_words_to_show > 0:
            word = self.generate_word()
            if word and not word in self.word_set:
                word_list_to_show.append({
                    'w': word
                })
                fake_words_to_show += -1

        random.shuffle(word_list_to_show)
        return word_list_to_show
