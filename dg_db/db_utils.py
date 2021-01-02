import contextlib
from dg_models.base_model import Base, Session, engine

# Models need to remain here, even though they're not being used in order for SQLAlchemy to import them when
# doing the DB init using metadata. Otherwise, tables won't be created if they don't exist.
from dg_models.accounts_report_model import AccountReportRecord
from dg_models.campaigns_report_model import CampaignReportRecord
from dg_models.ads_report_model import AdReportRecord

from dg_config import settingsfile

settings = settingsfile.get_settings()


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all()


def get_session():
    new_session = Session()
    return new_session

