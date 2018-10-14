import collections
from pprint import pprint
from Sentence import Sentence
import sys
PARTS_OF_SPEECH = ['noun', 'verb', 'inf', 'prep', 'phi', 'fin']

def is_transition_line(u, v):
    return u in PARTS_OF_SPEECH and v in PARTS_OF_SPEECH

class Viterbi:
    def __init__(self, probs_path):
        self.transition_probs, self.emission_probs = self.load_data(probs_path)

    def load_data(self, probs_path):
        transition_probs = collections.defaultdict(lambda: 0.0001)
        emission_probs = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0001))
        with open(probs_path, 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                if line:
                    [u, v, prob] = line.split(' ')
                    prob = float(prob)
                    if is_transition_line(u, v):
                        transition_probs[(u,v)] = prob
                    else:
                        emission_probs[u][v] = prob
        return transition_probs, emission_probs

def load_sents(sents_path):
    sentences = []
    with open(sents_path, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            if line:
                sentences.append(line.split(' '))   
    return sentences

def main(probs_path, sents_path):
    vit = Viterbi(probs_path)

    sentences = load_sents(sents_path)

    sentences = [Sentence(words, vit) for words in sentences]
    
    for sentence in sentences:
        sentence.tag()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise AssertionError('A path to a probabilities file and a sentences file must be provided.')
    [_, probs_path, sents_path] = sys.argv
    main(probs_path, sents_path)