# mlops-examples
Some examples of MLOps implementations, used for my lectures at Oxford and elsewhere.

## oxford-mlops-example-2025

There is a makefile, no devcontainer running.

Key steps are really:
1. Ensure mlops-pipeline package is built with poetry
2. Use makefile to build the mlops-pipeline container
3. Use makefile to "deploy" the airflow dags
4. Use makefile to run airflow standalone
5. Login to airflow and run the dags you want

For evidently demo:
1. Use the MLEWP2 repo, Chapter03, navigate to the drift folder
2. ```conda activate mlewp-chapter03-drift```
3. ```jupyter notebook``` then run the evidently example
4. Try multiplying dataset by 1.1 to see drift