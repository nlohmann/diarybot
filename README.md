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
| ![Foursquare](https://playfoursquare.s3.amazonaws.com/press/2014/foursquare-logomark.png) | Location | [Foursquare](https://www.foursquare.com) checkins of visited venues or events. |
| ![last.fm](http://cdn.last.fm/flatness/badges/lastfm_red.gif) | Media | [last.fm](https://www.lastfm.com) tracks your music you are listening to and suggest you new one. |


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

Diary Bot reads the file `diarybot.cfg` at startup. A template `diarybot_template.cfg` for this file is part of the distribution. You need to rename this file to `diarybot.cfg` before starting Diary Bot. The rest of this section explains which adjustments you need to make to `diarybot.cfg` to configure Diary Bot to your needs.


### CouchDB

All databases will be prefixed with `diarybot-` which makes it easier for you to clean up if you don't like Diary Bot any more. Please edit section `[couchdb]` in the configuration file `diarybot.cfg` to set the database URL, database username and password, and also the database prefix.

Diary Bot comes with several modules, one for each data source. In principle, a module will only be called, if the respective database has been created and the module has been enabled. The sections below explain you how to create the databases.


### Modules

The source for Diary Bot are implemented as modules. Each module pulls data from a data source and stores it in a dedicated data source.

#### iMessage

To create the iMessage database, please execute:

```
python -m diarybot.sources.chat.imessage.setup
```

To set up the module, please set `enable = true` in the `[imessage]` section of the configuration file `diarybot.cfg`.


#### Moves

To create the Moves database, please execute:

```
python -m diarybot.sources.location.moves.setup
```

To set up the module, please set `enable = true` in the `[moves]` section of the configuration file `diarybot.cfg` and set variable `access_token` to a valid access token of the Moves API.


#### Foursquare

To create the Foursquare database, please execute:

```
python -m diarybot.sources.location.foursquare.setup
```

To set up the module, please set `enable = true` in the `[foursquare]` section of the configuration file `diarybot.cfg` and set variable `access_token`, `client_id`, `client_secret` and `redirect_uri` to a valid values of the Foursquare API.


#### Skype

To create the Skype database, please execute:

```
python -m diarybot.sources.chat.skype.setup
```

To set up the module, please set `enable = true` in the `[skype]` section of the configuration file `diarybot.cfg` and set variable `skype_username` to your Skype user name.


#### Twitter

To create the Moves database, please execute:

```
python -m diarybot.sources.social.twitter.setup
```

To set up the module, please set `enable = true` in the `[twitter]` section of the configuration file `diarybot.cfg` and set variables `consumer_key`, `consumer_secret`, `access_token`, and `access_token_secret` to valid values for the Twitter API.
 

#### Xbox Achievements

To create the Xbox database, please execute:

```
python -m diarybot.sources.life.xbox.setup
```

To set up the module, please set `enable = true` in the `[xbox]` section of the configuration file `diarybot.cfg` and set variable `api_key` to your Xbox API key.

#### last.fm

To create the last.fm database, please execute:

```
python -m diarybot.sources.media.lastfm.setup
```

To set up the module, please set `enable = true` in the `[instagram]` section of the configuration file `diarybot.cfg` and set variable `access_token`, `client_id`, `client_secret` and `redirect_uri` to a valid values of the Foursquare API.


#### Instagram

To create the Instagram database, please execute:

```
python -m diarybot.sources.social.instagram.setup
```

To set up the module, please set `enable = true` in the `[instagram]` section of the configuration file `diarybot.cfg` and set variable `access_token`, `client_id`, `client_secret` and `redirect_uri` to a valid values of the Foursquare API.


## Run Diary Bot

Run Diary Bot with all enabled modules with

```
python -m main
```
