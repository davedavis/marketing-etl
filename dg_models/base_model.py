from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dg_config import settingsfile
settings = settingsfile.get_settings()


# Init the global base
Base = declarative_base()
engine = create_engine(settings['db_connection_string'], echo=True)
Base.metadata.bind = engine

# Init the global session.
Session = sessionmaker()
Session.configure(bind=engine)



