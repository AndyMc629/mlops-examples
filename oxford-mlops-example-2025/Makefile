build-mlops-pipeline:
	@echo "Building mlops-pipeline package container"
	docker build -t mlops_pipeline .

# Run the pipeline and mount your AWS credentials -> not correct for prod!
run-mlops-pipeline:
	docker run \
	-v ~/.aws:/root/.aws:ro \
	mlops_pipeline_test inference --data "s3://mlops-pipeline-example/landing/bank.csv"