#!/usr/bin/env python

from diarybot.utils.docprompt import docprompt
from diarybot.config import config, config_filename
from diarybot.utils.logger import logger
from diarybot.utils.dbbasic import create_database

import urllib
import requests
import webbrowser

module_name = 'moves'

screen_introduction = """
Introduction
============

There are different ways to access your Moves data. All include that you need
to trust a so-called "Moves app" (not to be confused with "the" Moves App). No
matter which app you trust - this app will be able to access your Moves data
(locations and activities). However, you can revoke the access at any time.

The philosophy of Diary Bot is that you will never have to "trust" a third
party or that you transmit your data to anyone. To this end, you will need to
create a Moves app yourself. Diary Bot will then use this app to download your
data from Moves. As Diary Bot runs locally on your computer, none of your data
will be shared with any third party.

You can find more information on the authentification process at 
https://dev.moves-app.com/docs/authentication and 
https://dev.moves-app.com/docs/faq

    :prompt: Do you understand (y/n)?
    :name: tmp0
    :choices: ['y']
"""

screen_createapp = """
Task 1: Create a Moves App
==========================

A browser window just opened with the site https://dev.moves-app.com/apps. You
need to sign in with a Google account. Next, please click "Create a New App".

You need to enter an "Application name" and a "Developer". Values for both
fields are required, but the content does not matter. Press "Create".

    :prompt: Did you create your Moves App (y/n)?
    :name: tmp1
    :choices: ['y']

Task 2: Set the Redirect URL
============================

Next, you need to enter

    http://httpbin.org/get

as "Redirect URI". You definitely need to click "Save Changes" before you
proceed. The URL will be used in the second step to retrieve an access token.
Note that httpbin.org will neither receive your Google Account or your Moves
data. It will only be used during the authentication process. No information
will be stored.

    :prompt: Did you set the Redirect URL (y/n)?
    :name: tmp2
    :choices: ['y']

Task 3: Tell us your Client ID and Client Secret
================================================

After saving, you will be presented with a dialog showing you a "Client ID" and
a "Client secret". Please enter these keys here.

    :prompt: Client ID:
    :name: client_id

    :prompt: Client secret:
    :name: client_secret
"""

screen2 = """
Task 4: Authorize your App
==========================

In the next step, you need to get an access token. Pleae follow the
instructions on the website that just opened:

1. Open Moves on your phone
2. Choose main menu (icon bottom right) > Connected Apps > Enter PIN
3. Enter the displayed code (the space does not matter)

You will then be presented with a confirmation dialoge. Click "Allow".

    :prompt: Did you open the Moves app, enter the code on the Website and press "Allow" (y/n)?
    :name: tmp
    :choices: ['y']

Task 5: Get an Access Token
===========================

Next, your Web browser (where you entered the last URL) displays a Website at
http://httpbin.org. On this site, you see a line at the top that begins with
"code". This site appears a bit cryptic, but we chose this way to provide a
transparent process for you.

Please copy the string after "code" (without quotes) below:

    :prompt: code:
    :name: code
"""

if __name__ == '__main__':
    # show introduction
    data = docprompt(source=screen_introduction)
    data.prompt()

    # open Moves Developer Center
    webbrowser.open_new("https://dev.moves-app.com/apps")

    # show first dialoge and retrieve client id and client secret
    data = docprompt(source=screen_createapp)
    data.prompt()
    client_id = data.client_id
    client_secret = data.client_secret

    # open authorization website
    url = "https://api.moves-app.com/oauth/v1/authorize" 
    data = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "activity location",
        "redirect_uri": "http://httpbin.org/get"
    }
    code_url = url + '?' + urllib.urlencode(data)
    webbrowser.open(code_url)

    # show second dialoge and retrieve authorization code
    data = docprompt(source=screen2.format(URL=code_url))
    data.prompt()
    code = data.code

    # get access token
    url = "https://api.moves-app.com/oauth/v1/access_token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://httpbin.org/get"
    }
    r = requests.post(url + '?' + urllib.urlencode(data))
    access_token = r.json()['access_token']

    # save stuff to config
    if not config.has_section(module_name):
        config.add_section(module_name)
    config.set(module_name, 'enable', 'true')
    config.set(module_name, 'access_token', access_token)

    config.write(open(config_filename, "w"))

    logger.debug("wrote access token to configuration file '%s'" % config_filename)

    # create database if required
    logger.debug("creating database for module %s" % module_name)

    design_document = r'''
    {
       "_id": "_design/diarybot",
       "language": "javascript",
       "views": {
           "bydate": {
               "map": "function(doc) {\n  var parts = doc._id.split('-');\n  var d = new Date(parts[0], parts[1]-1, parts[2]);\n\n  emit(d.getTime() / 1000, doc);\n}"
           },
           "lastid": {
               "map": "function(doc) {\n  var parts = doc._id.split('-');\n  var d = new Date(parts[0], parts[1]-1, parts[2]);\n\n  emit(null, d.getTime() / 1000);\n}",
               "reduce": "function (key, values, rereduce) {\n    var max = -Infinity;\n    for(var i = 0; i < values.length; i++)\n    {\n        if(typeof values[i] == 'number')\n        {\n            max = Math.max(values[i], max);\n        }\n    }\n    return max;\n}"
           }
       }
    }
    '''

    create_database(module_name, design_document)
    logger.debug("wizard for module %s done" % module_name)
