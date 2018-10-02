#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import codecs

from flask import Flask, request, abort, Response, stream_with_context
from flask_restful import Resource, Api

# Import emDepPy wrapper
import emdeppy

# import atexit
import threading

# ##################################################### EDIT THIS ######################################################

model_file_name = 'szk.mate.model'

# ##################################################### EDIT THIS ######################################################


# lock to control access to variable
emdeppy_lock = threading.Lock()

# Initiate
emdeppy_parser = emdeppy.EmDepPy(model_file_name)
# atexit.register(emdeppy_parser.close)

app = Flask(__name__)
api = Api(app)


class EmDepPyREST(Resource):
    @staticmethod
    @app.route('/')
    @app.route('/parse')
    def get():
            return 'Usage: HTTP POST /parse, TSV style file with the fields, wordform, lemma, pos, features' \
                   ' (empty line as sentence separator)'

    @staticmethod
    @app.route('/parse', methods=['POST'])
    def parse():
        if 'file' not in request.files:
            abort(400)
        inp_file = codecs.getreader('UTF-8')(request.files['file'])
        with emdeppy_lock:
            return Response(stream_with_context(emdeppy_parser.parse_stream(inp_file)),  direct_passthrough=True)


if __name__ == '__main__':
    app.run(debug=False)
