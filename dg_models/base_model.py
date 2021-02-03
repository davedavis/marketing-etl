from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dg_config import settingsfile
settings = settingsfile.get_settings()


# Init the global base
Base = declarative_base()
# engine = create_engine(settings['db_connection_string'], echo=True)

# ssl_args is needed when connecting to SSL on DO or other provider.
# ToDo: Create conditional here to switch between local and remote (no ssl args)

if settings['database_provider'] == "digitalocean":
    ssl_args = {'ssl_ca': settings['db_connection_cert']}
    engine = create_engine(settings['db_connection_string'], connect_args=ssl_args)
else:
    engine = create_engine(settings['db_connection_string'])

Base.metadata.bind = engine

# Init the global session.
Session = sessionmaker()
Session.configure(bind=engine)



