import contextlib
from datetime import datetime

from dg_models.base_model import Base, Session, engine

# Models need to remain here, even though they're not being used in order for SQLAlchemy to import them when
# doing the DB init using metadata. Otherwise, tables won't be created if they don't exist.
from dg_models.accounts_report_model import AccountReportRecord
from dg_models.campaigns_report_model import CampaignReportRecord
from dg_models.ads_report_model import AdReportRecord
from dg_models.analytics_model import MetricsReportRecord

from dg_config import settingsfile
from dg_utils.quarter_utils import get_quarter_from_date, get_start_of_quarter

settings = settingsfile.get_settings()


def get_session():
    new_session = Session()
    return new_session


def delete_current_q_records():
    sess = get_session()
    too_new = get_start_of_quarter(datetime.now())
    sess.query(AccountReportRecord).filter(AccountReportRecord.date >= too_new).delete(synchronize_session=False)
    sess.query(CampaignReportRecord).filter(CampaignReportRecord.date >= too_new).delete(synchronize_session=False)
    sess.query(MetricsReportRecord).filter(MetricsReportRecord.date >= too_new).delete(synchronize_session=False)

    sess.commit()
    print("All records for this quarter have been dropped. Carry on.")


def init_db(quarter, year):
    print(f'Initializing database for {year} year')

    # If the report requested is for the current quarter, delete all the
    # records for this quarter so they can be refetched. We do this as platforms
    # update/adjust their metrics (particularly spend metrics) as fraudulent/invalid
    # clicks are refunded.
    if year == 'this' and quarter == get_quarter_from_date(datetime.now()):
        print("Report is for this year and this quarter. Dropping records. ")
        delete_current_q_records()

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all()
