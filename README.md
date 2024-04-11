## Project Stracture

```
|--- jesse_trading
    |--- jesse_bot: This is where the strategies are developed and running (based on the template provided by Jesse -  `https://github.com/jesse-ai/project-template.git`)
|--- jesse: the backtesting framework - can be a pip package but I need to change some code so I imported it here
```


## Setup

- Clone jesse into the project (for local development):
```sh
git clone https://github.com/jesse-ai/jesse.git
```

- Set python interpreter to the correct version required (prob 3.9)
```sh 
poetry env use <path_to_python_binary>
```

- Add Jesse as editable module 
```sh
poetry add -e ./jesse
```
** This step is crucial to do as `poetry add` and NOT as `poetry install`. if you added it using `poetry install` it messed up the virutal env and may cauase weird import errors. if you mistekenly did `poetry install` you'll have to flush the virtual env and re-install the dependencies.

- Install dependencies
```sh
poetry install
```
- Set the .env file (see comments in .env.example)
```sh
cd jesse_trading/jesse_bot
# to create a .env file of yours
cp .env.example .env
```


## Getting started

- Start PostgreSQL server
```sh
pg_ctl start ...
```
- Start redit db
```sh
redis-server
```
- Start Jesse (while virtual env is activated)
```sh
jesse run
```
- Open [localhost:9000](http://localhost:9000) to see the dashboard.

** This related for local run - for debugging. To run in docker see jesse instructions

`https://github.com/jesse-ai/jesse` and `https://github.com/jesse-ai/project-template.git`
