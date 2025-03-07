build-mlops-pipeline:
	@echo "Building mlops-pipeline package container"
	docker build -t mlops_pipeline ./mlops-pipeline

# Run the pipeline and mount your AWS credentials -> not correct for prod!
run-mlops-pipeline-inference:
	docker run \
	-v ~/.aws:/root/.aws:ro \
	mlops_pipeline inference --data "s3://mlops-pipeline-example/landing/bank.csv" --output_dir "s3://mlops-pipeline-example/inference/predictions.csv"

run-mlops-pipeline-monitor:
	docker run \
	-v ~/.aws:/root/.aws:ro \
	mlops_pipeline monitoring --output_dir "s3://mlops-pipeline-example/inference/predictions.csv" --truth_dir "s3://mlops-pipeline-example/ground-truth/bank.csv"

build-package:
	@cd ./mlops-pipeline && poetry install

run-airflow:
	@cd ./airflow && bash airflow-standalone.sh

install-airflow:
	@cd ./airflow && bash airflow-install.sh

deploy-airflow-dags:
	@cd ./airflow && bash airflow-deploy-dags.sh

clean-airflow-db:
	@cd ./airflow && bash airflow-db-clean-init.sh

redo-airflow-admin-user:
	@cd ./airflow && bash airflow-redo-admin-user.sh
