def get_region(country_name):
    # normalize as adobe returns names in different cases.
    normalized_country_name = country_name.casefold().strip()

    # north
    if normalized_country_name == "nl" or normalized_country_name == "bing lenovo nl" or normalized_country_name == "lenovo netherlands brand" or normalized_country_name == "lenovonlpub" or normalized_country_name == "lenovo ecomm | netherlands | €" or normalized_country_name == "lenovo ecomm | microsoft | netherlands | search | €":
        return 'North'
    elif normalized_country_name == "dk" or normalized_country_name == "bing lenovo dk" or normalized_country_name == "lenovo denmark brand" or normalized_country_name == "lenovodkpub" or normalized_country_name == "lenovo ecomm | denmark | €" or normalized_country_name == "lenovo ecomm | microsoft | denmark | search | €":
        return 'North'
    elif normalized_country_name == "se" or normalized_country_name == "lenovo sweden direct" or normalized_country_name == "lenovo sweden brand" or normalized_country_name == "lenovosepub" or normalized_country_name == "lenovo ecomm | sweden | €" or normalized_country_name == "lenovo ecomm | microsoft | sweden | search | €":
        return 'North'
    elif normalized_country_name == "fi" or normalized_country_name == "lenovo finland direct" or normalized_country_name == "lenovo finland brand" or normalized_country_name == "lenovofipub" or normalized_country_name == "lenovo ecomm | finland | €" or normalized_country_name == "lenovo ecomm | microsoft | finland | search | €":
        return 'North'
    elif normalized_country_name == "be" or normalized_country_name == "lenovo belgium" or normalized_country_name == "lenovo belgium brand" or normalized_country_name == "lenovobepub" or normalized_country_name == "lenovo ecomm | belgium | €" or normalized_country_name == "lenovo ecomm | microsoft | belgium | search | €":
        return 'North'
    elif normalized_country_name == "no" or normalized_country_name == "lenovo norway" or normalized_country_name == "lenovo norway brand" or normalized_country_name == "lenovonopub" or normalized_country_name == "lenovo ecomm | norway | €" or normalized_country_name == "lenovo ecomm | microsoft | norway | search | €":
        return 'North'

    # central
    elif normalized_country_name == "de" or normalized_country_name == "lenovo germany direct" or normalized_country_name == "lenovo germany brand" or normalized_country_name == "lenovodepub" or normalized_country_name == "lenovo ecomm | germany | search | €" or normalized_country_name == "lenovo ecomm | microsoft | germany | search | €":
        return 'Central'
    elif normalized_country_name == "at" or normalized_country_name == "lenovo austria direct" or normalized_country_name == "lenovo austria brand" or normalized_country_name == "lenovoatpub" or normalized_country_name == "lenovo ecomm | austria | search | €" or normalized_country_name == "lenovo ecomm | microsoft | austria | search | €":
        return 'Central'
    elif normalized_country_name == "ch" or normalized_country_name == "lenovo switzerland direct" or normalized_country_name == "lenovo switzerland brand" or normalized_country_name == "lenovochpub" or normalized_country_name == "lenovo ecomm | switzerland | €" or normalized_country_name == "lenovo ecomm | microsoft | switzerland | search | €":
        return 'Central'
    # south
    elif normalized_country_name == "fr" or normalized_country_name == "lenovo france direct" or normalized_country_name == "lenovo france brand" or normalized_country_name == "lenovofrpub" or normalized_country_name == "lenovo ecomm | france | search |€" or normalized_country_name == "lenovo ecomm | microsoft | france | search | €":
        return 'South'
    elif normalized_country_name == "es" or normalized_country_name == "lenovo spain" or normalized_country_name == "lenovo spain brand" or normalized_country_name == "lenovoespub" or normalized_country_name == "lenovo ecomm | spain | €" or normalized_country_name == "lenovo ecomm | microsoft | spain | search | €":
        return 'South'
    elif normalized_country_name == "it" or normalized_country_name == "lenovo italy" or normalized_country_name == "lenovo italy brand" or normalized_country_name == "lenovoitpub" or normalized_country_name == "lenovo ecomm | italy | €" or normalized_country_name == "lenovo ecomm | microsoft | italy | search | €":
        return 'South'
    elif normalized_country_name == "pt" or normalized_country_name == "portugal" or normalized_country_name == "lenovo portugal brand" or normalized_country_name == "lenovoptpub" or normalized_country_name == "lenovo ecomm | portugal | €" or normalized_country_name == "lenovo ecomm | microsoft | portugal | search | €":
        return 'South'
    # uki
    elif normalized_country_name == "gb" or normalized_country_name == "lenovo uk direct" or normalized_country_name == "united kingdom" or normalized_country_name == "lenovo uk brand" or normalized_country_name == "lenovogbpub" or normalized_country_name == "lenovo ecomm | uk | search | €" or normalized_country_name == "lenovo ecomm | microsoft | uk | search | €":
        return 'UKI'
    elif normalized_country_name == "ie" or normalized_country_name == "lenovo ireland direct" or normalized_country_name == "lenovo ireland brand" or normalized_country_name == "lenovoiepub"or normalized_country_name == "lenovo ecomm | ireland | search | €" or normalized_country_name == "lenovo ecomm | microsoft | ireland | search | €":
        return 'UKI'

    else:
        return "unknown region"



