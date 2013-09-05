# Diary Bot

## About

Diary Bot is a robot that automatically writes a very detailed diary for you. It pulls data from all kind of sources such as social media providers, communities, or local storages and processes them into a daily overview of your activities.

## Privacy statement

Diary Bot stores all your data **locally**. It never uploads any information (passwords, keys) anywhere. As a side effect, it maintains a local archive of your data, so you can always access your data locally.

## Status

As of now, the Skype chat database is used as first data source. Other sources are already implemented, but the source code needs to be "cleaned up" before releasing. Also an early-beta frontend of the diary exists, which hopefully be relesed soon. Stay tuned!

## Prerequesites

- [CouchDB](http://couchdb.apache.org) is used as main data store. It should work with version 1.3.1 or later. We assume that it runs at `http://127.0.0.1:5984` and we have permission to create databases. All databases will be prefixed with `diarybot-` which makes it easier for you to clean up if you don't like Diary Bot any more.
- [Python](http://www.python.org) is used as main scripting language. Version 2.7.5 or later shoud be OK.
- [couchdb Python package](https://pypi.python.org/pypi/CouchDB) is used to access CouchDB from Python. Version 0.9 works. From this package, please set up couchpy as CouchDB view server, see http://pythonhosted.org/CouchDB/views.html for a documentation.
- [iso6801 Python package](https://pypi.python.org/pypi/iso8601) is used to remain sane while joggling with dates. Version 0.1.4 please.

## Installation

- Install CouchDB.
- Install Python.
- Install the Python packages:
	- `sudo pip install couchdb`
	- `sudo pip install iso6801`
- Set up couchpy as CouchDB view server.
