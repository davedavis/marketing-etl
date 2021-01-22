# Simple helper function that takes in the account name and returns the country name. This is needed as there
# is no consistency between account names across platforms, especially Bing.

def clean_country_name(dirty_name):
    # Normalize as Adobe returns names in different cases.
    normalized_country_name = dirty_name.casefold().strip()

    # North
    if normalized_country_name == "nl" or normalized_country_name == "netherlands":
        return 'Netherlands'
    elif normalized_country_name == "dk" or normalized_country_name == "denmark":
        return 'Denmark'
    elif normalized_country_name == "se" or normalized_country_name == "sweden":
        return 'Sweden'
    elif normalized_country_name == "fi" or normalized_country_name == "finland":
        return 'Finland'
    elif normalized_country_name == "be" or normalized_country_name == "belgium":
        return 'Belgium'
    elif normalized_country_name == "no" or normalized_country_name == "norway":
        return 'Norway'

    # Central
    elif normalized_country_name == "de" or normalized_country_name == "germany":
        return 'Germany'
    elif normalized_country_name == "at" or normalized_country_name == "austria":
        return 'Austria'
    elif normalized_country_name == "ch" or normalized_country_name == "switzerland":
        return 'Switzerland'
    # South
    elif normalized_country_name == "fr" or normalized_country_name == "france":
        return 'France'
    elif normalized_country_name == "es" or normalized_country_name == "spain":
        return 'Spain'
    elif normalized_country_name == "it" or normalized_country_name == "italy":
        return 'Italy'
    elif normalized_country_name == "pt" or normalized_country_name == "portugal":
        return 'Portugal'
    # UKI
    elif normalized_country_name == "uk" or normalized_country_name == "gb" or normalized_country_name == "united kingdom":
        return 'UK'
    elif normalized_country_name == "ie" or normalized_country_name == "ireland":
        return 'Ireland'

    else:
        return "Unknown Country"
