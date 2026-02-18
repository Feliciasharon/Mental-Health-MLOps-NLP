
FROM apache/airflow:2.9.3-python3.12

USER root

# Set working directory
WORKDIR /opt/airflow

# Copy project into container
COPY airflow/dags /opt/airflow/dags
COPY . /opt/airflow/mlops

# Give airflow ownership of project folder
RUN chown -R airflow: /opt/airflow/mlops

# Switch back to airflow user
USER airflow

# Install CPU torch FIRST (from PyTorch index)
RUN pip install --no-cache-dir \
    torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu

# Then install everything else from normal PyPI
RUN pip install --no-cache-dir \
    psycopg2-binary \
    pandas \
    numpy \
    scikit-learn==1.8.0 \
    sentence-transformers==5.2.2 \
    joblib


ENV PYTHONPATH="/opt/airflow/mlops"