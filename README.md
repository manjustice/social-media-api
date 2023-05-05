# Social media API

RESTful API for a social media platform. The API allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

## Installation

Python3 must be already installed

```shell

git clone https://github.com/manjustice/social-media-api.git
cd social_media_api
python -m venv venv
source venv/bin/activate (on Linux/maOS)
venv\Scripts\activate (on Windows)
pip install -r requirements.txt
copy .env.sample -> .env and populate with all required data
python manage.py migrate
python manage.py runserver
```

## Features

* JWT authenticated
* Admin panel - admin/
* Documentation is located at api/doc/swagger/
* User profile creation and updating with profile picture, bio, and other details
* User profile retrieval and searching for users by username or other criteria
* Follow/unfollow functionality with the ability to view lists of followed and following users
* Post creation with text content and optional media attachment
