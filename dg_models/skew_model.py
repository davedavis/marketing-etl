import sys

from sqlalchemy import Column, Integer, Float, ForeignKey

from dg_config import settingsfile
from dg_models.base_model import Base
from dg_models.account_model import Account

settings = settingsfile.get_settings()


class Skew(Base):
    __tablename__ = 'Skew'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    quarter = Column(Integer)
    week = Column(Integer)
    spend_target = Column(Float)
    revenue_target = Column(Float)
    er_target = Column(Float)


    def __repr__(self):
        return f'SKEW: {self.id}'
