import contextlib
from datetime import datetime
from rich.console import Console
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
console = Console()

def get_session():
    new_session = Session()
    return new_session


def delete_current_q_records():
    sess = get_session()
    start_of_quarter = get_start_of_quarter(datetime.now())
    sess.query(AccountReportRecord).filter(AccountReportRecord.date >= start_of_quarter).delete(synchronize_session=False)
    sess.query(CampaignReportRecord).filter(CampaignReportRecord.date >= start_of_quarter).delete(synchronize_session=False)
    sess.query(MetricsReportRecord).filter(MetricsReportRecord.date >= start_of_quarter).delete(synchronize_session=False)

    sess.commit()
    console.print("All records for this quarter have been deleted. Carry on.", style="bold, green")


def init_db(quarter, year):
    console.print(f'Initializing database for {year} year')

    # If the report requested is for the current quarter, delete all the
    # records for this quarter so they can be refetched. We do this as platforms
    # update/adjust their metrics (particularly spend metrics) as fraudulent/invalid
    # clicks are refunded.
    if year == 'this' and quarter == get_quarter_from_date(datetime.now()):
        console.print("Report is for this year and this quarter. Dropping records for this quarter.", style="bold, red")
        delete_current_q_records()
    else:
        console.print("Report is not for this quarter and no records have been deleted.", style="bold green")

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all()
