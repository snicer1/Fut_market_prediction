import os

default_value = ''

username = os.getenv('DB_USERNAME', default_value)
password = os.getenv('DB_PASSWORD', default_value)
host = os.getenv('DB_HOST', default_value)
port = os.getenv('DB_PORT', default_value)
db_name = os.getenv('DB_DB_NAME', default_value)