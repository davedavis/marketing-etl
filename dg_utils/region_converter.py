def get_region(country_name):
    # North
    if ' NL' in country_name or 'Netherlands' in country_name:
        return 'North'
    elif ' DK' in country_name or 'Denmark' in country_name:
        return 'North'
    elif 'SE' in country_name or 'Sweden' in country_name:
        return 'North'
    elif ' FI' in country_name or 'Finland' in country_name:
        return 'North'
    elif ' BE' in country_name or 'Belgium' in country_name:
        return 'North'
    elif 'NO' in country_name or 'Norway' in country_name:
        return 'North'
    # Central
    elif ' DE' in country_name or 'Germany' in country_name:
        return 'Central'
    elif ' AT' in country_name or 'Austria' in country_name:
        return 'Central'
    elif ' CH' in country_name or 'Switzerland' in country_name:
        return 'Central'
    # South
    elif ' FR' in country_name or 'France' in country_name:
        return 'South'
    elif ' ES' in country_name or 'Spain' in country_name:
        return 'South'
    elif ' IT' in country_name or 'Italy' in country_name:
        return 'South'
    elif ' PT' in country_name or 'Portugal' in country_name:
        return 'South'
    # UKI
    elif ' UK' in country_name or 'Kingdom' in country_name:
        return 'UKI'
    elif ' IE' in country_name or 'Ireland' in country_name:
        return 'UKI'