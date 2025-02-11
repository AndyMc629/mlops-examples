from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='oxford-genai-2025-inference',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['oxford-demo','inference'],
) as dag:

    # Fetching variables
    landing_data_path = Variable.get("landing_data_path", default_var="s3://mlops-pipeline-example/landing/bank.csv")
    output_path = Variable.get("output_data_path", default_var="s3://mlops-pipeline-example/inference/predictions.csv")
    docker_image = Variable.get("docker_image", default_var="mlops_pipeline")
    
    load_models = BashOperator(
        task_id='load_models',
        bash_command='echo "Loading models..."'
    )
    
    run_inference_pipeline = BashOperator(
        task_id='run_inference_pipeline',
        bash_command=f'docker run -v ~/.aws:/root/.aws:ro {docker_image} inference --data "{landing_data_path}" --output_dir "{output_path}"'
    )

    log_inference_data = BashOperator(
        task_id='log_inference_data',
        bash_command='echo "Logging inference data..."'
    )

    run_clean_up = BashOperator(
        task_id='run_clean_up',
        bash_command='echo cleaning up ...'
    )
    load_models >> run_inference_pipeline >> [log_inference_data, run_clean_up]