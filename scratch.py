from dg_db.db_utils import get_session
from dg_models.account_model import Account
from dg_models.platform_model import Platform
from dg_utils.clean_country import clean_country_name


def get_foreign_keys(table_name):
    # Get the foreign Keys for all Accounts as we can't insert with a query on a foreign key using
    # SQLAlchemy bulk insert.
    account_fk_dict = {}
    google_platform_fk_dict = {}
    microsoft_platform_fk_dict = {}
    session = get_session()

    if table_name == "accounts":
        accounts = session.query(Account.id, Account.account_name).all()
        for account in accounts:
            account_fk_dict.update({account.account_name: account.id})
        return account_fk_dict

    elif table_name == "google_platforms":
        google_platforms = session.query(Platform.id, Platform.account).filter_by(platform="Google").all()
        for platform in google_platforms:
            google_platform_fk_dict.update({platform.account: platform.id})
        return google_platform_fk_dict


    elif table_name == "microsoft_platforms":
        microsoft_platforms = session.query(Platform.id, Platform.account).filter_by(platform="Microsoft").all()
        for platform in microsoft_platforms:
            microsoft_platform_fk_dict.update({platform.account: platform.id})
        return microsoft_platform_fk_dict

    session.close()


test_platform = get_foreign_keys("google_platforms").get(get_foreign_keys("accounts").get("Ireland"))
print(test_platform)

