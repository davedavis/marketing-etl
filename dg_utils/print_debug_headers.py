# This file is for debugging and simply provides the column headers for the responses in the console.
# Eventually, they will be removed completely and it will run silently. Possibly with some progress bars instead.


def print_start_message():
    print("Getting Reports & POEs Ready...")


def print_truncate_message():
    print("Clearing or creating the DBs...")


def print_google_search_poes_headers():
    print('Date', '\t', 'Platform', '\t', 'Account', '\t', 'Campaign', '\t', 'Cost', '\t', 'Impressions', '\t',
          'Clicks', '\t',
          'CTR' '\t',
          'Conversions', '\t',
          'Headline1', '\t', 'Headline2', '\t', 'Headline3', '\t', 'Description', '\t',
          'Expanded Text Ad Description 2', '\t',
          'DSA Description 1', '\t', 'DSA Description 2', '\t',
          'RSA Headline 1', '\t', 'RSA Headline 2', '\t', 'RSA Headline 3', '\t', 'RSA Headline 4' '\t',
          'RSA Headline 5', '\t',
          'RSA Headline 6', '\t', 'RSA Headline 7', '\t', 'RSA Headline 8', '\t', 'RSA Headline 9' '\t',
          'RSA Headline 10', '\t',
          'RSA Headline 11', '\t', 'RSA Headline 12', '\t', 'RSA Headline 13', '\t', 'RSA Headline 14' '\t',
          'RSA Headline 15' '\t',
          'RSA Description 1', '\t', 'RSA Description 2', '\t', 'RSA Description 3', '\t', 'RSA Description 4'
          )


def print_google_shopping_poes_headers():
    print('TimePeriod', '\t', 'Platform', '\t', 'Account', '\t', 'Campaign', '\t', 'Title', '\t', 'Cost', '\t',
          'Impressions' '\t', 'Clicks', '\t', 'CTR'
          )


def print_bing_search_poes_headers():
    print('Month Starting', '\t', 'Platform', '\t', 'AccountName', '\t', 'CampaignName', '\t', 'AdGroupName', '\t',
          'CurrencyCode', '\t', 'AdDistribution' '\t', 'AdType', '\t', 'Impressions', '\t', 'Clicks', '\t', 'Ctr', '\t',
          'AverageCpc', '\t', 'Spend', '\t', 'AdTitle', '\t', 'AdDescription', '\t', 'AdDescription2', '\t',
          'TitlePart1', '\t', 'TitlePart2', '\t', 'TitlePart3' '\t', 'Path1', '\t', 'Path1', '\t'
          )


def print_bing_qtd_accounts_headers():
    print('Unit of Time', 'Account Number', 'Account Name', 'Impressions', 'Clicks', 'Spend', sep='\t')


def print_bing_shopping_poes_headers():
    print('Date', '\t', 'Platform', '\t', 'AccountName', '\t', 'CampaignName', '\t', 'AdGroupName', '\t',
          'CurrencyCode', '\t', 'Title' '\t', 'Brand', '\t', 'Price', '\t', 'Impressions', '\t', 'Clicks', '\t',
          'Ctr', '\t', 'AverageCpc', '\t', 'Spend', '\t', 'SellerName', '\t', 'OfferLanguage', '\t',
          'CountryOfSale', '\t', 'TotalClicksOnAdElements', '\t', 'ClickType' '\t', 'MerchantProductId', '\t'
          )