import sys

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from dg_config import settingsfile
from dg_models.base_model import Base
import argparse

settings = settingsfile.get_settings()


class Account(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'Account'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account_name = Column(String(length=16))
    account_country_code = Column(String(length=8))
    account_region = Column(String(length=16))
    account_subregion = Column(String(length=8))

    def __repr__(self):
        return f'Account: {self.account_name} Region: {self.account_region}'
