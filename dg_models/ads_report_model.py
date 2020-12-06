from sqlalchemy import Column, Integer, String, Date, Float
from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class AdReportRecord(Base):
    __tablename__ = 'adsReport'
    __tableargs__ = {'schema': settings['db_database']}

    report_id = Column(Integer, primary_key=True)
    platform = Column(String(length=64))
    account_name = Column(String(length=64))
    account_number = Column(String(length=64))
    time_period = Column(Date)
    week = Column(Integer)
    campaign = Column(String(length=512))
    currency = Column(String(length=16))
    impressions = Column(Float)
    clicks = Column(Float)
    spend = Column(Float)
    ctr = Column(Float)
    average_cpc = Column(Float)
    ad_type = Column(String(length=512))
    shopping_title = Column(String(length=512))
    headline_1 = Column(String(length=512))
    headline_2 = Column(String(length=512))
    headline_3 = Column(String(length=512))
    description_1 = Column(String(length=512))
    description_2 = Column(String(length=512))
    path_1 = Column(String(length=64))
    path_2 = Column(String(length=64))
    dsa_Description_1 = Column(String(length=512))
    dsa_Description_2 = Column(String(length=512))
    rsa_headline_1 = Column(String(length=128))
    rsa_headline_2 = Column(String(length=128))
    rsa_headline_3 = Column(String(length=128))
    rsa_headline_4 = Column(String(length=128))
    rsa_headline_5 = Column(String(length=128))
    rsa_headline_6 = Column(String(length=128))
    rsa_headline_7 = Column(String(length=128))
    rsa_headline_8 = Column(String(length=128))
    rsa_headline_9 = Column(String(length=128))
    rsa_headline_10 = Column(String(length=128))
    rsa_headline_11 = Column(String(length=128))
    rsa_headline_12 = Column(String(length=128))
    rsa_headline_13 = Column(String(length=128))
    rsa_headline_14 = Column(String(length=128))
    rsa_headline_15 = Column(String(length=128))
    rsa_description_1 = Column(String(length=512))
    rsa_description_2 = Column(String(length=512))
    rsa_description_3 = Column(String(length=512))
    rsa_description_4 = Column(String(length=512))

    def __repr__(self):
        return f'Ads Report: {self.platform} {self.account_name} Week: {self.week} - Spend: {self.spend}'
