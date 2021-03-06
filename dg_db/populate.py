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
        (1, "Google", "8005495881", "2059894093"),
        (2, "Google", "4825989316", "4302291843"),
        (3, "Google", "1345515457", "5635690780"),
        (4, "Google", "3136320411", "7447885588"),
        (5, "Google", "3456991375", "2037891425"),
        (6, "Google", "6033808683", "9021596480"),
        (7, "Google", "1795086707", "4753585796"),
        (8, "Google", "9503587615", "7310537721"),
        (9, "Google", "1739364726", "8212508088"),
        (10, "Google", "7245755087", "7575293197"),
        (11, "Google", "1332379677", "1904670595"),
        (12, "Google", "7966843210", "9271529992"),
        (13, "Google", "3704484034", "6338903272"),
        (14, "Google", "8457701491", "1150412027"),
        (15, "Google", "3377816067", "6186544301"),
        (1, "Microsoft", "X7356537", "X7356537"),
        (2, "Microsoft", "X7004130", "X7004130"),
        (3, "Microsoft", "F1071RW6", "F1071RW6"),
        (4, "Microsoft", "X8349003", "X8349003"),
        (5, "Microsoft", "B004ETLE", "B004ETLE"),
        (6, "Microsoft", "B004V7BM", "B004V7BM"),
        (7, "Microsoft", "NOTAVAIL", "NOTAVAIL"),
        (8, "Microsoft", "X000XGAU", "X000XGAU"),
        (9, "Microsoft", "B004SUHL", "B004SUHL"),
        (10, "Microsoft", "F107DTZT", "F107DTZT"),
        (11, "Microsoft", "F1074ELB", "F1074ELB"),
        (12, "Microsoft", "X0006AXW", "X0006AXW"),
        (13, "Microsoft", "B004295N", "B004295N"),
        (14, "Microsoft", "F107P4UT", "F107P4UT"),
        (15, "Microsoft", "F107MVC9", "F107MVC9")
    ]

    write_platforms(platforms)


