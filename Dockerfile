# Use Debian slim as base image
FROM python:3.8-slim-buster

# Define the port number as a build argument with a default value
ARG APP_PORT=80

# Set the defined port number as an environment variable
ENV APP_PORT=${APP_PORT}

# Set working directory inside the container
WORKDIR /sitetack

# Copy the contents of the current directory to /sitetack in the container
COPY . .

# Install poetry and dependencies
RUN pip3 install poetry && \
    # Config poetry to not create virtualenvs
    poetry config virtualenvs.create false && \
    # Install dependencies
    poetry install && \
    # cleanup downloaded python packages
    rm -rf /root/.cache/pip

# Add a non-root user and switch to it
RUN useradd -m sitetack

# Give ownership of /sitetack to sitetack user
# This ensures the user has the necessary permissions
RUN chown -R sitetack:sitetack /sitetack

# Change to sitetack user
USER sitetack

# Set the default command to run the app using the environment variable for the port
CMD uvicorn sitetack.app.main:app --reload --host 0.0.0.0 --port ${APP_PORT}

# docker run -it -d -p 8100:8100 -v ${pwd}:/sitetack --name sitetack-dev python:3.8-slim-buster bash
# uvicorn sitetack.app.main:app --reload --host 0.0.0.0 --port 8100