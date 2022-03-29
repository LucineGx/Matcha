
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

# API
## /auth
### /register - POST
Form content:
- email (constraints to decide)
- firstname (constraints to decide)
- lastname (constraints to decide)
- password (constraints to decide)

Responses:
- 201: User <user> successfully saved
- 400: <field> is required
- 409: <user> is already registered
- 500: Internal Server Error

### /register/confirm/<token> - GET
Responses:
- 200: User confirmed successfully
- 404: Unknown token
- 500: Internal Server Error

### /login - POST
Form content:
- email
- password

Responses:
- 200: Login successfully
- 404: Unknown token
- 500: Internal Server Error

### /logout - GET
Responses:
- 200: Logout successfully
- 500: Internal Server Error

### /forgot-password - POST
Form content:
- email

Responses:
- 200: If a user is linked to this mail address, a link has been sent to reinitialize the password
- 500: Internal Server Error

### /update-password/<token> - POST
Form content:
- password
Responses:
- 200: Password updated successfully
- 404: Unknown token
- 500: Internal Server Error

## /user
### / - GET
Responses:
- 200: user:
  - id
  - email
  - firstname
  - lastname
  - created_on
  - confirmed
- 500: Internal Server Error

### / - PUT 
Form content:
- email (optional)
- firstname (optional)
- lastname (optional)
- password(optional)

Responses:
- 200: user:
  - id
  - email
  - firstname
  - lastname
  - created_on
  - confirmed
- 500: Internal Server Error

### / - DELETE
Response
- 200: User successfully deleted
- 500: Internal Server Error

You're no longer logged in

## /tag
### /<tag_name> - GET
Create the tag if it doesn't exist yet, assign a random color.

Response
- 200 - tag:
  - id
  - name
  - color