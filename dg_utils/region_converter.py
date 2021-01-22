def get_region(country_name):
    # Normalize as Adobe returns names in different cases.
    normalized_country_name = country_name.casefold().strip()

    # North
    if normalized_country_name == "nl" or normalized_country_name == "netherlands":
        return 'North'
    elif normalized_country_name == "dk" or normalized_country_name == "denmark":
        return 'North'
    elif normalized_country_name == "se" or normalized_country_name == "sweden":
        return 'North'
    elif normalized_country_name == "fi" or normalized_country_name == "finland":
        return 'North'
    elif normalized_country_name == "be" or normalized_country_name == "belgium":
        return 'North'
    elif normalized_country_name == "no" or normalized_country_name == "norway":
        return 'North'

    # Central
    elif normalized_country_name == "de" or normalized_country_name == "germany":
        return 'Central'
    elif normalized_country_name == "at" or normalized_country_name == "austria":
        return 'Central'
    elif normalized_country_name == "ch" or normalized_country_name == "switzerland":
        return 'Central'
    # South
    elif normalized_country_name == "fr" or normalized_country_name == "france":
        return 'South'
    elif normalized_country_name == "es" or normalized_country_name == "spain":
        return 'South'
    elif normalized_country_name == "it" or normalized_country_name == "italy":
        return 'South'
    elif normalized_country_name == "pt" or normalized_country_name == "portugal":
        return 'South'
    # UKI
    elif normalized_country_name == "uk" or normalized_country_name == "gb" or normalized_country_name == "united kingdom":
        return 'UKI'
    elif normalized_country_name == "ie" or normalized_country_name == "ireland":
        return 'UKI'

    else:
        return "Unknown Region"
