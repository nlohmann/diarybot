# Diary Bot

## iMessage Module

Copies all your iMessage chats with their attachments into the database.

### Configuration

No configuration is needed. If you run a late OS X with enabled iMessage, then the data is read locally from the Sqlite database `~//Library/Messages/chat.db`, so don't be surprised or worried if no password or Internet connection is required.

### Usage

Before the initial pull, execute `reset_db.py` to create the CouchDB data base `diarybot-skype` and to set up required design documents. You can execute this script any time you want to start over. Your original iMessage database will never be touched by this.

Execute `update_db.py` to pull the data from your iMessage data base to the CouchDB data base `diarybot-skype`. Note that an initial update may take some time, especially since attachments are also put into the database. After that, only delta updates will be made which usually take less than a second.

### Example output

	$ ./reset_db.py 
	DONE: Created database 'diarybot-imessage'.
	DONE: Adding design documents from 'design_document.json'.

	$ ./update_db.py 
	STATUS: Reading new entries from iMessage's local database...
	DONE: Read 1174 new entries from iMessage's local database.
	NOTE: Adding entries can be slow, because 33 attachments (52 MB) are added.
	STATUS: Added 100 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 200 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 300 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 400 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 500 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 600 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 700 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 800 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 900 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 1000 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 1100 of 1174 entries to the database 'diarybot-imessage'.
	STATUS: Added 1174 of 1174 entries to the database 'diarybot-imessage'.
	DONE: Added 1174 entries to the database 'diarybot-imessage'.
	STATUS: Triggering re-indexing of table 'diarybot-imessage'...
	DONE: Re-indexing of table 'diarybot-imessage'.
