otakume ETL
===========

extracts anime data from Anime News Network and
puts in orchestrate with a better and legible format.

etl will also perform a ranking based on a set of features:

- Director
- Cast
- Opening Band
- Ending Band
- Number of episodes
- Anime studio
- Origin
- Creator
- Animation type
- Genre
- Topic
- Year/Season
- Photograph director

##Installation

the first requirement is create a virtual environment for python

$(venv) pip install -r requirements.txt

$(venv) python setup.py

##Configuration

you'll have to modify these files and create a version without "example" suffix:

- client.cfg.example 
- config/orchestrate.yml.example 
