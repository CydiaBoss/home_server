# Home Server

The backend for my home server.

## Installation

Latest Versions Tested:
Python - 3.11.9
Apache - 24v
PostgreSQL - 17.2

For PyPi modules, see ./requirements.txt

### Apache

Download version 24 or try the latest version of Apache from ApacheLounge.
Unzip the binaries to the desired location and create an environmental variable called `MOD_WSGI_APACHE_ROOTDIR`

### PyPi

Clone this repo and create a virtual environment.
Run `pip install -r requirements` to install all the dependencies.

### PostgreSQL

Install 17.2 of PostgreSQL or attempt the latest version from the official site.
Create a database called `home_db` and a user called `home_django` with a long password.
Write the password down in a `.env` file under the field `DBPASS`.
Grant all privileges and public schema rights to the new user with the new database.