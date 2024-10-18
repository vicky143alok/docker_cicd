# Use the official Apache Airflow image
FROM apache/airflow:2.7.2-python3.9

# Switch to the root user to install system packages (if needed)
USER root

# Update the package list and install any necessary system packages
RUN apt-get update && apt-get install -y \
    # Add any system packages you need here
    && apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Switch back to the airflow user for installing Python packages
USER airflow

# Install the required Python packages
RUN pip install --user pandas boto3 snowflake-connector-python

# Optionally copy your DAGs and other configuration files here
# COPY ./dags /opt/airflow/dags
# COPY ./requirements.txt /requirements.txt

# Optionally install additional dependencies from requirements.txt if needed
# RUN pip install --user -r /requirements.txt

# Set the entry point for the container (this is already defined in the base image)
# ENTRYPOINT ["/usr/local/bin/entrypoint"]
# CMD ["airflow", "webserver"]
