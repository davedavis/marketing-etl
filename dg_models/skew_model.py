import sys

from sqlalchemy import Column, Integer, String, Date, Float, Numeric
from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class SkewRecord(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'Q'+sys.argv[2]+'_skews'
    __tableargs__ = {'schema': settings['db_database']}

    skew_id = Column(Integer, primary_key=True)
    account_name = Column(String(length=64))
    spend_target = Column(Float)
    revenue_target = Column(Float)
    er_target = Column(Float)
    w1_skew = Column(Float)
    w2_skew = Column(Float)
    w3_skew = Column(Float)
    w4_skew = Column(Float)
    w5_skew = Column(Float)
    w6_skew = Column(Float)
    w7_skew = Column(Float)
    w8_skew = Column(Float)
    w9_skew = Column(Float)
    w10_skew = Column(Float)
    w11_skew = Column(Float)
    w12_skew = Column(Float)
    w13_skew = Column(Float)
    w14_skew = Column(Float)

    def __repr__(self):
        return f'SKEWS: {self.account_name}'
