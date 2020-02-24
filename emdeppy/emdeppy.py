#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
from itertools import count, repeat

from xtsv import jnius_config, import_pyjnius


class EmDepPy:
    class_path = os.path.join(os.path.dirname(__file__), 'anna-3.61.jar')
    pass_header = True

    def __init__(self, model_file=os.path.normpath(os.path.join(os.path.dirname(__file__), 'szk.mate.ud.model')),
                 maxlen=None, source_fields=None, target_fields=None):
        self._autoclass = import_pyjnius()
        self._jstr = self._autoclass('java.lang.String')
        system = self._autoclass('java.lang.System')
        print_stream = self._autoclass('java.io.PrintStream')
        output_stream = self._autoclass('java.io.OutputStream')
        orig_out = system.out
        orig_err = system.err
        system.setOut(print_stream(output_stream.nullOutputStream()))  # Shut up JAVA!
        system.setErr(print_stream(output_stream.nullOutputStream()))  # Shut up JAVA!
        self._parser = self._autoclass('is2.parser.Parser')(self._jstr(model_file.encode('UTF-8')))
        system.setOut(orig_out)  # Restore handles...
        system.setErr(orig_err)  # Restore handles...

        self._maxlen = maxlen
        if self._maxlen is not None:
            self._parse_sentence = self._parse_sentence_w_maxlen
        else:
            self._parse_sentence = self._parse_sentence_unlimited

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        out = self._parse_sentence(((tok[field_names[0]], tok[field_names[1]], tok[field_names[2]],
                                   tok[field_names[3]]) for tok in sen), len(sen))
        for tok, out_line in zip(sen, out):
            tok.extend([str(out_line[0]), out_line[6], str(out_line[5])])
        return sen

    @staticmethod
    def prepare_fields(field_names):
        return [field_names['form'], field_names['lemma'], field_names['upostag'], field_names['feats']]

    def _parse_sentence_w_maxlen(self, sen, sen_len):
        if sen_len > self._maxlen:
            return repeat(('_', '_', '_', '_', '_', '_', '_'))
        return self._parse_sentence_unlimited(sen, sen_len)

    def _parse_sentence_unlimited(self, lines, _):
        # Create a sentence class
        sentence_data = self._autoclass('is2.data.SentenceData09')()

        # Init Arrays for the text
        forms = [self._jstr(b'<root>')]
        lemmas = [self._jstr(b'<root-LEMMA>')]
        poss = [self._jstr(b'<root-POS>')]
        features = [self._jstr(b'<no-type>')]

        # Read the text from TSV style input
        for curr_form, curr_lemma, curr_pos, curr_feats in lines:
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


if not jnius_config.vm_running:
    jnius_config.add_classpath(EmDepPy.class_path)
