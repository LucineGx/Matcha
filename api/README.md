
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
- python3 -m flask init-db
- python3 -m flask run

### Explore db
- cd instance
- sqlite3 flaskr.sqlite

# API
## /auth
### /register - POST
Form content:
- <b>email (valid mail)
- first_name (32 char max)</b>
- lastname (32 char max)
- <b>password (8 char min, 32 char max, must contain one number, one low-case char and on up-case char)</b>

Responses:
- 201: "User created successfully"
- 400: Validation Error with details
- 409: "<user> is already registered"
- 500: Internal Server Error

### /register/confirm/<token> - GET
Responses:
- 200: "User confirmed successfully"
- 404: "Unknown token"
- 500: Internal Server Error

### /login - POST
Form content:
- <b>email</b>
- <b>password</b>

Responses:
- 200: user:
  - id
  - email
  - firstname
  - lastname
  - created_on
  - confirmed
- 401: "Incorrect email or password"
- 401: "User email is not confirmed"
- 500: Internal Server Error

### /logout - GET
Responses:
- 200: "Logout successful"
- 500: Internal Server Error

### /forgot-password - POST
Form content:
- <b>email</b>

Responses:
- 200: "If a user is linked to this mail address, a link has been sent to reinitialize the password"
- 500: Internal Server Error

### /update-password/<token> - POST
Form content:
- <b>password</b>

Responses:
- 201: "Password updated successfully"
- 400: Validation error with details
- 404: "Unknown token"
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
- 404: "Resource not found"
- 500: Internal Server Error

### / - PUT 
Form content:
- email
- firstname
- lastname
- password

Responses:
- 200: user:
  - id
  - email
  - firstname
  - lastname
  - created_on
  - confirmed
- 400: Validation Error with details
- 500: Internal Server Error

### / - DELETE
Response
- 200: "User successfully deleted"
- 500: Internal Server Error

You're no longer logged in

## /types
### - GET
List all the types available in the app.

Response
- 200: list of types:
  - id
  - name
  - color
- 500: Internal Server Error

## /egg_groups
### - GET
List all the egg groups available in the app.

Response
- 200: list of egg groups:
  - id
  - name
  - color
- 500: Internal Server Error

## /tag
### /<tag_name> - GET
Create the tag if it doesn't exist yet, assign a random color.

Response
- 200: tag:
  - id
  - name
  - color
- 201: tag:
  - id
  - name
  - color
- 400: Validation Error with details
- 500: Internal Server Error

## /profile
### / - POST
Create a profile for the current user.

Form content:
- <b>gender (one of "female", "male", "none")</b>
- <b>level</b> (between 1 and 100)
- search_male (True if in the form, else False)
- search_female (True if in the form, else False)
- search_none (True if in the form, else False)
- short_bio (280 char max)
- <b>type</b> (present in the type table)
- type_2 (present in the type table)
- <b>egg_group</b> (present in the egg_group table)
- egg_group_2 (present in the egg_group_table)

Response
- 201: profile:
  - user_id
  - gender
  - search_male
  - search_female
  - search_none
  - short_bio
  - public_popularity
  - type
  - type_2
  - egg_group
  - egg_group_2
  - level
- 400: Validation Error with details
- 409: "User <email> has already defined a profile"
- 500: Internal Server Error

### / - GET
Response
- 200: profile:
  - user_id
  - gender
  - search_male
  - search_female
  - search_none
  - short_bio
  - public_popularity
  - type_id
  - type_2_id
  - egg_group_id
  - egg_group_2_id
  - level
- 500: Internal Server Error

### / - PUT
Update the current user's profile

Form content:
- gender (one of "female", "male", "none")
- search_male (True if in the form, else False)
- search_female (True if in the form, else False)
- search_none (True if in the form, else False)
- short_bio (280 char max)
- type_id (present in the type table)
- type_2_id (present in the type table)
- egg_group_id (present in the egg_group table)
- egg_group_2_id (present in the egg_group_table)
- level (between 1 and 100)

Response
- 201: profile:
  - user_id
  - gender
  - search_male
  - search_female
  - search_none
  - short_bio
  - public_popularity
  - type_id
  - type_2_id
  - egg_group_id
  - egg_group_2_id
  - level
- 400: Validation Error with details
- 500: Internal Server Error

### / - DELETE
Delete the current user's profile
Response
- 200: "Profile successfully deleted"
- 500: Internal Server Error

### /<user_id> - GET
Get another user profile

Response
- 200: profile:
  - user_id
  - gender
  - search_male
  - search_female
  - search_none
  - short_bio
  - public_popularity
  - type_id
  - type_2_id
  - egg_group_id
  - egg_group_2_id
  - level
- 404: "Resource not found"
- 500: Internal Server Error
