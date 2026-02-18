from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "mlops",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="retrain_model",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    retrain = BashOperator(
        task_id="retrain_task",
        bash_command="python /opt/project/src/training/train.py",
    )

    retrain
