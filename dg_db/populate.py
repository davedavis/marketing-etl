from dg_db.db_write import write_countries, write_skews, write_platforms


def populate_accounts():

    countries = [
        ("Germany", "DE", "Central", "Gat"),
        ("Austria", "AT", "Central", "Gat"),
        ("Switzerland", "CH", "Central", "None"),
        ("France", "FR", "South", "None"),
        ("Italy", "IT", "South", "None"),
        ("Spain", "ES", "South", "Iberia"),
        ("Portugal", "PT", "South", "Iberia"),
        ("Denmark", "DK", "North", "None"),
        ("Norway", "NO", "North", "None"),
        ("Sweden", "SE", "North", "None"),
        ("Finland", "FI", "North", "None"),
        ("Netherlands", "NL", "North", "Benelux"),
        ("Belgium", "BE", "North", "Benelux"),
        ("UK", "UK", "UKI", "None"),
        ("Ireland", "IE", "UKI", "None"),
    ]

    write_countries(countries)


def populate_platforms():

    platforms = [
        (1, "Google", "8005495881"),
        (2, "Google", "4825989316"),
        (3, "Google", "1345515457"),
        (4, "Google", "3136320411"),
        (5, "Google", "3456991375"),
        (6, "Google", "6033808683"),
        (7, "Google", "1795086707"),
        (8, "Google", "9503587615"),
        (9, "Google", "1739364726"),
        (10, "Google", "7245755087"),
        (11, "Google", "1332379677"),
        (12, "Google", "7966843210"),
        (13, "Google", "3704484034"),
        (14, "Google", "8457701491"),
        (15, "Google", "3377816067"),
        (1, "Microsoft", "X7356537"),
        (2, "Microsoft", "X7004130"),
        (3, "Microsoft", "F1071RW6"),
        (4, "Microsoft", "X8349003"),
        (5, "Microsoft", "B004ETLE"),
        (6, "Microsoft", "B004V7BM"),
        (7, "Microsoft", "NOTAVAIL"),
        (8, "Microsoft", "X000XGAU"),
        (9, "Microsoft", "B004SUHL"),
        (10, "Microsoft", "F107DTZT"),
        (11, "Microsoft", "F1074ELB"),
        (12, "Microsoft", "X0006AXW"),
        (13, "Microsoft", "B004295N"),
        (14, "Microsoft", "F107P4UT"),
        (15, "Microsoft", "F107MVC9")
    ]

    write_platforms(platforms)


def populate_skews():

    records_to_insert = [
        ("UK", 492693, 2458665, 0.20, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
        ("IE", 51965, 409777, 0.13, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
        ("DE", 729221, 3698601, 0.20, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("AT", 111815, 821338, 0.14, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("CH", 157896, 1044068, 0.15, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("FR", 230684, 1120651, 0.20, 0.02, 0.06, 0.07, 0.09, 0.09, 0.09, 0.11, 0.07, 0.11, 0.06, 0.06, 0.06, 0.07, 0.03),
        ("ES", 95035, 545993, 0.17, 0.06, 0.06, 0.06, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.09, 0.08, 0.08, 0.08, 0.04),
        ("IT", 127896, 816425, 0.16, 0.03, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("PT", 16885, 60524, 0.27, 0.05, 0.06, 0.06, 0.07, 0.08, 0.08, 0.09, 0.07, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
        ("NO", 26584, 150431, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("SE", 44339, 243477, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("FI", 23039, 133146, 0.17, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("DK", 83330, 553985, 0.15, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("NL", 110166, 604416, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
        ("BE", 73444, 450679, 0.16, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03)
    ]

    formatted_skews = []

    # Format skew list into DB table format.
    for row in records_to_insert:
        skew_range = range(4, 18)
        for n, week in enumerate(skew_range):
            formatted_skews.append((row[0], 4, n + 1, row[1] * row[week], row[2] * row[week], row[3]))

    write_skews(formatted_skews)