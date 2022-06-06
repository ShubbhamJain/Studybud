# Studybud

### Table of contents
* [Intoduction](#introduction)
* [Features](#features)
* [Application Demo](#application-demo)
* [Technologies](#technologies)
* [Setup](#setup)

### Introduction

Project uses Django to build a discord like application. The application creates different rooms around a topic for users to connect with one another and share there ideas. The users can get a list of topics and see the recent activities happening on the site. Plus much more.

### Features

1. Login/SignUp
2. Room Creation
3. Recent topics
4. Recent activites
5. Search for rooms and topics
6. User profile/ User Feed
7. Profile editing
8. Room editing/Deletion
9. Message Editing/Deletion
10. Mobile view

### Application Demo

The app is deployed on heroku. The link to the site is-
Studybud ()

### Technologies

Project is created with:
* Django
* Python
* Sqlite
* Html
* CSS

### Setup

To run the project, follow the steps-

* Clone the Repo-
```
$ git clone [repo Url]
```

* Create a virtual environment and install dependencies-
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

* Once done, run the app-
```
$ python manage.py runserver
```