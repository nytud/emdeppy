
# emDepPy
A wrapper and REST API implemented in Python for __emDep__ (Bohnet parser a.k.a. Mate Tools).

## Requirements

  - _(Included in this repository)_ [Mate Tools parser](http://www.ims.uni-stuttgart.de/forschung/ressourcen/werkzeuge/matetools.en.html) compiled (stripped from [Magyarlánc 3.0](https://github.com/antaljanosbenjamin/magyarlanc/tree/b558823b2d1f9cdc0b5c0ad93b628e96fe251cc1))
  - _(Included in this repository)_ Modelfile for the parser (stripped from [e-magyar](https://github.com/dlt-rilmta/hunlp-GATE/tree/7a75b470753da7e655796c0b1bcaa97e8e143540))
  - Java JRE as in Aptfile (for building dependencies)
  - Python 3 (tested with 3.6)
  - Pip to install the additional requirements in requirements.txt
(MUST BE DONE IN TWO STEPS! -- as written in 'Install on local machine')

## Install on local machine

  - Install [git-lfs](https://git-lfs.github.com/)
  - `git-lfs install` 
  - Clone the repository: `git clone https://github.com/dlt-rilmta/emdeppy` (It should clone the model file also!)
  - ``sudo apt install `cat Aptfile` ``
  - `sudo pip3 install Cython`
  - `sudo pip3 install -r requirements.txt`
  - Use from Python

## Usage

```python
>>> import emdeppy.emdeppy as emdep
>>> p = emdep.EmDepPy('szk.mate.model')
>>> ex = 'A a Det SubPOS=f\n' \
         'kutya kutya N SubPOS=c|Num=s|Cas=n|NumP=none|PerP=none|NumPd=none\n' \
         'elment elmegy V SubPOS=m|Mood=i|Tense=s|Per=3|Num=s|Def=n\n' \
         'sétálni sétál V SubPOS=m|Mood=i|Tense=s|Per=none|Num=p|Def=n\n' \
         '. . . _'
>>> sentence = ex.split('\n')  # Like reading a file with open()
>>> print(list(p.parse_sentence(sentence)))
...
>>> p.parse_stream(ex)  # Same as parse_sentence, but sentences are separated with empty lines (like CoNLL-* fomrat)
...
```

`szk.mate.model` is the previously trained model file (eg. from Szeged Korpusz).

`parse_sentence` takes one sentence as a list of tokens,
a token is a wsp-separated list of 4 fields:
string, lemma, pos, feature.
It returns an iterator by tokens with 7 fields:
id, string, lemma, pos, feature, depTarget, depType.

`parse_stream` Parses multiple sentences which are separated with newlines like in the CoNLL-* formats (uses `parse_sentence` internally)

## License

This Python wrapper is licensed under the LGPL 3.0 license.
The model and the included jar file have their own licenses.
