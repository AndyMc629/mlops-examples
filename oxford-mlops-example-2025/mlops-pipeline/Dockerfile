FROM python:3.10-slim

# Install poetry
RUN pip install poetry

# Copy project files and install the package
WORKDIR /app   
COPY . . /app/
RUN poetry install

# Default run run:main -> requires parameters to be passed.
ENTRYPOINT ["poetry", "run", "mlops-pipeline"]