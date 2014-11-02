#!/usr/bin/env python

import diarybot

diarybot.modules.chat.skype.Skype()
diarybot.modules.chat.imessage.Imessage()

diarybot.modules.location.moves.Moves()
diarybot.modules.location.foursquare.dataimport.FoursquareDataImport()

diarybot.modules.social.twitter.Twitter()
diarybot.modules.social.instagram.InstagramDataImport()

diarybot.modules.media.lastfm.LastfmDataImport()

diarybot.modules.life.xbox.Xbox()
