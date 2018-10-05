
# emDepPy
A wrapper and REST API implemented in Python for ___emDep__ (Bohnet parser a.k.a. Mate Tools)_

## Requirements
  
  - (Included in this repository) [Mate Tools parser](http://www.ims.uni-stuttgart.de/forschung/ressourcen/werkzeuge/matetools.en.html) compiled (stripped from [Magyarlánc 3.0](https://github.com/antaljanosbenjamin/magyarlanc/tree/b558823b2d1f9cdc0b5c0ad93b628e96fe251cc1))
  - (Included in this repository) Modelfile for the parser (stripped from [e-magyar](https://github.com/dlt-rilmta/hunlp-GATE/tree/7a75b470753da7e655796c0b1bcaa97e8e143540))
  - Java JDK and Cython as in Aptfile (for building dependencies)
  - Python 3 (tested with 3.6)
  - Pip to install the additional requirements in requirements.txt (MUST BE DONE IN TWO STEPS!)
  - (Optional) a cloud service like [Heroku](https://heroku.com) for hosting the API

## Install on local machine

  - Install [`git-lfs`](https://git-lfs.github.com/)
  - Clone the repository
  - sudo apt install `cat Aptfile`
  - Run: `sudo pip3 install Cython`
  - Run: `sudo pip3 install -r requirements.txt`
  - Use from Python

## Install to Heroku

  - Register
  - Download Heroku CLI
  - Login to Heroku from the CLI
  - Create an app
  - Clone the repository
  - Add Heroku as remote origin
  - Add buildpacks (in the specified order!)
  - Push the repository to Heroku (Beware git-lfs, and pip Cython install!)
  - Enjoy!

## Usage

  - From Python:

	```python
	>>> import emdeppy.emdeppy as emdep
	>>> p = emdep.EmDepPy('szk.mate.model')
	>>> ex = 'A a Det SubPOS=f\n' \
             'kutya kutya N SubPOS=c|Num=s|Cas=n|NumP=none|PerP=none|NumPd=none\n' \
             'elment elmegy V SubPOS=m|Mood=i|Tense=s|Per=3|Num=s|Def=n\n' \
             'sétálni sétál V SubPOS=m|Mood=i|Tense=s|Per=none|Num=p|Def=n\n' \
             '. . . _'
	>>> p.parse_sentence(ex)  # Returns an iterator by tokens (id, token, lemma, pos, features, heads, labels)
	...
	>>> p.parse_stream(ex)  # Same as parse_sentence, but sentences are separated with empty lines
	...
	```

- Through the REST API:
	```python
	>>> import requests
	>>> r = requests.post('http://127.0.0.1:5000/parse', files={'file':open('parse_test.hfst', encoding='UTF-8')})
	>>> print(r.text)
	...
	```

- See test instance on heroku: https://emdeppy.herokuapp.com/


## License

This Python wrapper and the REST API is licensed under the LGPL 3.0 license.
The model and the included jar file have their own licenses.
