import sys

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class AccountReportRecord(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'AccountsReport'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    platform = Column(Integer, ForeignKey('Platform.id'))
    date = Column(Date)
    week = Column(Integer)
    impressions = Column(Float)
    clicks = Column(Float)
    spend = Column(Float)

    def __repr__(self):
        return f'Account Report: {self.account} Week: {self.week} - Spend: {self.spend}'
