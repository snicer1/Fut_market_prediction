import pg8000
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db import dbconn_credentials

engine = create_engine(f'postgresql+pg8000://{dbconn_credentials.username}:{dbconn_credentials.password}@{dbconn_credentials.host}'
                       f':{dbconn_credentials.port}/{dbconn_credentials.db_name}')

def create_db_session(engine = engine):
    session = sessionmaker(bind=engine)
    s = session()
    return s
