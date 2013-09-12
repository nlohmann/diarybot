# Diary Bot

## Jawbone Up Module

![Jawbone Up](http://a4.mzstatic.com/us/r30/Purple/v4/7c/e3/cf/7ce3cff0-3831-9c52-d032-fa24727506fa/mzl.zlmigmfa.175x175-75.jpg)

Copies all your activity from your Jawbone Up into the database.

### Configuration

Copy file `config.json.template` to `config.json` and set `username` and `password` to your Jawbone credentials, for instance

    {
        "username": "john.doe@gmail.com",
		"password": "this_is_a_secret"
    }

The data is then loaded from Jawbone and pushed into the database. Note that we do not use your password for any other purpose. It is transmitted once via a POST call to https://jawbone.com/user/signin/login.

### Usage

Before the initial pull, execute `reset_db.py` to create the CouchDB data base `diarybot-up` and to set up required design documents. You can execute this script any time you want to start over. Your data at Jawbone will never be touched by this: the access to the data is read-only.

Execute `update_db.py` to download your activity from Jawbone to the CouchDB data base `diarybot-up`. We currently download all activities from Jawbone, so an update is rather slow.

### Example output

	$ ./reset_db.py 
	DONE: Created database 'diarybot-up'.
	DONE: Adding design documents from 'design_document.json'.

	$ ./update_db.py 
    STATUS: Reading entries from Jawbone's API...
    STATUS: Fetching further information...
    DONE: Read 374 entries from Jawbone's API.
    DONE: Added 374 entries to the database 'diarybot-up'.

### Credits

We use the inofficial [Jawbone UP API](http://eric-blue.com/projects/up-api/), reverse-enginieered by [Eric Blue](http://twitter.com/ericblue). The [Updates](https://niklaslindblad.se/2013/07/jawbone-up-api-updates/) by [Niklas Lindblad](https://twitter.com/nlindblad) were also very helpful.
