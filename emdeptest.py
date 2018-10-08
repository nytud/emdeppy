# -*- coding: utf-8 -*-

import emdeppy.emdeppy as emdep 
# load Szeged Korpusz model
p = emdep.EmDepPy('szk.mate.model')

# example sentence, wsp-separated fields: wordform, lemma, pos, feature
ex = 'A a Det SubPOS=f\n' \
  'kutya kutya N SubPOS=c|Num=s|Cas=n|NumP=none|PerP=none|NumPd=none\n' \
  'elment elmegy V SubPOS=m|Mood=i|Tense=s|Per=3|Num=s|Def=n\n' \
  'sétálni sétál V SubPOS=m|Mood=i|Tense=s|Per=none|Num=p|Def=n\n' \
  '. . . _'

sentence = ex.split('\n')

# in: list of words (= 4 field lines)
# out: returns an iterator by tokens (id, string, lemma, pos, feature, depTarget, depType)
print(list(p.parse_sentence(sentence)))


# TODO: stream
# files={'file':open('parse_test.hfst', encoding='UTF-8')}
#with open('parse_test.hfst', 'r') as f:
#    ex = f.read()
#p.parse_stream(ex)  # Same as parse_sentence, but sentences are separated with empty lines

