# Simple helper function that takes in the account name and returns the country name. This is needed as there
# is no consistency between account names across platforms, especially Bing.

def clean_country_name(dirty_name):
    # Normalize as Adobe returns names in different cases.
    normalized_country_name = dirty_name.casefold().strip()

    # North
    if normalized_country_name == "nl" or normalized_country_name == "bing lenovo nl" or normalized_country_name == "lenovo netherlands brand" or normalized_country_name == "lenovonlpub":
        return 'Netherlands'
    elif normalized_country_name == "dk" or normalized_country_name == "bing lenovo dk" or normalized_country_name == "lenovo denmark brand" or normalized_country_name == "lenovodkpub":
        return 'Denmark'
    elif normalized_country_name == "se" or normalized_country_name == "lenovo sweden direct" or normalized_country_name == "lenovo sweden brand" or normalized_country_name == "lenovosepub":
        return 'Sweden'
    elif normalized_country_name == "fi" or normalized_country_name == "lenovo finland direct" or normalized_country_name == "lenovo finland brand" or normalized_country_name == "lenovofipub":
        return 'Finland'
    elif normalized_country_name == "be" or normalized_country_name == "lenovo belgium" or normalized_country_name == "lenovo belgium brand" or normalized_country_name == "lenovobepub":
        return 'Belgium'
    elif normalized_country_name == "no" or normalized_country_name == "lenovo norway" or normalized_country_name == "lenovo norway brand" or normalized_country_name == "lenovonopub":
        return 'Norway'

    # Central
    elif normalized_country_name == "de" or normalized_country_name == "lenovo germany direct" or normalized_country_name == "lenovo germany brand" or normalized_country_name == "lenovodepub":
        return 'Germany'
    elif normalized_country_name == "at" or normalized_country_name == "lenovo austria direct" or normalized_country_name == "lenovo austria brand" or normalized_country_name == "lenovoatpub":
        return 'Austria'
    elif normalized_country_name == "ch" or normalized_country_name == "lenovo switzerland direct" or normalized_country_name == "lenovo switzerland brand" or normalized_country_name == "lenovochpub":
        return 'Switzerland'
    # South
    elif normalized_country_name == "fr" or normalized_country_name == "lenovo france direct" or normalized_country_name == "lenovo france brand" or normalized_country_name == "lenovofrpub":
        return 'France'
    elif normalized_country_name == "es" or normalized_country_name == "lenovo spain" or normalized_country_name == "lenovo spain brand" or normalized_country_name == "lenovoespub":
        return 'Spain'
    elif normalized_country_name == "it" or normalized_country_name == "lenovo italy" or normalized_country_name == "lenovo italy brand" or normalized_country_name == "lenovoitpub":
        return 'Italy'
    elif normalized_country_name == "pt" or normalized_country_name == "portugal" or normalized_country_name == "lenovo portugal brand" or normalized_country_name == "lenovoptpub":
        return 'Portugal'
    # UKI
    elif normalized_country_name == "gb" or normalized_country_name == "uk" or normalized_country_name == "lenovo uk direct" or normalized_country_name == "lenovo uk brand" or normalized_country_name == "lenovogbpub":
        return 'UK'
    elif normalized_country_name == "ie" or normalized_country_name == "lenovo ireland direct" or normalized_country_name == "lenovo ireland brand" or normalized_country_name == "lenovoiepub":
        return 'Ireland'

    else:
        return "Unknown Country"
