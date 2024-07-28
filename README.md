## Project Stracture

```
|--- jesse_trading
    |--- jesse_bot: This is where the strategies are developed and running (based on the template provided by Jesse -  `https://github.com/jesse-ai/project-template.git`)
|--- jesse: the backtesting framework - can be a pip package but I need to change some code so I imported it here
```


## Setup

- Clone jesse into the project (for local development):
```sh
git clone https://github.com/Tzion/jesse.git
```

- Set python interpreter to the correct version required (prob 3.9)
```sh 
poetry env use <path_to_python_binary>
```

- Activate the virtual env:
``` sh
source .venv/bin/activate
```

- Add jesse as editable module 
```sh
poetry add -editable ./jesse
```
** This step is crucial to do as `poetry add` and NOT as `poetry install`. if you added it using `poetry install` it messed up the virutal env and may cauase weird import errors. if you mistekenly did `poetry install` you'll have to flush the virtual env and re-install the dependencies.
* Do not run `potery install` at any time - it ruin the environment - `jesse run` does not work after that.

- If `poetry install` will be needed at some point, a workaround to the bug could be `poetry add -e git+https://github.com/Tzion/jesse.git` - but then the package will be installed in the venv directory.

- Set the .env file (see comments in .env.example)
```sh
cd jesse_trading/jesse_bot
# to create a .env file of yours
cp .env.example .env
```
- Set postgres database
``` sh
cd jesse-trading/jesse_trading
initdb -D db_postgres/
# Create database with privilege user (as define in .env file)
pg_ctl -D db_postgres start
createdb jesse_db
psql jesse_db
CREATE USER jesse_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE jesse_db TO jesse_user;
pg_ctl -D db_postgres stop
```


## Getting started

- Start PostgreSQL server
```sh
pg_ctl -D jesse_trading/db_postgres/ start
```
- Start redit db
```sh
redis-server
```
- Start Jesse (while virtual env is activated and inside jesse_bot directory)
```sh
jesse run
```
- Open [localhost:9000](http://localhost:9000) to see the dashboard.

** This related for local run - for debugging. To run in docker see jesse instructions

`https://github.com/jesse-ai/jesse` and `https://github.com/jesse-ai/project-template.git`
