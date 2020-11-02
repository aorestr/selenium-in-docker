#################################
### Downloads the waiter file ###
#################################
FROM byrnedo/alpine-curl:0.1.8 as curl
# This file makes the container wait for another to be ready before running some other thing
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > wait-for-it.sh

##################################
### Set the Pytest environment ###
##################################
FROM python:3.9.0-alpine

# Set the working directory
WORKDIR /selenium_tests/

# Copy the folder with the tests into the container
COPY selenium_tests/ /selenium_tests/

# Copy the waiter
COPY --from=curl wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
RUN apk add bash

# Install all dependencies
RUN pip install -r requirements.txt

# This Dockerfile hasn't got any CMD or ENTRYPOINT so it doesn't do anything by its own.
# Check docker-compose.yml to see an implementation of the image