from sqlalchemy import Column, Integer, String, Date, Float
from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class CampaignReportRecord(Base):
    __tablename__ = 'campaignsReport'
    __tableargs__ = {'schema': settings['db_database']}

    report_id = Column(Integer, primary_key=True)
    platform = Column(String(length=64))
    account_name = Column(String(length=64))
    account_number = Column(String(length=64))
    time_period = Column(Date)
    week = Column(Integer)
    campaign = Column(String(length=512))
    campaign_id = Column(Integer)
    network = Column(String(length=64))
    impressions = Column(Float)
    clicks = Column(Float)
    spend = Column(Float)

    def __repr__(self):
        return f'Account Report: {self.platform} {self.account_name} Week: {self.week} - Spend: {self.spend}'
