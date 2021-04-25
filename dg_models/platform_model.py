import sys

from sqlalchemy import Column, Integer, ForeignKey, String

from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class Platform(Base):
    __tablename__ = 'Platform'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    platform = Column(String(length=64))
    account_number = Column(String(length=64))
    new_account_number = Column(String(length=64))


    def __repr__(self):
        return f'Platform: {self.platform}, Account Number: {self.account_number},'
