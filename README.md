# About
DG Tracker is an application that tracks SEM platform spend and other metrics across Google 
and Bing. It tracks those metrics and their attainment rates against revenue & conversion data 
in Adobe Analytics. This suite is only going to be useful to those who use SEM platforms but 
Adobe Analytics for their analytics platform. All examples will show EMEA countries only. 

Currently, it supports spend, revenue, ROAS/E:R, Conversion Rate and CTR.

# DB refactor
- [ ] Refactor DB to use SQLAlchemy for DB portability.

# Microsoft Refactor
- [x] Refactor auth
- [x] Refactor settings
- [ ] Refactor DB write
- [ ] Refactor Account, Campaign and Ads reports.

# Google Refactor
- [ ] Refactor queries as parameters for reports


# Adobe Refactor
- [ ] Refactor report file programmatically

### Supplemental Requirements
- Must be stateless.
- Must default to running current week from CLI and parameterize for backfill.
- Must be containerized and scalable using swarm or Kubernetes.
- Container must run on both ARM and X86 so necessary wheels need to be built manually.
- Final Container/Image must be under 100Mb
- Must use clustered managed DB.
- Must have an Airflow DAG for hourly runs.
- Must deliver reports via mail.
- Must stay within rate limits.
- All secrets must be docker/github or env.
- Must have robust test suite (but not TDD).

### Assumptions
- Full documentation to allow for ease of handoff. 
- Application will be easily utilized by other GEOs outside EMEA.
- Application will function correctly regardless of firewall or OTP requirements.


# Milestones
- [ ] Set up dictionary of country and Ads Accounts (Config/Secrets).
- [ ] Set up credentials for Google, MS and Adobe (JSON, Token & KeyFile respectively).
- [ ] Set up DB tables for each quarter programmatically. Single quarter table combining platforms.
- [ ] Set up backfill (separate backfill_database() method with a date range parameter).
- [ ] Set up business date ranges for each platform with custom business fiscal year functionality (Module).
- [ ] Pull basic campaign report or full ads report for each country.
- [ ] Pull program revenue data for each country report suite.
- [ ] Generate necessary database views for merged data.
- [ ] Generate separate tables/views for required reports 
- [ ] Create a front end service/stack (Flask or Django) for report viewing. 



# Modules to build
- [ ] DB Module (dg-db)
- [ ] Business Date Module (dg-date)
- [ ] Google Ads module (dg-google)
- [ ] Microsoft Ads module (dg-ms)
- [ ] Drive upload module (dg-drive)
- [ ] Mail sending module (dg-drive)
- [ ] Report generation (dg-report)


# Maybe Pile
- [ ] Use GitHub Actions for CI/CD
- [ ] Initial development script to automate Docker rebuilds


# Tables
#### (All Sample Data is clearly ridiculously facetious & purely for demonstration only)

Ads report will provide the most granular view of data and future proof it. Campaigns report
will make things easy but limit flexibility. 

### QTD Table (Dummy Data)
| Country | Quarter_Spend_Target | Quarter_Revenue_Target | ER_Target | QTD_ER | QTD_Conversion_Rate | QTD_Conversion_Rate_VS_Last_Year | QTD_Revenue_VS_Last_Year | Week1_Spend_Attainment | Week1_Revenue_Attainment | Week2_Spend_Attainment | Week2_Revenue_Attainment |
|---------|----------------------|------------------------|-----------|--------|---------------------|----------------------------------|--------------------------|------------------------|--------------------------|------------------------|--------------------------|
| UK      |               100000 |                 700000 |        14 |    9.5 |               0.50% |                              10% |                      21% |                    25% |                      25% |                    25% |                      25% |
| IE      |                40000 |                 280000 |        12 |    7.9 |               0.67% |                              12% |                      -4% |                    33% |                      33% |                    33% |                      33% |
| DE      |               500000 |                3500000 |        13 |    6.3 |               1.20% |                              21% |                      -2% |                    21% |                      50% |                    21% |                      50% |
| AT      |                50000 |                 350000 |        12 |    6.5 |               1.00% |                              -4% |                      22% |                    12% |                      45% |                    12% |                      45% |
| CH      |                70000 |                 490000 |        11 |   12.7 |               0.91% |                              -2% |                      21% |                     9% |                      12% |                     9% |                      12% |
| FR      |               400000 |                2800000 |        14 |   10.9 |               0.50% |                              22% |                      10% |                    44% |                      60% |                    44% |                      60% |
| IT      |                70000 |                 490000 |        13 |   10.7 |               0.67% |                              21% |                       6% |                    25% |                      25% |                    25% |                      25% |
| ES      |                50000 |                 350000 |        13 |   12.7 |               1.20% |                              10% |                      21% |                    33% |                      33% |                    33% |                      33% |
| PT      |                50000 |                 350000 |        14 |   28.6 |               1.40% |                              12% |                     -19% |                    21% |                      50% |                    21% |                      50% |
| NO      |                50000 |                 350000 |        13 |   32.8 |               0.91% |                              21% |                       2% |                    12% |                      45% |                    12% |                      45% |
| SE      |                70000 |                 490000 |        15 |   23.8 |               0.50% |                              -4% |                       1% |                     9% |                      12% |                     9% |                      12% |
| FI      |                40000 |                 280000 |        11 |   31.9 |               0.67% |                              -2% |                      21% |                    44% |                      60% |                    44% |                      60% |
| DK      |                70000 |                 490000 |        13 |    2.0 |               1.20% |                              22% |                     -19% |                    21% |                      50% |                    21% |                      50% |
| NL      |                70000 |                 490000 |        12 |   19.7 |               1.00% |                              21% |                       2% |                    12% |                      45% |                    12% |                      45% |
| BE      |                40000 |                 280000 |        12 |   31.9 |               0.91% |                               9% |                       1% |                     9% |                      12% |                     9% |                      12% |


