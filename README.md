# Tugas PWL 4

Nama : Raja Saputera
NIM : 120140228

## how to run

1. clone this repo

```bash
git clone
```

2. change directory to this repo

```bash
cd pwl4
```

3.  change development.ini url to your database url

```bash
sqlalchemy.url = mysql+pymysql://username:password@localhost:5432/dbname
```

4. install dependencies

```bash
 pip install -e .
```

5. migrate database

```bash
alembic -c development.ini upgrade head
```

6. load database

```bash
initialize_pwl_final_db development.ini
```

5. run

```bash
pserve development.ini --reload
```

6. run test

```bash
pytest
```

## api routes

| Route        | Method | Description        |
| ------------ | ------ | ------------------ |
| /login       | POST   | login              |
| /register    | POST   | register           |
| /movies      | GET    | get all movies     |
| /movies      | POST   | create movie       |
| /movies/{id} | GET    | get movie by id    |
| /movies/{id} | PUT    | update movie by id |
| /movies/{id} | DELETE | delete movie by id |
