# Diary Bot

## About

Diary Bot is a robot that automatically writes a very detailed diary for you. It pulls data from all kind of sources such as social media providers, communities, or local storages and processes them into a daily overview of your activities.

## Privacy statement

Diary Bot stores all your data **locally**. It never uploads any information (passwords, keys) anywhere. As a side effect, it maintains a local archive of your data, so you can always access your data locally.

## Status

As of now, the code for the first data sources is published. Other sources are already implemented, but the source code needs to be "cleaned up" before releasing. Also an early-beta frontend of the diary exists, which hopefully be released soon. Stay tuned!

## Modules

| Module        | Category      | Description |
| ------------- |---------------| ------|
| ![iMessages](http://upload.wikimedia.org/wikipedia/commons/2/23/Messages_%28application%29_logo.png) | Chat | [iMessages](http://www.apple.com/de/ios/messages/) together with their attachments (from local database) |
| ![Moves](https://www.moves-app.com/assets/moves-logo-206x206.png) | Location | [Moves](https://www.moves-app.com) daily storylines with places, routes, and activities. |
| ![Skype](http://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Skype_logo.svg/200px-Skype_logo.svg.png) | Chat | [Skype](http://www.skype.com) messages (from local database) |
| ![Twitter](http://upload.wikimedia.org/wikipedia/de/thumb/9/9f/Twitter_bird_logo_2012.svg/200px-Twitter_bird_logo_2012.svg.png) | Social | [Twitter](http://twitter.com) tweets. |
| ![Xbox](http://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Xbox.svg/200px-Xbox.svg.png) | Life | [Xbox](http://www.xbox.com) live achievements. Data provided by [XboxAPI](https://xboxapi.com). |

## Prerequisites

- [CouchDB](http://couchdb.apache.org) is used as main data store. It should work with version 1.3.1 or later.
- [Python](http://www.python.org) is used as main scripting language. Version 2.7.5 or later should be OK.

## Installation

- Install [CouchDB](http://couchdb.apache.org).
- Install [Python](http://www.python.org).
- Install a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/), select it and install the required modules with `pip install -r requirements.txt`.

### Installation example for OS X using Homebrew

```
git clone https://github.com/nlohmann/diarybot
cd diarybot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

For all subsequent calls, we expect the virtual environment to be set up and activated.

## Setup

### CouchDB

All databases will be prefixed with `diarybot-` which makes it easier for you to clean up if you don't like Diary Bot any more. Please rename `diarybot/dbconfig.py.template` to `diarybot/dbconfig.py`. You may edit that file to adjust the URL to your CouchDB installation (defaults to `http://localhost:5984/`) and a database username and password to be able to access databases.

Diary Bot comes with several modules, one for each data source. In principle, a module will only be called, if the respective database has been created. As there are initially no Diary Bot databases, all modules will be skipped. To create a modules database, please execute the respective database setup scripts, for instance

```
python -m diarybot.sources.chat.imessage.setup
``` 

for the iMessage module.

### Modules

The source for Diary Bot are implemented as modules. Each module pulls data from a data source and stores it in a dedicated data source.

#### iMessage

To enable the iMessage module, please execute:

```
python -m diarybot.sources.chat.imessage.setup
```

The module requires no further configuration.

#### Moves

To enable the Moves module, please execute:

```
python -m diarybot.sources.location.moves.setup
```

To set up the module, please rename the file `diarybot/location/moves/config.py.template` to `diarybot/location/moves/config.py` and add the information from your Moves app.

#### Skype

To enable the Skype module, please execute:

```
python -m diarybot.sources.chat.skype.setup
```

To set up the module, please rename the file `diarybot/chat/skype/config.py.template` to `diarybot/chat/skype/config.py` and add your Skype user name.

#### Twitter

To enable the Moves module, please execute:

```
python -m diarybot.sources.social.twitter.setup
```

To set up the module, please rename the file `diarybot/social/twitter/config.py.template` to `diarybot/social/twitter/config.py` and add the information from your Twitter app.

#### Xbox Achievements

To enable the Xbox module, please execute:

```
python -m diarybot.sources.life.xbox.setup
```

To set up the module, please rename the file `diarybot/life/xbox/config.py.template` to `diarybot/life/xbox/config.py` and add your API key from https://xboxapi.com.

## Run Diary Bot

Run Diary Bot with all enabled modules with

```
python -m main
```
