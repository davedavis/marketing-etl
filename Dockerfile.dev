# From Alpine, for keeping things small.
# Latest version is enough for type hinting.
FROM python:alpine

# Just me
MAINTAINER Dave Davis

# Setting the workdir on the container
WORKDIR /dg-tracker

# Copy and install the script dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all the files over.
COPY . .

# Run the main.py as the entry point (as CMD, not as ENTRYPOINT)
CMD [ "python", "./main.py" ]

# ToDo: Extract key/secrets
# docker build -t dg-tracker .
# docker run -it dg-tracker