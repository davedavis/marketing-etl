import sys

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class CampaignReportRecord(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'CampaignsReport'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    platform = Column(Integer, ForeignKey('Platform.id'))
    status = Column(String(length=16))
    date = Column(Date)
    week = Column(Integer)
    campaign_name = Column(String(length=512))
    campaign_id = Column(String(length=32))
    network = Column(String(length=32), default="Unknown")
    impressions = Column(Float, default=0)
    clicks = Column(Float, default=0)
    spend = Column(Float, default=0)
    conversions = Column(Float, default=0)
    cost_per_conversion = Column(Float, default=0)
    value_per_conversion = Column(Float, default=0)
    conversion_value = Column(Float, default=0)
    conversion_rate = Column(Float, default=0)
    conversion_value_per_cost = Column(Float, default=0)
    impression_share = Column(Float, default=0)
    budget_lost_is = Column(Float, default=0)
    rank_lost_is = Column(Float, default=0)


    def __repr__(self):
        return f'Campaign Report Item: {self.platform} {self.campaign_name} Week: {self.week} - Spend: {self.spend}'
