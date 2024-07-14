# BoobJuice WebApp

## Setup
### Database

1. Using MariaDB and your admin tool of choice, create a database or pick one that already exists.
	- **If you're using Adminer, click the `Create database` link on the `Select database` screen.**
2. Within that database, create a user with the following privileges.
	- **In Adminer, select the database and click `Privileges` and in the field at the top of the checkbox column enter `YOUR_DATABASE_NAME.*`**
	- Table > Alter, Create, Delete, Drop, Index, Insert, Select, Update,
	- Column > Select, Insert, Update

### BoobJuice

1. Copy the database name into a container variable called `MARIA_DATABASE`
2. Copy the username and password into container variables called `MARIA_USERNAME` and `MARIA_PASSWORD`
3. Copy the IP and port of your database container into container variables called `MARIA_HOST` and `MARIA_PORT`
