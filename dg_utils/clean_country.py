# Simple helper function that takes in the account name and returns the country name. This is needed as there
# is no consistency between account names across platforms, especially Bing.

def clean_country_name(dirty_name):
    # North
    if ' NL' in dirty_name or 'Netherlands' in dirty_name:
        return 'Netherlands'
    elif ' DK' in dirty_name or 'Denmark' in dirty_name:
        return 'Denmark'
    elif 'SE' in dirty_name or 'Sweden' in dirty_name:
        return 'Sweden'
    elif ' FI' in dirty_name or 'Finland' in dirty_name:
        return 'Finland'
    elif ' BE' in dirty_name or 'Belgium' in dirty_name:
        return 'Belgium'
    elif 'NO' in dirty_name or 'Norway' in dirty_name:
        return 'Norway'
    # Central
    elif ' DE' in dirty_name or 'Germany' in dirty_name:
        return 'Germany'
    elif ' AT' in dirty_name or 'Austria' in dirty_name:
        return 'Austria'
    elif ' CH' in dirty_name or 'Switzerland' in dirty_name:
        return 'Switzerland'
    # South
    elif ' FR' in dirty_name or 'France' in dirty_name:
        return 'France'
    elif ' ES' in dirty_name or 'Spain' in dirty_name:
        return 'Spain'
    elif ' IT' in dirty_name or 'Italy' in dirty_name:
        return 'Italy'
    elif ' PT' in dirty_name or 'Portugal' in dirty_name:
        return 'Portugal'
    # UKI
    elif ' UK' in dirty_name or 'Kingdom' in dirty_name:
        return 'UK'
    elif ' IE' in dirty_name or 'Ireland' in dirty_name:
        return 'Ireland'
