from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import mlflow

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='Inference',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    run_python_pipeline = BashOperator(
        task_id='run_python_pipeline',
        bash_command='docker run --network airflow_network python-pipeline'
    )

    log_mlflow = BashOperator(
        task_id='log_mlflow',
        bash_command='docker run --network airflow_network mlflow'
    )

    run_python_pipeline 