#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
from itertools import count

import jnius_config


def import_pyjnius():
    """
    PyJNIus can only be imported once per Python interpreter and one must set the classpath before importing...
    """
    # Check if autoclass is already imported...
    if not jnius_config.vm_running:

        # Tested on Ubuntu 16.04 64bit with openjdk-8 JDK and JRE installed:
        # sudo apt install openjdk-8-jdk-headless openjdk-8-jre-headless

        # Set JAVA_HOME for this session
        try:
            os.environ['JAVA_HOME']
        except KeyError:
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

        # Set path and import jnius for this session
        from jnius import autoclass
    else:
        import sys
        from jnius import cast, autoclass
        class_loader = autoclass('java.lang.ClassLoader')
        cl = class_loader.getSystemClassLoader()
        ucl = cast('java.net.URLClassLoader', cl)
        urls = ucl.getURLs()
        cp = ':'.join(url.getFile() for url in urls)

        print('Warning: PyJNIus is already imported with the following classpath: {0} Please check if it is ok!'.
              format(cp), file=sys.stderr)

    # Return autoclass for later use...
    return autoclass


class EmDepPy:
    class_path = os.path.join(os.path.dirname(__file__), 'anna-3.61.jar')

    def __init__(self, model_file=os.path.normpath(os.path.join(os.path.dirname(__file__), 'szk.mate.conll.model')),
                 source_fields=None, target_fields=None):
        if not jnius_config.vm_running:
            jnius_config.add_classpath(EmDepPy.class_path)
        self._autoclass = import_pyjnius()
        self._jstr = self._autoclass('java.lang.String')
        self._parser = self._autoclass('is2.parser.Parser')(self._jstr(model_file.encode('UTF-8')))

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = {}

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        out = self.parse_sentence('\t'.join((tok[field_names[0]], tok[field_names[1]], tok[field_names[2]],
                                             tok[field_names[3]])) for tok in sen)
        for tok, out_line in zip(sen, out):
            tok.extend([str(out_line[0]), out_line[6], str(out_line[5])])
        return sen

    @staticmethod
    def prepare_fields(field_names):
        return [field_names['string'], field_names['lemma'], field_names['pos'], field_names['feature']]

    def parse_sentence(self, lines):
        # Create a sentence class
        sentence_data = self._autoclass('is2.data.SentenceData09')()

        # Init Arrays for the text
        forms = [self._jstr(b'<root>')]
        lemmas = [self._jstr(b'<root-LEMMA>')]
        poss = [self._jstr(b'<root-POS>')]
        features = [self._jstr(b'<no-type>')]

        # Read the text from TSV style input
        for line in lines:
            curr_form, curr_lemma, curr_pos, curr_feats = line.strip().split()
            forms.append(self._jstr(curr_form.encode('UTF-8')))
            lemmas.append(self._jstr(curr_lemma.encode('UTF-8')))
            poss.append(self._jstr(curr_pos.encode('UTF-8')))
            features.append(self._jstr(curr_feats.encode('UTF-8')))

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
