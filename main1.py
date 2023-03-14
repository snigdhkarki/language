import itertools
from nltk.corpus import wordnet

nouns = sorted(list(set(
            itertools.chain.from_iterable([n.replace('_', ' ') for n in synset.lemma_names()] for synset in wordnet.all_synsets('n'))
        )), key=str.casefold)

with open('nouns.txt', 'w', encoding='utf-8') as outfile:
    print(*nouns, sep='\n', file=outfile)