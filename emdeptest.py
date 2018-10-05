# -*- coding: utf-8 -*-

# files={'file':open('parse_test.hfst', encoding='UTF-8')}

import emdeppy.emdeppy as emdep
p = emdep.EmDepPy('szk.mate.model')

ex = 'A	a	Det	SubPOS=f\n' \
     'kutya	kutya	N	SubPOS=c|Num=s|Cas=n|NumP=none|PerP=none|NumPd=none\n' \
     'elment	elmegy	V	SubPOS=m|Mood=i|Tense=s|Per=3|Num=s|Def=n\n' \
     '.	.	.	_'

#with open('parse_test.hfst', 'r') as f:
#    ex = f.read()

p.parse_sentence(ex)  # Returns an iterator by tokens (id, token, lemma, pos, features, heads, labels)
#p.parse_stream(ex)  # Same as parse_sentence, but sentences are separated with empty lines

