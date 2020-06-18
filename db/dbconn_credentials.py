import os

username = os.getenv('DB_USERNAME', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres1')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_DB_NAME', 'fut_market_prediction')