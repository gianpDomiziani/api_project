import os

def get_api_url():

    host = os.environ.get('API_HOST', 'localhost')
    port = 8080 if host == 'localhost' else 1234
    return f"http://{host}:{port}"

def get_postgres_uri():

    host = os.environ.get('DB_HOST', 'localhost')
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PSW', 'abc123')
    user, db_name = 'pages', 'pages'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
