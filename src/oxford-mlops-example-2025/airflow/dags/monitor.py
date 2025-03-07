from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="oxford-genai-2025-monitor",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["oxford-demo", "monitor"],
) as dag:
    # Fetching variables
    output_data_path = Variable.get(
        "output_data_path",
        default_var="s3://mlops-pipeline-example/inference/predictions.csv",
    )
    ground_truth_data_path = Variable.get(
        "ground_truth_data_path",
        default_var="s3://mlops-pipeline-example/ground-truth/bank.csv",
    )
    docker_image = Variable.get("docker_image", default_var="mlops_pipeline")

    run_monitor_pipeline = BashOperator(
        task_id="run_monitor_pipeline",
        bash_command=f'docker run -v ~/.aws:/root/.aws:ro {docker_image} monitoring --output_dir "{output_data_path}"  --truth_dir "{ground_truth_data_path}"',
    )

    run_trigger_alerts = BashOperator(
        task_id="run_trigger_alerts", bash_command="echo triggering alerts ..."
    )

    log_monitor_data = BashOperator(
        task_id="log_monitor_data", bash_command="echo logging monitor data ..."
    )

    run_clean_up = BashOperator(
        task_id="run_clean_up", bash_command="echo cleaning up ..."
    )

    run_monitor_pipeline >> run_trigger_alerts >> [log_monitor_data, run_clean_up]
