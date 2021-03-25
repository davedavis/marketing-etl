def get_report_type(report_type, date_range):
    if report_type == 'accounts':
        report = get_account_report_type(date_range)

    elif report_type == 'campaigns':
        report = get_campaign_report_type(date_range)

    elif report_type == 'ads':
        report = get_search_ads_report_type(date_range)

    elif report_type == 'shopping':
        report = get_shopping_ads_report_type(date_range)

    elif report_type == 'budgetcap':
        report = get_budget_opportunities_report_type(date_range)

    else:
        print("You need to provide a Google Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping.")
        report = None

    return report


def get_account_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions
                         FROM customer 
                         WHERE segments.date 
                         BETWEEN {date_range}
                         AND metrics.cost_micros > 0'''
    return report_request


def get_budget_opportunities_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, campaign_budget.has_recommended_budget, campaign_budget.amount_micros, campaign_budget.status,
                         campaign_budget.recommended_budget_amount_micros, 
                         campaign.name, campaign.id, segments.date, segments.budget_campaign_association_status.campaign, segments.budget_campaign_association_status.status
                         FROM campaign_budget 
                         WHERE segments.date BETWEEN {date_range}
                         AND campaign_budget.has_recommended_budget = True'''
    return report_request


def get_campaign_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, segments.date, metrics.cost_micros, metrics.clicks, 
                                metrics.impressions, metrics.impressions, metrics.cost_per_conversion,
                                metrics.value_per_conversion, metrics.conversions_value, 
                                metrics.conversions_from_interactions_rate, metrics.search_impression_share, 
                                metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share,
                                campaign.status, campaign.name, campaign.id, campaign.advertising_channel_type
                         FROM campaign 
                         WHERE segments.date 
                         BETWEEN {date_range}
                         AND metrics.cost_micros > 0'''
    return report_request


def get_search_ads_report_type(date_range):
    report_request = f'''SELECT campaign.name, ad_group.name, customer.id, customer.descriptive_name,
                        campaign.advertising_channel_type,
                        segments.date,
                        ad_group_ad.ad.expanded_text_ad.headline_part1,
                        ad_group_ad.ad.expanded_text_ad.headline_part2, 
                        ad_group_ad.ad.expanded_text_ad.headline_part3,
                        ad_group_ad.ad.expanded_text_ad.description,
                        ad_group_ad.ad.expanded_text_ad.description2,
                        ad_group_ad.ad.expanded_dynamic_search_ad.description,
                        ad_group_ad.ad.expanded_dynamic_search_ad.description2,
                        ad_group_ad.ad.responsive_search_ad.headlines,
                        ad_group_ad.ad.expanded_text_ad.path1,
                        ad_group_ad.ad.expanded_text_ad.path2,
                        ad_group_ad.ad.responsive_search_ad.descriptions,
                        customer.currency_code,
                        metrics.average_cpc,
                        ad_group_ad.ad.shopping_product_ad,
                        metrics.cost_micros,
                        metrics.impressions,
                        metrics.clicks,
                        metrics.ctr,
                        metrics.conversions
                        FROM ad_group_ad
                        WHERE segments.date BETWEEN {date_range}
                        AND campaign.advertising_channel_type = 'SEARCH'
                        AND metrics.cost_micros > 0
                        ORDER BY segments.date
                        '''

    return report_request


def get_shopping_ads_report_type(date_range):
    report_request = f'''SELECT campaign.name, ad_group.name, customer.id, customer.descriptive_name,
                        campaign.advertising_channel_type,
                        segments.date,
                        segments.product_title,
                        metrics.clicks,  
                        metrics.cost_micros,  
                        metrics.impressions, 
                        metrics.average_cpc,
                        metrics.ctr
                        FROM  shopping_performance_view
                        WHERE segments.date BETWEEN {date_range}
                          AND metrics.cost_micros > 0
                        ORDER BY
                            segments.date
                        '''

    return report_request