### Weekly Table (Dummy Data)
| Country | Week1_Skew | Week1_Spend_Target | Week1_Spend_Actual | Week1_Spend_Attainment | Week1_Revenue_Target | Week1_Revenue_Actual | Week1_Revenue_Attainment | Week1_Revenue_VS_Last_Year | Week1_Spend_VS_Last_Year | Week1_Conversion_Rate | Week1_Conversion_Rate_VS_Last_Year | Week1_Price_Benchmark | Week1_Price_Benchmark_VS_Last_Year | Week1_CTR | Week1_CTR_VS_Last_Year | Week1_Lost_IS | Week1_Lost_IS_VS_Last_Year |
|---------|------------|--------------------|--------------------|------------------------|----------------------|----------------------|--------------------------|----------------------------|--------------------------|-----------------------|------------------------------------|-----------------------|------------------------------------|-----------|------------------------|---------------|----------------------------|
| UK      |          7 |               7000 |               4000 |                     57 |                49000 |                42000 |                       86 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| IE      |          7 |               2800 |               1000 |                     36 |                19600 |                12600 |                       64 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| DE      |          7 |              35000 |              15000 |                     43 |               245000 |               238000 |                       97 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| AT      |          4 |               2000 |                455 |                     23 |                14000 |                 7000 |                       50 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| CH      |          5 |               3500 |               2230 |                     64 |                24500 |                17500 |                       71 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| FR      |          8 |              32000 |              23556 |                     74 |               224000 |               217000 |                       97 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| IT      |          8 |               5600 |               3440 |                     61 |                39200 |                32200 |                       82 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| ES      |          7 |               3500 |               2230 |                     64 |                24500 |                17500 |                       71 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| PT      |          7 |               3500 |               5000 |                    143 |                24500 |                17500 |                       71 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| NO      |          5 |               2500 |               3440 |                    138 |                17500 |                10500 |                       60 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| SE      |          4 |               2800 |               3000 |                    107 |                19600 |                12600 |                       64 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| FI      |          5 |               2000 |               2230 |                    112 |                14000 |                 7000 |                       50 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| DK      |          6 |               4200 |                455 |                     11 |                29400 |                22400 |                       76 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| NL      |          5 |               3500 |               3440 |                     98 |                24500 |                17500 |                       71 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |
| BE      |          5 |               2000 |               2230 |                    112 |                14000 |                 7000 |                       50 |                            |                          |                       |                                    |                       |                                    |           |                        |               |                            |


### Budget & SKEW Table (Dummy Data)
| Country | Media_Spend | Revenue_Target | ER_Target | Week1_Skew | Week2_Skew | Week3_Skew | Week4_Skew | Week5_Skew | Week6_Skew | Week7_Skew | Week8_Skew | Week9_Skew | Week10_Skew | Week11_Skew | Week12_Skew | Week13_Skew | Week14_Skew |
|---------|-------------|----------------|-----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|-------------|-------------|-------------|-------------|-------------|
| UK      |      100000 |         700000 |        14 |          7 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           1 |
| IE      |       40000 |         280000 |        12 |          7 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           1 |
| DE      |      500000 |        3500000 |        13 |          7 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           1 |
| AT      |       50000 |         350000 |        12 |          4 |          8 |          9 |          7 |         13 |          9 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           3 |
| CH      |       70000 |         490000 |        11 |          5 |         10 |         11 |          5 |         14 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           2 |
| FR      |      400000 |        2800000 |        14 |          8 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           6 |           6 |           3 |           2 |           1 |
| IT      |       70000 |         490000 |        13 |          8 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           6 |           6 |           3 |           2 |           1 |
| ES      |       50000 |         350000 |        13 |          7 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           1 |
| PT      |       50000 |         350000 |        14 |          7 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           1 |
| NO      |       50000 |         350000 |        13 |          5 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           3 |
| SE      |       70000 |         490000 |        15 |          4 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           4 |
| FI      |       40000 |         280000 |        11 |          5 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           3 |
| DK      |       70000 |         490000 |        13 |          6 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           2 |
| NL      |       70000 |         490000 |        12 |          5 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           2 |           3 |
| BE      |       40000 |         280000 |        12 |          5 |          8 |         11 |          5 |         15 |          6 |          9 |          8 |         12 |           7 |           6 |           3 |           1 |           4 |