# Use Debian Bookworm slim as base image
FROM python:3.8-slim-buster

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
