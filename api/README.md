
## Installation

If you don't have a python environment configured yet, you can follow the instruction on the pyenv github page https://github.com/pyenv/pyenv#installation until you succesfully run 

<code>pyenv init -</code>

You'll need to install python 3.9 dependencies: https://devguide.python.org/setup/#build-dependencies. Then run

<code>pyenv install 3.9.10</code>

### Install pyenv-virtualenv
If you need a new virtual environment, make sure to install pyenv-virtualenv, by following the instruction on https://github.com/pyenv/pyenv-virtualenv

### Create the project environment

<code>pyenv virtualenv 3.9.10 Matcha_3_9_10</code>

### Activate virtualenv and the env
- <code>eval "$(pyenv init -)"
- eval "$(pyenv virtualenv-init -)"
- pyenv activate Matcha_3_9_10</code>

### Install dependencies

<code>pip install -r requirements.txt</code>

### Run the application
- export FLASK_APP=flaskr
- export FLASK_ENV=development
- flask init-db
- flask run

### Explore db
- cd instance
- sqlite3 flaskr.sqlite