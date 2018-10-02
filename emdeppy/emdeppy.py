#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
from itertools import count

# Set JAVA_HOME for this session
try:
    os.environ['JAVA_HOME']
except KeyError:
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

# Set path for PurePOS for this session
curr_dir = os.path.dirname(__file__)

os.environ['CLASSPATH'] = os.path.join(curr_dir, 'anna-3.61.jar')

# Set path and import jnius for this session
from jnius import autoclass


class EmDepPy:
    def __init__(self, model_file='szk.mate.model'):
        if not os.path.isabs(model_file):
            model_file = os.path.normpath(os.path.join(curr_dir, model_file))
        self._parser = autoclass('is2.parser.Parser')(model_file)

    def parse_sentence(self, lines):
        # Create a sentence class
        sentence_data = autoclass('is2.data.SentenceData09')()

        # Init Arrays for the text
        forms = ['<root>']
        lemmas = ['<root-LEMMA>']
        poss = ['<root-POS>']
        features = ['<no-type>']

        # Read the text from TSV style input
        for line in lines:
            curr_form, curr_lemma, curr_pos, curr_feats = line.strip().split()
            forms.append(curr_form)
            lemmas.append(curr_lemma)
            poss.append(curr_pos)
            features.append(curr_feats)

        # Init sentence class
        sentence_data.init(forms)
        sentence_data.setLemmas(lemmas)
        sentence_data.setPPos(poss)
        sentence_data.setFeats(features)

        # Parse
        out = self._parser.apply(sentence_data)

        # Return output as an iterator over tokens...
        return zip(count(start=1), out.forms, out.plemmas, out.ppos, out.pfeats, out.pheads, out.plabels)

    def parse_stream(self, stream):
        lines = []
        for line in stream:
            line = line.strip()
            if len(line) == 0:
                for n, f, lemm, p, f, h, labels in self.parse_sentence(lines):
                    yield '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(n, f, lemm, p, f, h, labels).encode('UTF-8')
                yield b'\n'
                lines = []
            else:
                lines.append(line)
        if len(lines) > 0:
            for n, f, lemm, p, f, h, labels in self.parse_sentence(lines):
                yield '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(n, f, lemm, p, f, h, labels).encode('UTF-8')


if __name__ == '__main__':
    dep_parser = EmDepPy()

    ex = 'A a Det SubPOS=f\n' \
         'kutya kutya N SubPOS=c|Num=s|Cas=n|NumP=none|PerP=none|NumPd=none\n' \
         'elment elmegy V SubPOS=m|Mood=i|Tense=s|Per=3|Num=s|Def=n\n' \
         'sétálni sétál V SubPOS=m|Mood=i|Tense=s|Per=none|Num=p|Def=n\n' \
         '. . . _'

    for i, form, lemma, pos, feat, head, label in dep_parser.parse_sentence(ex.split('\n')):
        print(i, form, lemma, pos, feat, head, label, sep='\t')
