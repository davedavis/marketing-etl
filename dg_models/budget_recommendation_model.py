import sys

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from dg_config import settingsfile
from dg_models.base_model import Base

settings = settingsfile.get_settings()


class BudgetRecommendation(Base):
    __tablename__ = 'BudgetRecommendationsReport'
    __tableargs__ = {'schema': settings['db_database']}

    id = Column(Integer, primary_key=True)
    account = Column(Integer, ForeignKey('Account.id'))
    platform = Column(Integer, ForeignKey('Platform.id'))
    campaign_id = Column(String(length=32))
    campaign_name = Column(String(length=512))
    current_budget = Column(Float, default=0)
    recommended_budget = Column(Float, default=0)

    def __repr__(self):
        return f'Budget Recommendation Report: {self.account} Campaign: {self.campaign_name} - Recommendation: {self.recommended_budget} '
