# About

DG Tracker is an ETL application that tracks extracts account, campaign
and ads report data from the Google Ads and Microsoft Ads APIs,
transforms them using pre-built models with appropriate relationships
and loads them into a database. It also pulls metric reports, based on
RSID, from Adobe Analytics and creates an RSID/Account(s) relationship
so that both spend and site metrics can be tracked together.

Most databases are supported as it uses SQLAlchemy as an ORM which
allows easy switching of database provider.

This is the ETL component of a larger reporting suite. So what you do
with the data once it's loaded, is up to you. Sample DB views for paid
media program managers will be provided in the example directory. If you
are interested in the post ETL application, please see my other repos.



# DB Requirements

This app is quite flexible on DB choice. However, If you're using MySQL
as your database of choice, you'll need to change the
max_allowed_packets setting to something large for the ads reports to
actually write to the DB. So in your /etc/my.cnf file, add:

`[mysqld]
max_allowed_packet=999M
`

This is especially if you're extracting data for a large account or lots
of accounts. Packet size needs to be increased because the DB write time
is exponentially faster when using the bulk write functions of each
RDBMS.

# ToDo

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

# Maybe Pile

- [ ] Use GitHub Actions for CI/CD
- [ ] Initial development script to automate Docker rebuilds

