import collections
import math
from pprint import pprint

PARTS_OF_SPEECH = ['noun', 'verb', 'inf', 'prep']


class Sentence:
    def __init__(self, words, transition_probs, emission_probs):
        self.sentence = ' '.join(words)
        self.words = words
        self.transition_probs = transition_probs
        self.emission_probs = emission_probs
        self.PI = self.__init_table()
        self.BP = self.__init_table()
        self.S = {
            -1: ['phi']
        }
        for i in range(len(self.words)):
            self.S[i] = PARTS_OF_SPEECH

    def __init_table(self):
        table = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))
        table[-1]['phi'] = 1
        return table

    def __probability(self, k, v, w):
        lookup_prob = self.PI[k - 1][w]
        transition_prob = math.log(self.transition_probs[(v, w)])
        emission_prob = math.log(self.emission_probs[self.words[k]][v])
        return lookup_prob + transition_prob + emission_prob

    def tag(self):
        print(f'PROCESSING SENTENCE: {self.sentence}\n')
        viterbi_output = "FINAL VITERBI NETWORK\n\n"
        bp_output = "FINAL BACKPOINTER NETWORK\n\n"
        n = len(self.words)
        for k in range(n):
            for v in self.S[k]:
                max_probability = self.__probability(k, v, v)
                max_arg = v
                for w in self.S[k-1]:
                    pi = self.__probability(k, v, w)
                    if pi > max_probability:
                        max_probability = pi
                        max_arg = w
                self.PI[k][v] = max_probability
                self.BP[k][v] = max_arg
                viterbi_output += f"P({self.words[k]} = {v}) = {'{0:0.10f}'.format(math.e**max_probability)}\n"
                if k > 0:
                    bp_output += f"Backptr({self.words[k]} = {v}) = {max_arg}\n"

        print(viterbi_output)
        print(bp_output)

        self.traceback()

    def traceback(self):
        i = len(self.words) - 1
        max_tag, max_prob = max(self.PI[i].items(), key=lambda x: x[1])
        print(
            f'BEST TAG SEQUENCE HAS PROBABILITY {"{0:0.10f}".format(math.e ** max_prob)}')
        tags = [max_tag]
        while i >= 0:
            tags.append(self.BP[i][tags[-1]])
            i -= 1
        tags.reverse()

        for a, b in zip(self.words, tags[1:]):
            print(a, b, sep=' -> ')
        print('\n')
