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
    country = Column(String(length=64))
    net_media_spend = Column(Float)
    alliance_media_spend = Column(Float)
    er_target = Column(Float)
    w1_skew = Column(Numeric)
    w2_skew = Column(Numeric)
    w3_skew = Column(Numeric)
    w4_skew = Column(Numeric)
    w5_skew = Column(Numeric)
    w6_skew = Column(Numeric)
    w7_skew = Column(Numeric)
    w8_skew = Column(Numeric)
    w9_skew = Column(Numeric)
    w10_skew = Column(Numeric)
    w11_skew = Column(Numeric)
    w12_skew = Column(Numeric)
    w13_skew = Column(Numeric)
    w14_skew = Column(Numeric)

    def __repr__(self):
        return f'SKEWS: {self.platcuntry}'
