#!/usr/bin/env python

import diarybot

diarybot.sources.chat.skype.Skype()
diarybot.sources.chat.imessage.Imessage()

diarybot.sources.location.moves.Moves()
diarybot.sources.location.foursquare.dataimport.FoursquareDataImport()

diarybot.sources.social.twitter.Twitter()

diarybot.sources.media.lastfm.LastfmDataImport()

diarybot.sources.life.xbox.Xbox()

diarybot.sources.social.instagram.InstagramDataImport()