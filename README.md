# SCALAR Part-of-speech tagger
This the official release of the SCALAR Part-of-speech tagger

**NOTE**
There is a fork of SCALAR which was designed to handle parallel http requests and cache SCALAR's output to increase its speed. You can find this version here: https://github.com/brandonscholten/scanl_tagger. These will be combined into a single application in the *very* near future.

## Getting Started with Docker

To run SCNL tagger in a Docker container you can clone the repository and pull the latest docker impage from `srcml/scanl_tagger:latest`

```
git clone https://github.com/brandonscholten/scanl_tagger.git
cd scanl_tagger
docker compose pull
docker compose up
```

## Setup and Run
You will need `python3.10` installed. 

You'll need to install `pip3`

Conosider configuring `PYTHONPATH` as well:

	export PYTHONPATH=~/path/to/scanl_tagger

Install dependencies by running `pip3 install -r requirements.txt` in the root of the repository. 

Finally, we require the `token` and `target` vectors from [code2vec](https://github.com/tech-srl/code2vec). The tagger will attempt to automatically download them if it doesn't find them, but you could download them yourself if you like. It will place them in your local directory under `./code2vec/*`

## Usage

```
usage: main [-h] [-v] [-r] [-t] [-a ADDRESS] [--port PORT] [--protocol PROTOCOL]
            [--words WORDS]

options:
  -h, --help            show this help message and exit
  -v, --version         print tagger application version
  -r, --run             run server for part of speech tagging requests
  -t, --train           run training set to retrain the model
  -a ADDRESS, --address ADDRESS
                        configure server address
  --port PORT           configure server port
  --protocol PROTOCOL   configure whether the server uses http or https
  --words WORDS         provide path to a list of acceptable abbreviations
```

`./main -r` will start the server, which will listen for identifier names sent via HTTP over the route:

http://127.0.0.1:5000/{identifier_name}/{code_context}/{database_name (optional)}

"database name" specifies an sqlite database to be used for result caching and data collection. If the database specified does not exist, one will be created. 

You can check wehther or not a database exists by using the `/probe` route by sending an HTTP request like this:

http://127.0.0.1:5000/probe/{database_name}

"code context" is one of:
- FUNCTION
- ATTRIBUTE
- CLASS
- DECLARATION
- PARAMETER

For example:

Tag a declaration: ``http://127.0.0.1:5000/cache/numberArray/DECLARATION``

Tag a function: ``http://127.0.0.1:5000/cache/GetNumberArray/FUNCTION``

Tag an class: ``http://127.0.0.1:5000/cache/PersonRecord/CLASS``

#### Note
Kebab case is not currently supported due to the limitations of Spiral. Attempting to send the tagger identifiers which are in kebab case will result in the entry of a single noun. 

You will need to have a way to parse code and filter out identifier names if you want to do some on-the-fly analysis of source code. We recommend [srcML](https://www.srcml.org/). Since the actual tagger is a web server, you don't have to use srcML. You could always use other AST-based code representations, or any other method of obtaining identifier information. 

## Training the tagger
You can train this tagger using the `-t` option (which will re-run the training routine). For the moment, most of this is hard-coded in, so if you want to use a different data set/different seeds, you'll need to modify the code. This will potentially change in the future.

## Errors?
Please make an issue if you run into errors

# Please Cite the Paper!

No paper for now however the current tagger is based on our previous, so you could cite the previous one for now: 

Christian  D.  Newman,  Michael  J.  Decker,  Reem  S.  AlSuhaibani,  Anthony  Peruma,  Satyajit  Mohapatra,  Tejal  Vishnoi, Marcos Zampieri, Mohamed W. Mkaouer, Timothy J. Sheldon, and Emily Hill, "An Ensemble Approach for Annotating Source Code Identifiers with Part-of-speech Tags," in IEEE Transactions on Software Engineering, doi: 10.1109/TSE.2021.3098242.

# Training set
The data used to train this tagger can be found in the most recent database update in the repo -- https://github.com/SCANL/scanl_tagger/blob/master/input/scanl_tagger_training_db_11_29_2024.db

# Interested in our other work?
Find our other research [at our webpage](https://www.scanl.org/) and check out the [Identifier Name Structure Catalogue](https://github.com/SCANL/identifier_name_structure_catalogue)

# WordNet
This project uses WordNet to perform a dictionary lookup on the individual words in each identifier:

Princeton University "About WordNet." [WordNet](https://wordnet.princeton.edu/). Princeton University. 2010