def populate_skews():

    # Q2 22
    records_to_insert = [
        ("UK", 910534.84, 4660585.24, 0.1954, 0.0173, 0.0419, 0.0440, 0.0692, 0.0533, 0.0533, 0.0551, 0.0589, 0.2653, 0.0677, 0.0799, 0.0810, 0.0810, 0.0320),
        ("IE", 102951.89, 727779.08, 0.1415, 0.0180, 0.0437, 0.0459, 0.0722, 0.0556, 0.0556, 0.0574, 0.0614, 0.2339, 0.0706, 0.0833, 0.0844, 0.0844, 0.0334),
        ("DE", 1109019.05, 5427544.86, 0.2043, 0.0153, 0.0400, 0.0438, 0.0762, 0.0514, 0.0533, 0.0552, 0.0590, 0.2649, 0.0670, 0.0789, 0.0812, 0.0812, 0.0325),
        ("AT", 105074.22, 745541.88, 0.1409, 0.0160, 0.0417, 0.0457, 0.0794, 0.0536, 0.0556, 0.0576, 0.0616, 0.2335, 0.0700, 0.0826, 0.0850, 0.0842, 0.0335),
        ("CH", 240387.78, 1437894.37, 0.1672, 0.0218, 0.0496, 0.0595, 0.0811, 0.0811, 0.0811, 0.0991, 0.0631, 0.1295, 0.0673, 0.0737, 0.0737, 0.0804, 0.0389),
        ("FR", 529057.49, 2634799.26, 0.2008, 0.0170, 0.0348, 0.0382, 0.0531, 0.0448, 0.0481, 0.0498, 0.0514, 0.2308, 0.0638, 0.0705, 0.1072, 0.1440, 0.0466),
        ("ES", 153548.47, 807181.61, 0.1902, 0.0170, 0.0348, 0.0382, 0.0531, 0.0448, 0.0481, 0.0498, 0.0514, 0.2308, 0.0638, 0.0705, 0.1072, 0.1440, 0.0466),
        ("IT", 165266.60, 898683.98, 0.1839, 0.0270, 0.0505, 0.0586, 0.0631, 0.0622, 0.0712, 0.0667, 0.0703, 0.1558, 0.0930, 0.0842, 0.0842, 0.0797, 0.0337),
        ("PT", 39063.01, 148691.35, 0.2627, 0.0270, 0.0631, 0.0631, 0.0721, 0.0721, 0.0721, 0.0811, 0.0631, 0.0945, 0.0821, 0.0885, 0.0885, 0.0885, 0.0442),
        ("NO", 49170.23, 213901.64, 0.2299, 0.0270, 0.0505, 0.0586, 0.0631, 0.0622, 0.0712, 0.0667, 0.0703, 0.1558, 0.0930, 0.0842, 0.0842, 0.0797, 0.0337),
        ("SE", 68291.98, 315653.46, 0.2164, 0.0361, 0.0541, 0.0586, 0.0811, 0.0631, 0.0856, 0.0631, 0.0631, 0.1170, 0.0748, 0.0807, 0.0807, 0.0807, 0.0612),
        ("FI", 32780.15, 151513.66, 0.2164, 0.0361, 0.0541, 0.0586, 0.0811, 0.0631, 0.0856, 0.0631, 0.0631, 0.1170, 0.0748, 0.0807, 0.0807, 0.0807, 0.0613),
        ("DK", 122925.57, 635020.50, 0.1936, 0.0361, 0.0541, 0.0586, 0.0811, 0.0631, 0.0856, 0.0631, 0.0631, 0.1170, 0.0748, 0.0807, 0.0807, 0.0807, 0.0612),
        ("NL", 170456.79, 834216.40, 0.2043, 0.0406, 0.0628, 0.0628, 0.0679, 0.0679, 0.0787, 0.0763, 0.0652, 0.1213, 0.0732, 0.0848, 0.0821, 0.0795, 0.0369),
        ("BE", 113637.86, 617938.08, 0.1839, 0.0406, 0.0628, 0.0628, 0.0679, 0.0679, 0.0787, 0.0763, 0.0652, 0.1213, 0.0732, 0.0848, 0.0821, 0.0795, 0.0369)
    ]

    # Q1 Final (Reduced Budget)
    # records_to_insert = [
    #     ("UK", 850737, 3511354, 0.24, 0.02, 0.04, 0.04, 0.07, 0.05, 0.05, 0.06, 0.06, 0.27, 0.07, 0.08, 0.08, 0.08, 0.03),
    #     ("IE", 92370, 564691, 0.16, 0.02, 0.04, 0.05, 0.07, 0.06, 0.06, 0.06, 0.06, 0.23, 0.07, 0.08, 0.08, 0.08, 0.03),
    #     ("DE", 1085957, 3956971, 0.27, 0.02, 0.04, 0.04, 0.08, 0.05, 0.05, 0.06, 0.06, 0.26, 0.07, 0.08, 0.08, 0.08, 0.03),
    #     ("AT", 98265, 508753, 0.19, 0.02, 0.04, 0.05, 0.08, 0.05, 0.06, 0.06, 0.06, 0.23, 0.07, 0.08, 0.09, 0.08, 0.03),
    #     ("CH", 195306, 996198, 0.20, 0.02, 0.05, 0.06, 0.08, 0.08, 0.08, 0.10, 0.06, 0.13, 0.07, 0.07, 0.07, 0.08, 0.04),
    #     ("FR", 531644, 1648781, 0.32, 0.02, 0.03, 0.04, 0.05, 0.04, 0.05, 0.05, 0.05, 0.23, 0.06, 0.07, 0.11, 0.14, 0.05),
    #     ("ES", 126968, 590136, 0.22, 0.02, 0.03, 0.04, 0.05, 0.04, 0.05, 0.05, 0.05, 0.23, 0.06, 0.07, 0.11, 0.14, 0.05),
    #     ("IT", 137325, 567718, 0.24, 0.03, 0.05, 0.06, 0.06, 0.06, 0.07, 0.07, 0.07, 0.16, 0.09, 0.08, 0.08, 0.08, 0.03),
    #     ("PT", 32134, 101955, 0.32, 0.03, 0.06, 0.06, 0.07, 0.07, 0.07, 0.08, 0.06, 0.09, 0.08, 0.09, 0.09, 0.09, 0.04),
    #     ("NO", 39934, 168357, 0.24, 0.03, 0.05, 0.06, 0.06, 0.06, 0.07, 0.07, 0.07, 0.16, 0.09, 0.08, 0.08, 0.08, 0.03),
    #     ("SE", 55464, 167020, 0.33, 0.04, 0.05, 0.06, 0.08, 0.06, 0.09, 0.06, 0.06, 0.12, 0.07, 0.08, 0.08, 0.08, 0.06),
    #     ("FI", 26623, 101548, 0.26, 0.04, 0.05, 0.06, 0.08, 0.06, 0.09, 0.06, 0.06, 0.12, 0.07, 0.08, 0.08, 0.08, 0.06),
    #     ("DK", 99835, 440934, 0.23, 0.04, 0.05, 0.06, 0.08, 0.06, 0.09, 0.06, 0.06, 0.12, 0.07, 0.08, 0.08, 0.08, 0.06),
    #     ("NL", 136775, 542948, 0.25, 0.04, 0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.07, 0.12, 0.07, 0.08, 0.08, 0.08, 0.04),
    #     ("BE", 91184, 398162, 0.23, 0.04, 0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.07, 0.12, 0.07, 0.08, 0.08, 0.08, 0.04)
    # ]


    # Q1 22
    # records_to_insert = [
    #     ("UK", 659636, 3970904, 0.1661, 0.0227, 0.0550, 0.0577, 0.0909, 0.0700, 0.0700, 0.0723, 0.0773, 0.1104, 0.0784, 0.0861, 0.0873, 0.0873, 0.0345),
    #     ("IE", 73293, 638596, 0.1148, 0.0227, 0.0550, 0.0577, 0.0909, 0.0700, 0.0700, 0.0723, 0.0773, 0.1104, 0.0784, 0.0861, 0.0873, 0.0873, 0.0345),
    #     ("DE", 826140, 4474841, 0.1846, 0.0201, 0.0525, 0.0575, 0.1000, 0.0675, 0.0700, 0.0725, 0.0775, 0.1100, 0.0775, 0.0850, 0.0875, 0.0875, 0.0350),
    #     ("AT", 81706, 575337, 0.1420, 0.0201, 0.0525, 0.0575, 0.1000, 0.0675, 0.0700, 0.0725, 0.0775, 0.1100, 0.0775, 0.0850, 0.0875, 0.0875, 0.0350),
    #     ("CH", 175908, 1126576, 0.1561, 0.0201, 0.0525, 0.0575, 0.1000, 0.0675, 0.0700, 0.0725, 0.0775, 0.1100, 0.0775, 0.0850, 0.0875, 0.0875, 0.0350),
    #     ("FR", 359010, 1864565, 0.1925, 0.0255, 0.0525, 0.0575, 0.0800, 0.0675, 0.0725, 0.0750, 0.0775, 0.1099, 0.0850, 0.0875, 0.0875, 0.0875, 0.0350),
    #     ("ES", 116539, 667371, 0.1746, 0.0255, 0.0525, 0.0575, 0.0800, 0.0675, 0.0725, 0.0750, 0.0775, 0.1099, 0.0850, 0.0875, 0.0875, 0.0875, 0.0350),
    #     ("IT", 123686, 642018, 0.1927, 0.0255, 0.0525, 0.0575, 0.0800, 0.0675, 0.0725, 0.0750, 0.0775, 0.1099, 0.0850, 0.0875, 0.0875, 0.0875, 0.0350),
    #     ("PT", 28942, 115298, 0.2510, 0.0255, 0.0525, 0.0575, 0.0800, 0.0675, 0.0725, 0.0750, 0.0775, 0.1099, 0.0850, 0.0875, 0.0875, 0.0875, 0.0350),
    #     ("NO", 35968, 190390, 0.1889, 0.0400, 0.0600, 0.0650, 0.0900, 0.0700, 0.0950, 0.0700, 0.0700, 0.0950, 0.0725, 0.0725, 0.0725, 0.0725, 0.0550),
    #     ("SE", 49955, 188879, 0.2645, 0.0400, 0.0600, 0.0650, 0.0900, 0.0700, 0.0950, 0.0700, 0.0700, 0.0950, 0.0725, 0.0725, 0.0725, 0.0725, 0.0550),
    #     ("FI", 23979, 114839, 0.2088, 0.0400, 0.0600, 0.0650, 0.0900, 0.0700, 0.0950, 0.0700, 0.0700, 0.0950, 0.0725, 0.0725, 0.0725, 0.0725, 0.0550),
    #     ("DK", 89919, 498641, 0.1803, 0.0400, 0.0600, 0.0650, 0.0900, 0.0700, 0.0950, 0.0700, 0.0700, 0.0950, 0.0725, 0.0725, 0.0725, 0.0725, 0.0550),
    #     ("NL", 123191, 614006, 0.2006, 0.0450, 0.0697, 0.0697, 0.0753, 0.0753, 0.0873, 0.0847, 0.0723, 0.0997, 0.0703, 0.0750, 0.0727, 0.0703, 0.0327),
    #     ("BE", 82127, 450271, 0.1824, 0.0450, 0.0697, 0.0697, 0.0753, 0.0753, 0.0873, 0.0847, 0.0723, 0.0997, 0.0703, 0.0750, 0.0727, 0.0703, 0.0327)
    # ]



    # // Q4
    # records_to_insert = [
    #     ("UK", 492693, 2458665, 0.20, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
    #     ("IE", 51965, 409777, 0.13, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
    #     ("DE", 729221, 3698601, 0.20, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
    #     ("AT", 111815, 821338, 0.14, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
    #     ("CH", 157896, 1044068, 0.15, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
    #     ("FR", 230684, 1120651, 0.20, 0.02, 0.06, 0.07, 0.09, 0.09, 0.09, 0.11, 0.07, 0.11, 0.06, 0.06, 0.06, 0.07, 0.03),
    #     ("ES", 95035, 545993, 0.17, 0.06, 0.06, 0.06, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.09, 0.08, 0.08, 0.08, 0.04),
    #     ("IT", 127896, 816425, 0.16, 0.03, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.04),
    #     ("PT", 16885, 60524, 0.27, 0.05, 0.06, 0.06, 0.07, 0.08, 0.08, 0.09, 0.07, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
    #     ("NO", 26584, 150431, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
    #     ("SE", 44339, 243477, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
    #     ("FI", 23039, 133146, 0.17, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
    #     ("DK", 83330, 553985, 0.15, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
    #     ("NL", 110166, 604416, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
    #     ("BE", 73444, 450679, 0.16, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03)
    # ]

    formatted_skews = []

    # Format skew list into DB table format.
    for row in records_to_insert:
        skew_range = range(4, 18)
        for n, week in enumerate(skew_range):
            formatted_skews.append((row[0], 4, n + 1, row[1] * row[week], row[2] * row[week], row[3]))

    write_skews(formatted_skews)