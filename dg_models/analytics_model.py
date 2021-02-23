import sys

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from dg_config import settingsfile
from dg_models.base_model import Base
import argparse

settings = settingsfile.get_settings()


class MetricsReportRecord(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'AnalyticsReport'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    date = Column(Date)
    week = Column(Integer)
    revenue = Column(Float)
    conversion_rate = Column(Float)
    visits = Column(Float)
    orders = Column(Float)
    aov = Column(Float)
    units = Column(Float)
    aur = Column(Float)

    def __repr__(self):
        return f'Analytics Report: {self.account} Week: {self.week} - Revenue: {self.revenue}'
