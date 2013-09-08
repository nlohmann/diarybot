# Diary Bot

## Skype Module

![Skype](http://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Skype_logo.svg/200px-Skype_logo.svg.png "Skype")

Copies all your Skype chats into the database.

### Configuration

Copy file `config.json.template` to `config.json` and set `skype_username` to your Skype user name, for instance

    {
        "skype_username": "foo"
    }

if your Skyype user name is "foo".

The data is read locally from the Sqlite database `~/Library/Application Support/Skype/foo/main.db`, so don't be surprised or worried if no password or Internet connection is required. We currently only tried OS X as operating system and would be happy to hear about other experiences.

### Usage

Before the initial pull, execute `reset_db.py` to create the CouchDB data base `diarybot-skype` and to set up required design documents. You can execute this script any time you want to start over. Your original Skype database will never be touched by this.

Execute `update_db.py` to pull the data from your Skype data base to the CouchDB data base `diarybot-skype`. Note that an initial update may take some time. After that, only delta updates will be made which usually take less than a second.

### Example output

	$ ./reset_db.py 
	DONE: Created database 'diarybot-skype'.
	DONE: Adding design documents from 'design_document.json'.

	$ ./update_db.py 
	STATUS: Reading new entries from Skype's local database...
	DONE: Read 228753 new entries from Skype's local database.
	STATUS: Added 10000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 20000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 30000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 40000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 50000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 60000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 70000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 80000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 90000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 100000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 110000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 120000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 130000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 140000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 150000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 160000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 170000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 180000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 190000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 200000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 210000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 220000 of 228753 entries to the database 'diarybot-skype'.
	STATUS: Added 228753 of 228753 entries to the database 'diarybot-skype'.
	DONE: Added 228753 entries to the database 'diarybot-skype'.
	STATUS: Triggering re-indexing of table 'diarybot-skype'...
	DONE: Re-indexing of table 'diarybot-skype'.
