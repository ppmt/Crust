import os
basedir = os.path.abspath(os.path.dirname(__file__))

## For the forms
WTF_CSRF_ENABLED = True
SECRET_KEY = 'the secret is in the time!'

## For the Databases
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'crust.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



## What is below is not used yet. It was used in the flask tutorial
## on Miguel Grinberg's blog : http://blog.miguelgrinberg.com

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'your email'
MAIL_PASSWORD = 'your password'
# administrator list
ADMINS = ['your email']

# pagination
POSTS_PER_PAGE = 3

# Woosh is a search engine extension to Flask
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

#Openid.. use to login to the site when implemented.
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

