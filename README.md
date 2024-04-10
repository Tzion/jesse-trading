## Project Stracture

```
|--- jesse_trading
    |--- jesse_bot: This is where the strategies are developed and running (based on the template provided by Jesse -  `https://github.com/jesse-ai/project-template.git`)
|--- jesse: the backtesting framework - can be a pip package but I need to change some code so I imported it here
```


## Setup

- Set the .env file (see .env.example)
```sh
# to create a .env file of yours
cp .env.example .env
```
- Start PostgreSQL server
```sh
pg_ctl start ...
```
- Start redit db
```sh
redis-server
```
- Start Jesse 
```sh
jesse run
```
- Open [localhost:9000](http://localhost:9000) to see the dashboard.

** This related for local run - for debugging. To run in docker see jesse instructions

`https://github.com/jesse-ai/jesse` and `https://github.com/jesse-ai/project-template.git`
