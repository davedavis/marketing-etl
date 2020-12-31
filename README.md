# About

DG Tracker is an ETL application that tracks SEM platform spend and
other metrics across Google and Microsoft ads and writes account,
campaign, search ads and shopping ads level data to a database for
easier and fresher reporting. It also pulls Adobe Analytics revenue
reporting data for the accounts reports and puts that inside the
database too.

The reporting and report generation mechanism will be a separate
application.

# DB Requirements

This app is quite flexible on DB choice. However, If you're using MySQL
as your database of choice, you'll need to change the
max_allowed_packets setting to something large for the ads reports to
actually write to the DB. So in your /etc/my.cnf file, add:

`[mysqld]
max_allowed_packet=16M
`


# ToDo

## DB refactor

- [x] Refactor DB to use SQLAlchemy for DB portability.
- [x] Use SQLAlchemy functions to replace queries.

## Microsoft Refactor

- [x] Refactor auth
- [x] Refactor settings
- [x] Refactor DB write
- [x] Refactor Account, Campaign and Ads reports.

## Google Refactor

- [x] Refactor queries as parameters for reports


## Adobe Refactor

- [ ] Refactor report file programmatically

### Supplemental Requirements

- Must be stateless.
- Must default to running current week from CLI and parameterize for
  backfill.
- Must be containerized and scalable using swarm or Kubernetes.
- Container must run on both ARM and X86 so necessary wheels need to be
  built manually.
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
- Application will function correctly regardless of firewall or OTP
  requirements.


# Milestones

- [x] Set up dictionary of country and Ads Accounts (Config/Secrets).
- [x] Set up credentials for Google, MS and Adobe (JSON, Token & KeyFile
      respectively).
- [ ] Set up DB tables for each quarter programmatically. Single quarter
      table combining platforms.
- [ ] Set up backfill (separate backfill_database() method with a date
      range parameter).
- [ ] Set up business date ranges for each platform with custom business
      fiscal year functionality (Module).
- [x] Pull basic campaign report or full ads report for each country.
- [ ] Pull program revenue data for each country report suite.
- [ ] Generate necessary database views for merged data.


# Modules to build

- [x] DB Module (dg-db)
- [x] Business Date Module (dg-date)
- [x] Google Ads module (dg-google)
- [x] Microsoft Ads module (dg-ms)


# Maybe Pile

- [ ] Use GitHub Actions for CI/CD
- [ ] Initial development script to automate Docker rebuilds

