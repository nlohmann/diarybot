# Diary Bot

## About

Diary Bot is a robot that automatically writes a very detailed diary for you. It pulls data from all kind of sources such as social media providers, communities, or local storages and processes them into a daily overview of your activities.

## Privacy statement

Diary Bot stores all your data **locally**. It never uploads any information (passwords, keys) anywhere. As a side effect, it maintains a local archive of your data, so you can always access your data locally.

## Status

As of now, the code for the first data sources is published. Other sources are already implemented, but the source code needs to be "cleaned up" before releasing. Also an early-beta frontend of the diary exists, which hopefully be relesed soon. Stay tuned!

## Modules

| Module        | Category      | Description |
| ------------- |---------------| ------|
| ![iMessages](http://upload.wikimedia.org/wikipedia/commons/2/23/Messages_%28application%29_logo.png) | Chat | [iMessages](http://www.apple.com/de/ios/messages/) together with their attachments (from local database) |
| ![Skype](http://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Skype_logo.svg/200px-Skype_logo.svg.png) | Chat | [Skype](http://www.skype.com) messages (from local database) |
| ![Nike+](http://upload.wikimedia.org/wikipedia/en/thumb/a/ac/Logo_of_Nike%2BiPod.svg/200px-Logo_of_Nike%2BiPod.svg.png) | Health | activities logged with the [Nike+ running app](http://nikeplus.nike.com/plus/products/gps_app/) (including GPS coordinates) |
| ![Jawbone Up](http://a4.mzstatic.com/us/r30/Purple/v4/7c/e3/cf/7ce3cff0-3831-9c52-d032-fa24727506fa/mzl.zlmigmfa.175x175-75.jpg) | Health | activities from the [Jawbone Up](https://jawbone.com/up) activity tracker |

## Prerequesites

- [CouchDB](http://couchdb.apache.org) is used as main data store. It should work with version 1.3.1 or later.
- [Python](http://www.python.org) is used as main scripting language. Version 2.7.5 or later shoud be OK.
- [PHP](http://php.net) is used for some other scripts. Any PHP version 5.x should work.
- [couchdb Python package](https://pypi.python.org/pypi/CouchDB) is used to access CouchDB from Python. Version 0.9 works.
- [iso6801 Python package](https://pypi.python.org/pypi/iso8601) is used to remain sane while joggling with dates. Version 0.1.4 please.

## Installation

- Install [CouchDB](http://couchdb.apache.org). We assume that it runs at `http://127.0.0.1:5984` and we have permission to create databases. All databases will be prefixed with `diarybot-` which makes it easier for you to clean up if you don't like Diary Bot any more.
- Install [Python](http://www.python.org).
- Install [PHP](http://php.net).
- Install the Python packages by executing:
	- `sudo pip install couchdb`
	- `sudo pip install iso6801`
- [Set up couchpy](http://pythonhosted.org/CouchDB/views.html) as CouchDB view server. The hardest part is usually finding your `local.ini` file. Using OS X, it is usally located in `~/Library/Application Support/CouchDB/etc/couchdb`. Please not that also the location of the `couchpy` executable may differ - it's `/usr/local/bin/couchpy` on my machine.
