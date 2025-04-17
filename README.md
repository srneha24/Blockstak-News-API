# BLOCKSTAK NEWS API

## Project description

## Setup instructions

### FastAPI Setup

1. Create a virtual environment using the following command

    **MacOS / Linux**

    ```bash
    python3 -m venv env
    ```

    **Windows**

    ```powershell
    python -m venv env
    ```

2. Activate the virtual environment using the following command

    **MacOS / Linux**

    ```bash
    source env/bin/activate
    ```

    **Windows**

    ```powershell
    env/Scripts/activate
    ```

3. Install all the required packages using the following command

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file on the project root, then copy the contents from the `.env.example` file and paste them to this file. Fill the variables with the values for your system.

### Database Setup

1. Create a Postgres database on `psql` using the following command

    ```sql
    CREATE DATABASE news_api_db;
    ```

2. On the project root, run the following command to create the database tables and apply the migrations

    ```bash
    aerich upgrade
    ```

## How to run the server

**Development**

To run the server in development mode, run the following command

```bash
fastapi dev main.py
```

**Production**

To run the server in production mode, run the following command

```bash
fastapi run --host 0.0.0.0 main.py
```

## How to run tests

## How to use Docker

## How to generate access tokens and use secured endpoints

## API usage examples and descriptions for all 5 endpoints above