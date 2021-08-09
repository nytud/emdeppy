
# emDepPy
A wrapper and REST API implemented in Python for __emDep__ (Bohnet parser a.k.a. Mate Tools).

__WARNING__: This module is not thread-safe! [One can not load multiple models simultaneously!](https://code.google.com/archive/p/mate-tools/issues/2)

__WARNING__: This wrapper is only compatible with [JAVA 11](https://askubuntu.com/questions/1037646/why-is-openjdk-10-packaged-as-openjdk-11/1037655#1037655) or higher!

## Requirements

  - _(Included in this repository)_ [Mate Tools parser](http://www.ims.uni-stuttgart.de/forschung/ressourcen/werkzeuge/matetools.en.html) compiled (stripped from [Magyarlánc 3.0](https://github.com/antaljanosbenjamin/magyarlanc/tree/b558823b2d1f9cdc0b5c0ad93b628e96fe251cc1))
  - _(Included in this repository)_ Modelfile for the parser (stripped from [e-magyar](https://github.com/dlt-rilmta/hunlp-GATE/tree/7a75b470753da7e655796c0b1bcaa97e8e143540))
  - Java JRE as in Aptfile (for building dependencies)
  - Python 3 (tested with 3.6)
  - Pip to install the additional requirements in requirements.txt

## Install on local machine

  - Install [git-lfs](https://git-lfs.github.com/)
  - `git-lfs install` 
  - Clone the repository: `git clone https://github.com/dlt-rilmta/emdeppy` (It should clone the model file also!)
  - ``sudo apt install `cat Aptfile` ``
  - `make build`
  - `sudo pip3 install dist/*.whl`
  - Use from Python

## Usage

It is recommended to use the program as the part of [_e-magyar_ language processing framework](https://github.com/dlt-rilmta/emtsv).

If all columns are already exists one can use `python3 -m emdeppy` with the unified [xtsv CLI API](https://github.com/dlt-rilmta/xtsv#command-line-interface).

When `--maxlen [n: Int > 0]` is supplied only sentences with at least n tokens are parsed longer ones get `_` for all fields.

## Train

The training is currently available from JAVA CLI only:

1. `cat SzegedDep/*.conll-2009 | awk -F$'\t' -v OFS=$'\t' '{if ($0 != "") print $0,"_","_","_","_","_","_","_"; else print $0}{}' > train_corpus.txt`
2. `empdejava -Xmx2G -classpath ./emdeppy/anna-3.61.jar is2.parser.Parser -model szk.mate.new.model -train train_corpus.txt`

For more training parameters see the [documentation](https://code.google.com/archive/p/mate-tools/wikis/Training.wiki) or the [source code](https://code.google.com/archive/p/mate-tools/source/default/source).

## License

This Python wrapper is licensed under the LGPL 3.0 license.
The model and the included jar file have their own licenses.
