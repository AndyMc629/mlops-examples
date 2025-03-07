# Running

1. Run the data ingestion example
```
poetry run python -m mlops_pipeline.data
```

2. Run the model inference example
```
poetry run mlops-pipeline inference --data "s3://mlops-pipeline-example/landing/bank.csv"
```

3. Get help on the package input parameters:
```
poetry run mlops-pipeline -h
```
