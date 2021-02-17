def get_region(country_name):
    # Normalize as Adobe returns names in different cases.
    normalized_country_name = country_name.casefold().strip()

    # North
    if normalized_country_name == "nl" or normalized_country_name == "bing lenovo nl" or normalized_country_name == "lenovo netherlands brand" or normalized_country_name == "lenovonlpub":
        return 'North'
    elif normalized_country_name == "dk" or normalized_country_name == "bing lenovo dk" or normalized_country_name == "lenovo denmark brand" or normalized_country_name == "lenovodkpub":
        return 'North'
    elif normalized_country_name == "se" or normalized_country_name == "lenovo sweden direct" or normalized_country_name == "lenovo sweden brand" or normalized_country_name == "lenovosepub":
        return 'North'
    elif normalized_country_name == "fi" or normalized_country_name == "lenovo finland direct" or normalized_country_name == "lenovo finland brand" or normalized_country_name == "lenovofipub":
        return 'North'
    elif normalized_country_name == "be" or normalized_country_name == "lenovo belgium" or normalized_country_name == "lenovo belgium brand" or normalized_country_name == "lenovobepub":
        return 'North'
    elif normalized_country_name == "no" or normalized_country_name == "lenovo norway" or normalized_country_name == "lenovo norway brand" or normalized_country_name == "lenovonopub":
        return 'North'

    # Central
    elif normalized_country_name == "de" or normalized_country_name == "lenovo germany direct" or normalized_country_name == "lenovo germany brand" or normalized_country_name == "lenovodepub":
        return 'Central'
    elif normalized_country_name == "at" or normalized_country_name == "lenovo austria direct" or normalized_country_name == "lenovo austria brand" or normalized_country_name == "lenovoatpub":
        return 'Central'
    elif normalized_country_name == "ch" or normalized_country_name == "lenovo switzerland direct" or normalized_country_name == "lenovo switzerland brand" or normalized_country_name == "lenovochpub":
        return 'Central'
    # South
    elif normalized_country_name == "fr" or normalized_country_name == "lenovo france direct" or normalized_country_name == "lenovo france brand" or normalized_country_name == "lenovofrpub":
        return 'South'
    elif normalized_country_name == "es" or normalized_country_name == "lenovo spain" or normalized_country_name == "lenovo spain brand" or normalized_country_name == "lenovoespub":
        return 'South'
    elif normalized_country_name == "it" or normalized_country_name == "lenovo italy" or normalized_country_name == "lenovo italy brand" or normalized_country_name == "lenovoitpub":
        return 'South'
    elif normalized_country_name == "pt" or normalized_country_name == "portugal" or normalized_country_name == "lenovo portugal brand" or normalized_country_name == "lenovoptpub":
        return 'South'
    # UKI
    elif normalized_country_name == "gb" or normalized_country_name == "lenovo uk direct" or normalized_country_name == "united kingdom" or normalized_country_name == "lenovo uk brand" or normalized_country_name == "lenovogbpub":
        return 'UKI'
    elif normalized_country_name == "ie" or normalized_country_name == "lenovo ireland direct" or normalized_country_name == "lenovo ireland brand" or normalized_country_name == "lenovoiepub":
        return 'UKI'

    else:
        return "Unknown Region"
